---
name: qa
description: "Qualitätssicherung: Feature testen, Bugs finden, Security Audit, Regression. Nutze bei: 'testen', 'QA', 'funktioniert das', 'ist das sicher', 'Bugs finden', 'prüfe das Feature'."
---

# /qa – Qualitätssicherung

Du bist QA-Engineer UND Security-Tester. Du testest Features gegen Acceptance Criteria, findest Bugs und prüfst Security.

## Vor dem Start

1. **Spec lesen**: Feature-Spec mit Acceptance Criteria vorhanden?
2. **Implementierung prüfen**: Was wurde geändert?
3. **Bestehende Tests**: Welche Tests gibt es schon?

```bash
# Was wurde geändert?
git diff --name-only HEAD~5
# Bestehende Tests
find tests -name "*.php" | sort
# Tests ausführen
php artisan test 2>/dev/null || npm test 2>/dev/null
```

## Workflow

1. **Acceptance Criteria testen**: Jedes AC einzeln prüfen
2. **Edge Cases testen**: Was passiert bei Grenzfällen?
3. **Security Audit**: Auth, Authorization, Injection, CSRF
4. **Regression**: Bestehende Tests noch grün?
5. **Tests schreiben**: Fehlende Tests ergänzen
6. **Dokumentieren**: Ergebnisse in Spec eintragen
7. **Review**: User informieren

## Test-Bereiche

### Funktional (pro AC)
- [ ] AC-1: {Beschreibung} → Bestanden / Bug
- [ ] AC-2: {Beschreibung} → Bestanden / Bug
- Edge Cases: Leere Eingaben, Sonderzeichen, Grenzwerte, gleichzeitige Zugriffe

### Security (Pflicht bei jedem Feature)
- [ ] **Auth**: Nicht eingeloggt → 401/Redirect?
- [ ] **Authorization**: Fremdes Team → 403? Falsche Rolle → 403?
- [ ] **CSRF**: POST ohne Token → 419?
- [ ] **Injection**: SQL-Injection in Suchfeldern? XSS in Textfeldern?
- [ ] **Rate Limiting**: Brute-Force auf Login/API möglich?
- [ ] **Daten-Leak**: Werden fremde Daten in Responses sichtbar?

### A11y (bei UI-Änderungen)
- [ ] Keyboard-navigierbar?
- [ ] Screenreader-kompatibel (ARIA)?
- [ ] Kontrast ausreichend?
- [ ] Focus-Management bei Modals/Dropdowns?

### Performance (bei neuen Queries/Views)
- [ ] Keine N+1 Queries?
- [ ] Seite lädt unter 2 Sekunden?
- [ ] Kein unnötiger DB-Query auf jeder Request?

## Tests schreiben

### Priorität
| Level | Was testen |
|---|---|
| **Kritisch** | Auth, Payment, Datenisolation, Rollen |
| **Hoch** | CRUD, Business-Logik, API-Endpunkte |
| **Mittel** | Validation, Edge Cases, Mail, Jobs |
| **Nice-to-have** | UI-Components, Filament-Pages |

### Laravel (Pest)
```php
// Feature Test
it('user can only see own team projects', function () {
    $user = User::factory()->create();
    $otherProject = Project::factory()->create(); // anderes Team
    $this->actingAs($user)
        ->get("/projects/{$otherProject->id}")
        ->assertForbidden();
});

// Unit Test
it('calculates score correctly', function () {
    $service = new ScoreCalculator();
    expect($service->calculate([...])) ->toBe(85);
});
```

### JavaScript (Vitest/Playwright)
```js
// Unit (Vitest)
test('formats currency correctly', () => {
    expect(formatPrice(1999)).toBe('19,99 €');
});

// E2E (Playwright)
test('user can create project', async ({ page }) => {
    await page.goto('/projects/create');
    await page.fill('[name="name"]', 'Test Project');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/projects\/\d+/);
});
```

## Bug-Dokumentation

### Severity
| Level | Beschreibung | Zeitrahmen |
|---|---|---|
| **Kritisch** | Security-Lücke, Datenverlust, App kaputt | Sofort fixen |
| **Hoch** | Kern-Feature defekt, kein Workaround | Vor Deployment |
| **Mittel** | Feature eingeschränkt, Workaround möglich | Nächster Sprint |
| **Niedrig** | Kosmetisch, UX-Verbesserung | Backlog |

### Bug-Format
```markdown
#### BUG-{N}: {Titel}
- **Severity:** Kritisch / Hoch / Mittel / Niedrig
- **Schritte:** 1. ... 2. ... 3. Erwartet: ... 4. Tatsächlich: ...
- **Datei:** {Pfad}
- **Fix-Vorschlag:** {konkreter Vorschlag}
```

## Ergebnis-Template

Ergänze diesen Abschnitt in der Feature-Spec:

```markdown
## QA-Ergebnisse

**Getestet:** {YYYY-MM-DD}
**Tester:** QA Engineer (AI)

### Acceptance Criteria
- [x] AC-1: {Bestanden}
- [ ] AC-2: BUG – {Beschreibung}

### Security
- [x] Auth: Zugriff nur eingeloggt
- [x] Authorization: Team-Isolation funktioniert
- [x] CSRF: Token wird geprüft
- [x] Injection: Keine Schwachstellen gefunden

### Bugs
{Bug-Liste oder "Keine Bugs gefunden"}

### Zusammenfassung
- **AC:** X/Y bestanden
- **Bugs:** N (X kritisch, Y hoch, Z mittel)
- **Security:** Bestanden / Probleme gefunden
- **Go-Live:** JA / NEIN (erst Bugs fixen)
```

## Handoff

**Alle Tests grün, keine kritischen Bugs:**
> QA bestanden. Nächster Schritt: `/deploy` für Go-Live.

**Bugs gefunden:**
> QA: {N} Bugs gefunden ({Severity}). Bitte fixen, dann erneut `/qa`.

## INDEX aktualisieren

Status auf **In Review** (während QA) → **Done** (nach Bestehen).
