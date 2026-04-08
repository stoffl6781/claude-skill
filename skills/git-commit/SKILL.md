---
name: git-commit
description: >
  Smart Git Commit & Push. Nutze bei: "commit", "push", "committen",
  "pushen", "Änderungen sichern", "mach einen commit", "stage and commit",
  "fass die Änderungen zusammen", "Was hat sich geändert?".
---

# Git Commit & Push

## Workflow

1. `git status --short` + `git diff` + `git diff --cached` – Änderungen erfassen
2. Nur Chat-relevante Änderungen stagen (außer User sagt "alles")
3. Thematisch zusammengehörend? → 1 Commit. Trennbar? → mehrere
4. Commit-Message: Conventional Commits (→ CLAUDE.md Kapitel 10)
5. Zusammenfassung zeigen, User bestätigen lassen
6. Commit + Push (nur wenn User will). Neuer Branch: `git push -u origin {branch}`

## Commit-Message

```
type(scope): kurze Beschreibung (Imperativ, max 72 Zeichen, Englisch)
```

Types: `feat`, `fix`, `refactor`, `style`, `docs`, `chore`, `perf`, `test`, `security`, `a11y`, `i18n`

## Regeln

- **Scope:** Nur Chat-relevante Dateien stagen. Andere erwähnen aber nicht committen
- **Sensible Dateien:** `.env`, Credentials → NIEMALS committen, warnen
- **Große Binaries:** Warnen wenn >5MB
- **Sprache:** Message Englisch, Chat Deutsch

## Sonderfälle

| Fall | Aktion |
|---|---|
| Pre-Hook Failure | Fehler beheben, **NEUER Commit**. Nie `--amend`, nie `--no-verify` |
| Amend | Nur wenn User explizit sagt UND nicht gepusht |
| Merge-Konflikte | Nicht auto-resolven, User fragen |
| Kein Remote | Nur committen, User informieren |
| Leerer Diff | Nichts committen, User informieren |
