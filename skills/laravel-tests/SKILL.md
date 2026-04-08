---
name: laravel-tests
description: >
  Generiert Pest-Tests für Laravel. Scannt Codebase, erstellt Tests nach Priorität.
  Nutze bei: "Tests schreiben", "Test generieren", "Pest Tests", "Feature Tests",
  "Unit Tests", "teste den Controller/Model/Service", "Coverage verbessern",
  "ist das getestet?", "Refactoring absichern".
---

# Laravel Pest Test Generator

## Grundprinzipien

1. Pest-Syntax (nicht PHPUnit). 2. Arrange-Act-Assert. 3. Ein Assert pro Test.
4. Factories nutzen. 5. RefreshDatabase. 6. Sprechende Namen.

## Workflow

1. **Scan:** Existierende Tests, Models, Controller, Services, Routes, Jobs identifizieren
2. **Plan:** Test-Prioritäten festlegen (KRITISCH → NÜTZLICH)
3. **Infrastruktur:** Pest.php, Factories, Test-Helpers prüfen
4. **Schreiben:** Tests nach Patterns unten
5. **Ausführen:** `php artisan test` oder `vendor/bin/pest`

## Test-Prioritäten

| Priorität | Was testen |
|---|---|
| KRITISCH | Auth, Login, Passwort, Rollen, Payment |
| HOCH | CRUD-Operationen, Business-Logik, API-Endpoints |
| MITTEL | Validierung, Edge Cases, Mail, Jobs |
| NÜTZLICH | UI-Komponenten, Filament-Pages, Helfer |

## Test-Patterns

### A) Route/Controller (Feature)

```php
it('returns 200 for published items', function () {
    $item = Item::factory()->published()->create();
    $this->get("/items/{$item->slug}")->assertOk();
});

it('returns 404 for unpublished items', function () {
    $item = Item::factory()->unpublished()->create();
    $this->get("/items/{$item->slug}")->assertNotFound();
});

it('requires auth for admin routes', function () {
    $this->get('/admin')->assertRedirect('/login');
});
```

### B) Service/Business Logic (Unit)

```php
it('calculates tax correctly', function () {
    $service = new TaxService();
    expect($service->calculate(100, 'AT'))->toBe(120.0);
});
```

### C) Model

```php
it('has correct fillable fields', function () {
    $model = new Item();
    expect($model->getFillable())->toContain('title', 'slug');
});

it('scopes to published only', function () {
    Item::factory()->published()->count(2)->create();
    Item::factory()->unpublished()->create();
    expect(Item::published()->count())->toBe(2);
});
```

### D) Job/Queue

```php
it('dispatches notification job', function () {
    Queue::fake();
    $order->markAsPaid();
    Queue::assertPushed(SendInvoiceJob::class);
});

it('handles job chain correctly', function () {
    Queue::fake();
    ProcessPayment::withChain([SendInvoice::class])->dispatch($order);
    Queue::assertPushed(ProcessPayment::class);
});
```

### E) Livewire

```php
it('can search items', function () {
    $item = Item::factory()->create(['title' => 'Unique']);
    Livewire::test(ItemList::class)
        ->set('search', 'Unique')
        ->assertSee('Unique');
});
```

### F) Security

```php
it('prevents unauthorized access', function () {
    $user = User::factory()->create();
    $this->actingAs($user)->get('/admin/users')->assertForbidden();
});

it('validates CSRF on forms', function () {
    $this->post('/contact', ['name' => 'Test'])->assertStatus(419);
});

it('rate limits login attempts', function () {
    for ($i = 0; $i < 6; $i++) {
        $this->post('/login', ['email' => 'a@b.com', 'password' => 'wrong']);
    }
    $this->post('/login', ['email' => 'a@b.com', 'password' => 'wrong'])
        ->assertStatus(429);
});
```

### G) Filament Admin

```php
it('admin can access dashboard', function () {
    $admin = User::factory()->admin()->create();
    $this->actingAs($admin)->get('/admin')->assertOk();
});
```

## Hinweise

- **RefreshDatabase** für Feature Tests, **DatabaseTransactions** wenn schneller nötig
- **Mail::fake()**, **Queue::fake()**, **Notification::fake()** für Side-Effects
- Externe APIs (Mollie, VIES) immer mocken
- Factories mit States: `->published()`, `->admin()`, `->withTeam()`
- Ziel: min. 80% Coverage auf Auth, Payment, Business Logic
