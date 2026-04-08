---
description: "Allgemeine Regeln für Code-Qualität, Naming, Kommunikation. Gilt überall."
globs: "**/*"
---

# Allgemeine Regeln

## Kommunikation
- Antworten auf Deutsch (Code-Kommentare auf Englisch)
- Bei langen Tasks: Erst Plan zeigen, dann umsetzen
- Vorschläge mit Begründung: "Ich würde X wählen, weil Y"
- Bei Breaking Changes: Explizit warnen

## Code-Qualität
- Variablen und Funktionen: Selbsterklärend, keine Abkürzungen (`$user` statt `$u`)
- Funktionen: Max ~20 Zeilen, eine Aufgabe
- Keine Magic Numbers: Konstanten nutzen
- Kommentare erklären WARUM, nicht WAS
- Boy Scout Rule: Code sauberer hinterlassen als vorgefunden

## Feature-Workflow
- Neues Feature? → Prüfe ob `features/INDEX.md` existiert
- Nutze den Workflow: `/requirements` → `/architecture` → `/frontend` + `/backend` → `/qa` → `/deploy`
- Status in `features/INDEX.md` aktuell halten

## Git
- Conventional Commits: `feat(scope):`, `fix(scope):`, `refactor(scope):`
- Kein Push ohne Bestätigung
- Keine Secrets committen (.env, API-Keys)
- Sensitive Dateien immer prüfen vor `git add`

## NIEMALS
- `var_dump()`, `dump()`, `dd()`, `console.log()` in Produktionscode lassen
- Secrets hardcodieren
- Code ohne Review einbinden
- Features ohne Plan drauflos coden
