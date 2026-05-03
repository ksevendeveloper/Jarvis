import importlib
import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


TEST_MODULES = ["db", "api.models", "api.auth", "api.routes", "main"]


def _reload_app_modules():
    for name in TEST_MODULES:
        if name in sys.modules:
            del sys.modules[name]
    main = importlib.import_module("main")
    db = importlib.import_module("db")
    models = importlib.import_module("api.models")
    auth = importlib.import_module("api.auth")
    return main, db, models, auth


def _ensure_admin(db, models, auth):
    session = db.SessionLocal()
    try:
        user = session.query(models.User).filter(models.User.username == "admin").first()
        if user is None:
            user = models.User(
                username="admin",
                hashed_password=auth.pwd_context.hash("admin"),
                role="admin",
            )
            session.add(user)
            session.commit()
    finally:
        session.close()


def _setup_client(tmp_path: Path):
    os.environ["DATABASE_URL"] = f"sqlite:///{tmp_path / 'test.db'}"
    os.environ["JARVIS_JWT_SECRET"] = "test-secret"
    os.environ["JARVIS_ALLOWED_COMMANDS"] = "echo,pwd,ls,whoami,date,uptime"

    main, db, models, auth = _reload_app_modules()
    db.Base.metadata.create_all(bind=db.engine)
    _ensure_admin(db, models, auth)
    return TestClient(main.app)


def _login(client: TestClient):
    resp = client.post("/api/auth/login", json={"username": "admin", "password": "admin"})
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_health(tmp_path):
    client = _setup_client(tmp_path)
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_login_success_and_failure(tmp_path):
    client = _setup_client(tmp_path)

    ok = client.post("/api/auth/login", json={"username": "admin", "password": "admin"})
    assert ok.status_code == 200
    assert "access_token" in ok.json()

    bad = client.post("/api/auth/login", json={"username": "admin", "password": "wrong"})
    assert bad.status_code == 401


def test_execute_requires_auth(tmp_path):
    client = _setup_client(tmp_path)
    resp = client.post("/api/execute", json={"command": "echo hello"})
    assert resp.status_code == 401


def test_execute_allowlisted_command(tmp_path):
    client = _setup_client(tmp_path)
    headers = _login(client)

    resp = client.post("/api/execute", json={"command": "echo hello"}, headers=headers)
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["status"] == "scheduled"
    assert payload["submitted_by"] == "admin"


def test_execute_blocks_non_allowlisted_command(tmp_path):
    client = _setup_client(tmp_path)
    headers = _login(client)

    resp = client.post("/api/execute", json={"command": "python3 -V"}, headers=headers)
    assert resp.status_code == 403


def test_execute_blocks_dangerous_pattern(tmp_path):
    client = _setup_client(tmp_path)
    headers = _login(client)

    resp = client.post("/api/execute", json={"command": "echo ok && rm -rf /tmp/demo"}, headers=headers)
    assert resp.status_code == 400
