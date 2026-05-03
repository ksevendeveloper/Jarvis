# Git Release Comments — Jarvis

Use os blocos abaixo para subir as atualizações em etapas.

## Atualização 1 — Imagens demonstrativas completas

```bash
git add docs/images/architecture.svg docs/images/workflow.svg docs/images/ui-mockup.svg
git commit -m "docs(images): replace demo diagrams with complete production-style visuals"
git push origin main
```

## Atualização 2 — Página web completa para GitHub Pages

```bash
git add docs/index.html
git commit -m "docs(site): add full GitHub Pages landing with architecture, workflow and setup"
git push origin main
```

## Atualização 3 — Guia de release com comentários de commit

```bash
git add docs/GIT_RELEASE_COMMENTS.md
git commit -m "docs(release): add ready-to-use git comments and publish steps"
git push origin main
```

## Atualização 4 — Publicação final de documentação (opcional, tudo junto)

```bash
git add docs/
git commit -m "docs: finalize visual documentation pack and GitHub page"
git push origin main
```

## Atualização 5 — Site completo (guia, docs, funcionalidades, versões, downloads, autores)

```bash
git add docs/index.html
git commit -m "docs(site): expand to full project website with guide, docs, features, changelog, downloads and authors"
git push origin main
```

## Ativação do GitHub Pages

No GitHub:
1. Abra `Settings` do repositório.
2. Entre em `Pages`.
3. Em `Build and deployment`, selecione `Deploy from a branch`.
4. Escolha branch `main` e pasta `/docs`.
5. Salve.
