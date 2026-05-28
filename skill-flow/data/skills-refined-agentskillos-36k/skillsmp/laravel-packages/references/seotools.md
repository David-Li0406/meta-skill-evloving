# SEOTools Advanced

## Sitemap Generation

```php
// routes/web.php
use Spatie\Sitemap\Sitemap;
use Spatie\Sitemap\Tags\Url;

Route::get('/sitemap.xml', function () {
    $sitemap = Sitemap::create();

    // Static pages
    $sitemap->add(Url::create('/')->setPriority(1.0));
    $sitemap->add(Url::create('/about')->setPriority(0.8));
    $sitemap->add(Url::create('/contact')->setPriority(0.7));

    // Dynamic pages
    Product::all()->each(function (Product $product) use ($sitemap) {
        $sitemap->add(
            Url::create("/products/{$product->slug}")
                ->setLastModificationDate($product->updated_at)
                ->setPriority(0.9)
        );
    });

    return $sitemap->toResponse(request());
});
```

## Canonical URLs

```php
use Artesaos\SEOTools\Facades\SEOMeta;

// Set canonical URL
SEOMeta::setCanonical(url()->current());

// For paginated content
SEOMeta::setCanonical(url()->current() . '?page=' . request('page', 1));

// With query string filtering
SEOMeta::setCanonical(
    url()->current() . '?' . http_build_query(request()->only(['category', 'sort']))
);
```

## Multilingual SEO

```php
use Artesaos\SEOTools\Facades\SEOMeta;
use Artesaos\SEOTools\Facades\OpenGraph;

public function show(Product $product)
{
    $locale = app()->getLocale();

    SEOMeta::setTitle($product->getTranslation('name', $locale));
    SEOMeta::setDescription($product->getTranslation('description', $locale));

    // Alternate language links
    foreach (['en', 'tr', 'de'] as $lang) {
        SEOMeta::addAlternateLanguage($lang, route('products.show', [
            'product' => $product,
            'locale' => $lang,
        ]));
    }

    OpenGraph::setLocale($locale);
}
```

## E-commerce Schema

```php
use Artesaos\SEOTools\Facades\JsonLd;

public function show(Product $product)
{
    JsonLd::setType('Product');
    JsonLd::setTitle($product->name);
    JsonLd::setDescription($product->description);
    JsonLd::addImage($product->image_url);
    JsonLd::addValue('sku', $product->sku);
    JsonLd::addValue('brand', [
        '@type' => 'Brand',
        'name' => $product->brand->name,
    ]);
    JsonLd::addValue('offers', [
        '@type' => 'Offer',
        'url' => url()->current(),
        'price' => $product->price,
        'priceCurrency' => 'GBP',
        'availability' => $product->in_stock 
            ? 'https://schema.org/InStock' 
            : 'https://schema.org/OutOfStock',
        'seller' => [
            '@type' => 'Organization',
            'name' => config('app.name'),
        ],
    ]);

    // Reviews
    if ($product->reviews_count > 0) {
        JsonLd::addValue('aggregateRating', [
            '@type' => 'AggregateRating',
            'ratingValue' => $product->average_rating,
            'reviewCount' => $product->reviews_count,
        ]);
    }
}
```

## Organization Schema

```php
// In layout or home page
JsonLd::setType('Organization');
JsonLd::setTitle(config('app.name'));
JsonLd::addValue('url', config('app.url'));
JsonLd::addValue('logo', asset('images/logo.png'));
JsonLd::addValue('contactPoint', [
    '@type' => 'ContactPoint',
    'telephone' => '+44-xxx-xxx-xxxx',
    'contactType' => 'customer service',
]);
JsonLd::addValue('sameAs', [
    'https://twitter.com/mysite',
    'https://facebook.com/mysite',
]);
```

## Robots Meta

```php
// Allow indexing
SEOMeta::setRobots('index,follow');

// Prevent indexing (admin, search results, etc.)
SEOMeta::setRobots('noindex,nofollow');

// Index but don't follow links
SEOMeta::setRobots('index,nofollow');
```

## Middleware for Default SEO

```php
<?php

namespace App\Http\Middleware;

use Artesaos\SEOTools\Facades\SEOTools;
use Closure;
use Illuminate\Http\Request;

class SetDefaultSeo
{
    public function handle(Request $request, Closure $next)
    {
        SEOTools::setTitle(config('app.name'));
        SEOTools::setDescription(config('seo.default_description'));
        SEOTools::opengraph()->setUrl($request->url());
        SEOTools::opengraph()->addProperty('site_name', config('app.name'));
        SEOTools::twitter()->setSite('@mysite');

        return $next($request);
    }
}
```
