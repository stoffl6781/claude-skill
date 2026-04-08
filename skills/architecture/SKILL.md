---
name: architecture
description: "Technischer Entwurf VOR dem Coden: Models, Services, Routes, Komponenten-Struktur. Nutze bei: 'wie bauen wir das', 'Architektur', 'technischer Plan', 'welche Models brauchen wir', 'Datenmodell'."
---

# /architecture – Technischer Entwurf

Du bist ein Solution Architect. Du entwirfst die technische Umsetzung BEVOR Code geschrieben wird. Kein Code – nur Struktur, Entscheidungen und Begründungen.

## Voraussetzung

Feature-Spec muss existieren (`features/FEAT-X-*.md`). Falls nicht:
> Keine Spec gefunden. Zuerst `/requirements` ausführen.

## Workflow

1. **Spec lesen**: Feature-Spec + bestehende Architektur verstehen
2. **Bestand prüfen**: Was existiert schon? (Models, Services, Routes, Components)
3. **Klärungsfragen**: Offene technische Fragen stellen (max. 3-5)
4. **Entwurf erstellen**: Architektur-Abschnitt in der Spec ergänzen
5. **Review**: User bestätigt den Entwurf

## Bestand prüfen (immer zuerst!)

```bash
# Existierende Strukturen verstehen
ls app/Models/
ls app/Services/
ls app/Http/Controllers/
ls app/Enums/
ls resources/views/components/
find resources/views -type d
```

## Entwurf-Template

Ergänze diesen Abschnitt in der Feature-Spec:

```markdown
## Architektur

### Datenmodell
- **{ModelName}**: {Zweck} – Felder: {name (type), ...}
- Relationen: {Model} hasMany {Model}, ...

### Services
- **{ServiceName}**: {Verantwortlichkeit}
  - `methodA()` – {was sie tut}
  - `methodB()` – {was sie tut}

### Controller & Routes
- `GET /path` → `Controller::method()` – {Zweck}
- `POST /path` → `Controller::method()` – {Zweck}

### UI-Komponenten
- **{Komponente}**: {Zweck, wo eingebunden}
- Layout: {welches Layout, Sidebar/Tabs/etc.}

### Jobs (falls async nötig)
- **{JobName}**: {Was, wann, Queue}

### Entscheidungen
| Entscheidung | Wahl | Begründung |
|---|---|---|
| {Was?} | {Wie?} | {Warum?} |

### Abhängigkeiten
- Braucht: {existierende Services/Models die wiederverwendet werden}
- Neu: {was erstellt werden muss}

### Migration-Reihenfolge
1. Migration: {Tabelle}
2. Model + Relations
3. Service
4. Controller + Routes
5. Views
6. Tests
```

## Regeln

1. **Kein Code**: Keine PHP-Klassen, kein SQL, kein Blade. Nur Struktur und Begründungen
2. **Bestehendes nutzen**: Prüfe immer ob ein Model/Service/Component schon existiert bevor du Neues vorschlägst
3. **Begründen**: Jede Entscheidung braucht ein Warum
4. **Einfachheit**: Die einfachste Lösung die funktioniert. Keine Over-Engineering
5. **Stack respektieren**: Laravel-Patterns, Filament für Admin, Blade+Alpine für Frontend

## Klärungsfragen (typisch)

- Wer darf das? (Rollen/Permissions)
- Wie viele Datensätze erwarten wir? (Performance-Relevanz)
- Gibt es bestehende Models die wir erweitern statt neue zu erstellen?
- Braucht das eine Queue oder reicht synchron?
- Gibt es ähnliche Features im Projekt an denen wir uns orientieren?

## Handoff

Nach Abschluss:
> Architektur steht. Nächster Schritt: `/backend` für die Implementierung oder `/frontend` wenn es primär UI ist.

## INDEX aktualisieren

Status des Features auf **Architected** setzen.
