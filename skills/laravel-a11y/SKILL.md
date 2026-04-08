---
name: laravel-a11y
description: >
  WCAG 2.1 AA Accessibility-Audit für Laravel/Blade.
  Nutze bei: "A11y prüfen", "Barrierefreiheit", "WCAG Audit",
  "ist das barrierefrei", "aria fehlt", "alt-Texte", "Kontrast",
  "Tastatur-Navigation", "Screenreader", "A11y Tests", "BITV".
---

# Laravel A11y Audit (WCAG 2.1 AA)

Allgemeine WCAG-Regeln → **CLAUDE.md Kapitel 4**. Dieser Skill fokussiert auf Laravel/Blade-spezifische Audit-Methodik.

## Workflow

| Schritt | Aktion |
|---|---|
| 1. Scan | Blade-Templates, Layouts, Components finden und analysieren |
| 2. Analyse | WCAG-Kriterien gegen Code prüfen (siehe Checkliste) |
| 3. Fix | Automatisch behebbare Issues fixen |
| 4. Test | Pest-Tests für dauerhafte A11y-Sicherung |
| 5. Report | Ergebnisse als Markdown/JSON |

## Scan-Befehle

```bash
find resources/views -name "*.blade.php" | sort
grep -rln "<form\|wire:submit" resources/views/ --include="*.blade.php"
grep -rln "onclick\|@click\|x-on:click" resources/views/ --include="*.blade.php"
grep -rln "<img" resources/views/ --include="*.blade.php"
```

## Blade-spezifische Prüfpunkte

**Bilder:**
- `<img>` ohne `alt` → Fix: `alt=""` (dekorativ) oder beschreibender Text
- Spatie MediaLibrary: `alt` aus `custom_properties.alt` ziehen

**Formulare:**
- Jedes Input braucht `<label for="id">` oder `aria-label`
- Livewire `wire:model` Inputs: Label nicht vergessen
- Fehlermeldungen: `@error` Block mit `role="alert"` oder `aria-describedby`

**Interaktive Elemente:**
- Alpine.js Toggles: `aria-expanded`, `aria-controls` setzen
- Modals: `role="dialog"`, `aria-modal="true"`, Focus-Trap
- Custom Dropdowns: `role="listbox"`, Keyboard-Navigation

**Navigation:**
- Skip-Link: `<a href="#main-content" class="sr-only focus:not-sr-only">`
- `<nav aria-label="Hauptnavigation">` – nicht nur `<nav>`
- Mobile-Menü: `aria-expanded` auf Toggle-Button

**Dynamischer Content:**
- Livewire-Updates: `aria-live="polite"` auf Container
- Loading States: `aria-busy="true"` während Laden

## Pest-Test Beispiele

```php
it('all images have alt attributes', function () {
    $response = $this->get('/');
    $response->assertDontSee('<img ', false); // Oder:
    // DOM parsen und prüfen dass jedes <img> alt hat
});

it('all forms have labels', function () {
    $response = $this->get('/kontakt');
    $response->assertSee('<label', false);
});

it('skip link exists', function () {
    $response = $this->get('/');
    $response->assertSee('skip', false);
});

it('page has exactly one h1', function () {
    $response = $this->get('/');
    expect(substr_count($response->getContent(), '<h1'))->toBe(1);
});
```

## Tools zur Validierung

- **axe DevTools** (Chrome Extension) – automatisierter Scan
- **WAVE** (WebAIM) – visuelles Overlay
- **Lighthouse** (Chrome) – A11y Score
- **VoiceOver** (macOS) – Screenreader-Test

## Report-Format

```markdown
# A11y Audit – {Projekt}

## Zusammenfassung
{X} Kritisch, {Y} Wichtig, {Z} Hinweise

## Findings
| # | Severity | WCAG | Problem | Datei | Fix |
|---|----------|------|---------|-------|-----|
| 1 | Kritisch | 1.1.1 | Bild ohne alt | show.blade.php:42 | alt="" hinzufügen |
```
