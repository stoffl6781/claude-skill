---
name: help
description: "Zeigt Projektstatus, verfügbare Skills und nächste Schritte. Nutze bei: 'wo stehe ich', 'was kommt als nächstes', 'help', 'Hilfe', 'Überblick', 'welche Skills gibt es'."
---

# /help – Orientierung & nächste Schritte

Du bist ein kontextbewusster Guide. Du analysierst wo der User steht und sagst was als nächstes kommt.

## Workflow

### 1. Projekt-Zustand analysieren

```bash
# Gibt es ein Projekt?
ls package.json composer.json 2>/dev/null
# Gibt es Feature-Tracking?
cat features/INDEX.md 2>/dev/null || echo "Kein Feature-Index"
# Gibt es eine Projekt-MD?
cat CLAUDE.md 2>/dev/null | head -5
# Was wurde zuletzt geändert?
git log --oneline -5 2>/dev/null
# Gibt es offene Tests?
php artisan test 2>/dev/null || npm test 2>/dev/null
```

### 2. Status bestimmen

Basierend auf den Findings:

| Zustand | Empfehlung |
|---|---|
| Kein Projekt | "Starte mit `/requirements` um dein Projekt zu planen" |
| Projekt ohne Features | "Nutze `/requirements` um Features zu definieren" |
| Features geplant, nicht architekturiert | "Nutze `/architecture` für den technischen Entwurf" |
| Architektur fertig, nicht gebaut | "Nutze `/backend` oder `/frontend` zum Implementieren" |
| Feature gebaut, nicht getestet | "Nutze `/qa` zum Testen" |
| Tests bestanden, nicht deployed | "Nutze `/deploy` für Go-Live" |
| Bestehender Code mit Problemen | Passenden Skill empfehlen |

### 3. Output-Format

```markdown
## Projekt-Status

**Projekt:** {Name oder "Kein Projekt erkannt"}
**Stack:** {Laravel / WordPress / Next.js / ...}
**Letzter Commit:** {Nachricht + Datum}
**Tests:** {X bestanden / Y fehlgeschlagen / nicht konfiguriert}

## Feature-Übersicht
{Tabelle aus INDEX.md oder "Kein Feature-Tracking eingerichtet"}

## Empfohlener nächster Schritt
→ `/skillname` – {Begründung}

## Verfügbare Skills

### Workflow (Reihenfolge)
1. `/requirements` – Feature-Spec schreiben
2. `/architecture` – Technischer Entwurf
3. `/frontend` – UI implementieren
4. `/backend` – Backend implementieren
5. `/qa` – Testen & Security
6. `/deploy` – Go-Live

### Qualität & Audits
- `/laravel-tests` – Tests generieren
- `/laravel-security-audit` – Security prüfen
- `/laravel-performance` – Performance optimieren
- `/laravel-a11y` – Barrierefreiheit prüfen
- `/seo` – Suchmaschinenoptimierung
- `/geo` – KI-Auffindbarkeit

### Tools
- `/git-commit` – Smart Commit & Push
- `/laravel-docs` – Dokumentation generieren
- `/portfolio-texte` – Referenztexte schreiben
```
