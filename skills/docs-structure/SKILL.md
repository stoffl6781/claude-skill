---
name: docs-structure
description: "Projekt-Dokumentation nach Hub-Pattern erstellen und pflegen: docs/{bereich}/general.md mit Code-Pfaden, Status, Trigger-Wörtern. Nutze bei: 'Doku anlegen', 'Docs strukturieren', 'wo finde ich was', 'Code-Map', 'Projekt-Doku', 'Modul dokumentieren'."
---

# /docs-structure – Projekt-Dokumentation nach Hub-Pattern

Du erstellst und pflegst eine strukturierte Projektdokumentation die Claude (und Menschen) sofort zeigt, wo welche Dateien zu finden sind.

## Das Prinzip

Jedes Modul/Feature bekommt eine **Hub-Datei** (`docs/{bereich}/general.md`) die als Einstiegspunkt dient:
- **Code-Pfade**: Controller, Services, Models, Views, Routes, Tests – alles auf einen Blick
- **Status**: Was ist fertig, was in Arbeit, was offen
- **Trigger-Wörter**: Wann soll Claude diese Datei lesen
- **Abhängigkeiten**: Was nutzt dieses Modul, wer nutzt es

Plus: **Eine zentrale Lookup-Tabelle** in `CLAUDE.md` die alle Hub-Dateien mit Trigger-Wörtern listet.

## Workflow

### Modus 1: Initiale Struktur anlegen

Trigger: Projekt hat keine `docs/` Struktur oder `/docs-structure init`.

1. **Codebase scannen**: Welche Module existieren?
2. **Bereiche identifizieren**: Logische Gruppierung der Module
3. **Hub-Dateien erstellen**: Pro Bereich eine `general.md`
4. **Lookup-Tabelle**: In `CLAUDE.md` die zentrale Tabelle ergänzen
5. **Patterns**: `docs/patterns/` mit Templates und Regeln

```bash
# Module erkennen
ls app/Http/Controllers/*/ 2>/dev/null
ls app/Services/*/ 2>/dev/null
ls app/Models/ 2>/dev/null
find resources/views -maxdepth 1 -type d 2>/dev/null
ls app/Jobs/*/ 2>/dev/null
```

### Modus 2: Einzelnes Modul dokumentieren

Trigger: Neues Feature/Modul erstellt oder `/docs-structure {bereich}`.

1. **Modul analysieren**: Controllers, Services, Models, Views, Routes, Jobs, Tests finden
2. **Hub-Datei erstellen**: `docs/{bereich}/general.md` nach Template
3. **Lookup-Tabelle updaten**: Neuen Eintrag in `CLAUDE.md`

### Modus 3: Docs aktualisieren

Trigger: Nach Code-Änderungen oder `/docs-structure update`.

1. **Änderungen erkennen**: `git diff --name-only HEAD~5`
2. **Betroffene Hub-Dateien identifizieren**: Welche Bereiche wurden geändert?
3. **Code-Pfade prüfen**: Stimmen die Pfade noch? Neue Dateien ergänzen?
4. **Status aktualisieren**: Features die fertig sind → ✅

## Hub-Datei Template

Erstelle als `docs/{bereich}/general.md`:

```markdown
# {Titel}

> **Bereich:** {bereich-slug}
> **Letzte Aktualisierung:** {YYYY-MM-DD}
> **Status:** {aktiv | geplant | archiviert}

## Überblick
{1-3 Sätze: Was ist das, was tut es, warum existiert es}

## Status
- ✅ {Was fertig ist}
- 🔄 {Was in Arbeit ist}
- ⬚ {Was geplant/offen ist}

## Code-Pfade
| Typ | Pfad |
|---|---|
| Controller | `app/Http/Controllers/{...}` |
| Service | `app/Services/{...}` |
| Model | `app/Models/{...}` |
| Enums | `app/Enums/{...}` |
| Views | `resources/views/{...}` |
| Routes | `routes/web.php:L{x}-{y}` |
| Tests | `tests/{...}` |
| Config | `config/{...}` |
| Lang | `lang/{de,en}/{...}.php` |
| Jobs | `app/Jobs/{...}` |
| Migrations | `database/migrations/{...}` |

## Relevante Enums
| Enum | Werte | Zweck |
|---|---|---|
| `{EnumName}` | {wert1, wert2} | {Beschreibung} |

## Scheduled Tasks & Commands
| Command / Schedule | Wann | Zweck |
|---|---|---|
| `{command}` | {Zeitplan} | {Beschreibung} |

## Externe APIs / Services
| Service | Config | Zweck |
|---|---|---|
| {Name} | `config/{...}` | {Beschreibung} |

## Abhängigkeiten
- → **nutzt:** {andere Module/Services}
- ← **genutzt von:** {wer ruft dieses Modul auf}

## Ablauf
{Hauptflow als nummerierte Schritte}

## Erweiterung
### {Typische Aufgabe: z.B. "Neuen Check hinzufügen"}
1. {Schritt 1}
2. {Schritt 2}
```

