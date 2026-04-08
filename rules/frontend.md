---
description: "Frontend-Regeln für Blade, Vue, React, CSS, JS. Automatisch aktiv bei Frontend-Dateien."
globs: "resources/views/**/*.blade.php,resources/js/**,resources/css/**,src/components/**,*.vue,*.tsx,*.jsx"
---

# Frontend-Regeln

## Component-Reuse (PFLICHT)
Vor dem Erstellen einer neuen Component:
1. Prüfe bestehende Components (`ls resources/views/components/` oder `ls src/components/ui/`)
2. Prüfe UI-Bibliothek (Preline, shadcn, Flowbite)
3. Nur neue Component wenn nichts Passendes existiert

## Tailwind CSS
- Tailwind als Basis – keine inline Styles
- Keine unnötigen Custom-Klassen wenn Tailwind-Utility reicht
- Responsive: Mobile-First (375px → 768px → 1024px → 1440px)
- Dark Mode: `prefers-color-scheme` + Toggle-Klasse

## A11y (immer!)
- Semantisches HTML: `<button>`, `<nav>`, `<main>`, `<article>`
- Heading-Hierarchie: h1 → h2 → h3 (keine Sprünge)
- Focus-Ring sichtbar – nie `outline: none` ohne Alternative
- Jedes `<input>` hat ein `<label>`
- `alt` auf Bildern (beschreibend oder `alt=""` bei dekorativen)
- `aria-live="polite"` bei dynamischen Inhalten
- `prefers-reduced-motion` respektieren
- Kontrast: 4.5:1 (Text), 3:1 (UI-Elemente)

## States
- Loading: Skeleton oder Spinner bei async
- Empty: Nachricht + CTA bei leeren Listen
- Error: Sichtbar, `role="alert"`, verständlich

## Blade/Laravel
- `{{ __('key') }}` für alle Strings
- `@csrf` in jedem Form
- Alpine.js für einfache Interaktion
- Livewire für State-Heavy Forms

## JavaScript
- `const` by default, `let` wenn nötig, kein `var`
- Async/Await statt Promise-Chains
- Destructuring, Optional Chaining, Nullish Coalescing
- `{ passive: true }` bei Scroll/Touch-Events
- Error Handling: try/catch mit User-Feedback
- Kein jQuery wenn natives JS reicht (ES2020+)

## TypeScript (bei Vue/React Pflicht)
- `strict: true` in `tsconfig.json`
- Props, Emits, API-Responses typisieren
- Kein `any` ohne expliziten Grund
