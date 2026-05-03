#!/usr/bin/env python3
"""Bootstrap helpers for the Jarvis database.

Usage:
  python3 scripts/bootstrap_db.py --create-admin <username> <password>
  python3 scripts/bootstrap_db.py --info
"""
import argparse
import os
import sys

from db import engine, Base, SessionLocal
from api import models as orm_models
from passlib.context import CryptContext

# Use pbkdf2_sha256 for compatibility
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def create_tables():
    print("Creating database tables (if not exist)...")
    Base.metadata.create_all(bind=engine)


def create_admin(username: str, password: str):
    db = SessionLocal()
    try:
        existing = db.query(orm_models.User).filter(orm_models.User.username == username).first()
        if existing:
            print(f"User '{username}' already exists (id={existing.id}). Skipping creation.")
            return
        hashed = pwd_context.hash(password)
        user = orm_models.User(username=username, hashed_password=hashed, role="admin")
        db.add(user)
        db.commit()
        print(f"Created admin user '{username}'.")
    finally:
        db.close()


def info():
    print(f"DATABASE_URL={os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/jarvis')}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--create-admin", nargs=2, metavar=("USERNAME", "PASSWORD"), help="Create admin user")
    parser.add_argument("--info", action="store_true", help="Show DB info")
    args = parser.parse_args()

    if args.info:
        info()
        return

    create_tables()

    if args.create_admin:
        username, password = args.create_admin
        create_admin(username, password)


if __name__ == "__main__":
    main()