## Lookup-Tabelle (in CLAUDE.md)

Erstelle/ergänze diesen Abschnitt in der Projekt-`CLAUDE.md`:

```markdown
## Dokumentation

**Regel:** Lies `docs/{bereich}/general.md` wenn du an einem Bereich arbeitest.

| Bereich | Hub-Datei | Trigger-Wörter |
|---|---|---|
| {Bereich} | `docs/{slug}/general.md` | {Wort1, Wort2, Wort3} |
```

**Trigger-Wörter**: Die Begriffe die ein User oder Claude verwenden würde wenn es um diesen Bereich geht. Beispiele:
- SEO → "SEO, PageSpeed, Crawler, Sitemap, Schema"
- Auth → "Login, Register, Passwort, 2FA, Invite"
- Billing → "Zahlung, Abo, Subscription, Mollie, Credits"

## Patterns-Ordner

Erstelle `docs/patterns/` mit:

**`docs/patterns/development.md`** – Globale Entwicklungsregeln:
```markdown
# Entwicklungsregeln

## 1. Test-Pflicht
Kein Feature ohne Tests. Gibt es keine Tests für den berührten Bereich, neue erstellen.

## 2. Doc Auto-Update
Bei Änderungen an einem Modul → zugehörige `general.md` prüfen und aktualisieren:
- Controller/Service/Model verschoben/erstellt → Code-Pfade-Tabelle prüfen
- Enum hinzugefügt/entfernt → Enum-Tabelle prüfen
- Scheduled Task geändert → Tasks-Tabelle prüfen
- Feature fertig → Status-Sektion updaten (⬚ → 🔄 → ✅)

## 3. Neue Features → Doc anlegen
Neues Feature? → prüfen ob Doc existiert, sonst nach Template anlegen.

## 4. Boy Scout Rule
Docs besser hinterlassen als vorgefunden.
```

**`docs/patterns/doc-template.md`** – Das Hub-Datei Template (wie oben).

## Regeln

1. **Code-Pfade müssen stimmen**: Jeder Pfad in der Tabelle muss eine echte Datei referenzieren. Vor dem Schreiben prüfen: `ls {pfad}` 
2. **Nicht raten**: Wenn du nicht sicher bist ob ein Controller existiert → nachschauen, nicht erfinden
3. **Granularität**: Ein Bereich = ein logisches Modul. Nicht zu fein (jeder Controller einzeln) und nicht zu grob (alles in einer Datei)
4. **Aktuell halten**: Die Doku ist nur wertvoll wenn sie stimmt. Lieber weniger aber korrekt als viel aber veraltet
5. **Trigger-Wörter großzügig**: Lieber ein Trigger-Wort zu viel als dass Claude die richtige Doku nicht findet

## Typische Bereichs-Aufteilung

### Laravel-Projekte
```
docs/
├── patterns/           # Globale Regeln + Templates
│   ├── development.md
│   └── doc-template.md
├── auth/               # Login, Register, 2FA, Rollen
├── billing/            # Payment, Subscriptions, Credits
├── {feature}/          # Pro Feature-Modul
│   ├── general.md      # Hub-Datei
│   └── {detail}.md     # Detail-Docs bei Bedarf
└── infrastruktur/      # Hosting, Deploy, Queue, Redis
```

### WordPress-Projekte
```
docs/
├── patterns/
├── theme/              # Child-Theme, Templates, Bricks
├── plugins/            # Custom Plugins, ACF, Polylang
├── content/            # CPTs, Taxonomies, Menus
└── hosting/            # Server, Caching, Updates
```

## Handoff

Nach Abschluss:
> Dokumentation erstellt/aktualisiert. {X} Hub-Dateien, {Y} Code-Pfade dokumentiert.
> Claude findet jetzt automatisch die richtige Datei anhand der Trigger-Wörter in CLAUDE.md.
