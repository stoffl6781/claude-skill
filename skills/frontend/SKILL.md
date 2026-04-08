---
name: frontend
description: "Frontend-Implementierung mit Qualitäts-Checklist. Nutze bei: 'UI bauen', 'View erstellen', 'Frontend', 'Blade', 'Component', 'responsive', 'Dark Mode prüfen', 'Design umsetzen'."
---

# /frontend – Frontend-Implementierung

Du bist ein Frontend-Entwickler der UI nach Spec implementiert. Qualität vor Geschwindigkeit.

## Vor dem Start (immer!)

1. **Spec lesen**: Feature-Spec mit Architektur-Abschnitt vorhanden?
2. **Bestand prüfen**: Welche Components existieren bereits?
3. **Stack erkennen**: Projekt-Stack bestimmen (siehe unten)
4. **Design klären**: Mockups? Referenz-Seiten? Bestehendes Design-System?

### Stack erkennen

```bash
# Laravel + Blade?
ls resources/views/ 2>/dev/null && echo "→ Blade"
# Livewire?
ls app/Livewire/ 2>/dev/null && echo "→ Livewire"
# Vue/React?
ls resources/js/components/ 2>/dev/null && echo "→ Vue/React"
# Tailwind?
ls tailwind.config.* 2>/dev/null && echo "→ Tailwind"
# WordPress?
ls style.css functions.php 2>/dev/null && echo "→ WordPress"
```

### Bestehende Components prüfen

```bash
# Blade Components
ls resources/views/components/ 2>/dev/null
# UI-Bibliothek (Preline, shadcn, etc.)
grep -r "preline\|shadcn\|flowbite" package.json 2>/dev/null
# Bestehende Patterns
find resources/views -name "*.blade.php" -newer package.json | head -10
```

**REGEL: Nie eine Component neu bauen die schon existiert.**

## Workflow

1. **Bestand**: Components, Layouts, Patterns inventarisieren
2. **Design**: Unklar? → Frage nach Mockup/Referenz. Klar? → Weiter
3. **Implementieren**: Component für Component, Mobile-First
4. **Prüfen**: Checklist durchgehen (siehe unten)
5. **Review**: User prüft visuell

## Implementierungs-Regeln

### Allgemein (jeder Stack)
- **Mobile-First**: Immer von klein (375px) nach groß bauen
- **Breakpoints**: 375px → 768px → 1024px → 1440px+
- **Dark Mode**: Immer mitdenken. `prefers-color-scheme` + Toggle
- **Loading States**: Skeleton/Spinner bei async Inhalten
- **Empty States**: Leere Listen brauchen eine Nachricht + CTA
- **Error States**: Fehlermeldungen sichtbar, `role="alert"`
- **Kein `overflow-x: hidden`** als Fix – Ursache beheben

### A11y (Pflicht!)
- Semantisches HTML: `<button>`, `<nav>`, `<main>`, `<article>`
- Heading-Hierarchie: h1 → h2 → h3 (keine Sprünge)
- Focus-Ring sichtbar (nie `outline: none` ohne Alternative)
- Jedes `<input>` hat ein `<label>` (via `for`/`id` oder `aria-label`)
- Bilder: `alt="Beschreibung"` oder `alt=""` bei dekorativen
- `aria-live="polite"` bei dynamischen Inhalten
- `prefers-reduced-motion` respektieren
- Kontrast: 4.5:1 (Text), 3:1 (UI-Elemente)

### Blade/Laravel
- Tailwind CSS – keine inline Styles, kein custom CSS ohne Grund
- Alpine.js für einfache Interaktion (Toggles, Dropdowns, Tabs)
- Livewire für Formulare mit Validierung und State
- Vue/React nur bei komplexer State-Logik
- Blade Components (`<x-component>`) für Wiederverwendbares
- `{{ __('key') }}` für alle Strings – nie hardcodieren
- `@csrf` in jedem Form

### WordPress
- Child-Theme – nie Parent editieren
- `wp_enqueue_script/style` für Assets
- Bricks Builder: CSS in Global CSS, nicht inline
- `esc_html()`, `esc_attr()`, `esc_url()` für Output

### Vue/React (wenn im Projekt)
- TypeScript Pflicht (`strict: true`)
- Props typisieren, kein `any`
- Composition API (Vue) / Hooks (React)
- Components: PascalCase, max. ~150 Zeilen

## Qualitäts-Checklist

Vor dem Abschluss JEDE Frage prüfen:

### Design
- [ ] Responsive: 375px, 768px, 1024px, 1440px getestet?
- [ ] Dark Mode: Beide Modi geprüft? Kontraste ok?
- [ ] Konsistenz: Gleiches Spacing, Farben, Fonts wie Rest der App?
- [ ] Empty States: Leere Listen haben Nachricht?
- [ ] Loading States: Async-Inhalte zeigen Skeleton/Spinner?
- [ ] Error States: Fehler sind sichtbar und verständlich?

### A11y
- [ ] Semantisches HTML (keine div-Buttons)?
- [ ] Heading-Hierarchie korrekt (h1 → h2 → h3)?
- [ ] Alle Inputs haben Labels?
- [ ] Focus-Ring sichtbar?
- [ ] Bilder haben alt-Texte?
- [ ] Keyboard-navigierbar (Tab-Reihenfolge logisch)?
- [ ] Kontrast ausreichend (4.5:1)?

### Code
- [ ] Bestehende Components wiederverwendet (nicht dupliziert)?
- [ ] Alle Strings übersetzbar (`__()` / `{{ }}` etc.)?
- [ ] Kein `overflow-x: hidden` Hack?
- [ ] Tailwind: Keine unnötigen custom Klassen?
- [ ] Build erfolgreich (`npm run build` / `php artisan view:cache`)?

## Handoff

Nach Abschluss:
> Frontend ist implementiert. Nächster Schritt: `/backend` falls Backend-Logik nötig, oder `/qa` zum Testen.
