# Data Extraction Example

## Use Case
Scraping structured data from web pages.

## Task Setup

```
TaskName: "Extracting Product Listings"

Task: Navigate to https://shop.example.com/products and extract product data:
1. Wait for all product cards to load completely
2. For each product card visible on the first page, extract:
   - Product name
   - Price
   - Rating (if available)
   - Availability status (In Stock / Out of Stock)
   - Image URL
3. Return a structured list of all products with this information
4. Include total count of products found

RecordingName: product_data_scrape
```

## Expected Return

```json
{
  "totalProducts": 12,
  "products": [
    {
      "name": "Wireless Headphones",
      "price": "$79.99",
      "rating": "4.5/5",
      "availability": "In Stock",
      "imageUrl": "https://shop.example.com/images/headphones.jpg"
    },
    {
      "name": "Smart Watch",
      "price": "$199.99",
      "rating": "4.8/5",
      "availability": "In Stock",
      "imageUrl": "https://shop.example.com/images/watch.jpg"
    }
    // ... more products
  ],
  "scrapedAt": "2024-01-15T10:30:00Z"
}
```

## Variations

### Pagination Handling
```
Task: Scrape product listings across multiple pages:
1. Extract products from page 1
2. Click "Next" to go to page 2
3. Extract products from page 2
4. Continue until "Next" button is disabled or page 5 is reached
5. Return combined list of all products from all pages
```

### Table Data Extraction
```
Task: Navigate to the data table at https://example.com/reports/sales, 
extract all visible rows with columns: Date, Product, Quantity, Revenue. 
Sort by Revenue descending and return the top 10 entries.
```

### Nested Content Extraction
```
Task: On the blog listing page:
1. Extract titles and excerpts from all blog post cards
2. For each of the first 3 posts, click through to the full post
3. Extract the full article content and publish date
4. Return back to listing and repeat for next posts
5. Return structured data with titles, excerpts, full content, and dates
```

### Dynamic Content Scraping
```
Task: Navigate to the infinite-scroll page, scroll down to load more 
content 5 times (waiting for new items after each scroll), then extract 
all product titles and prices from the entire loaded content.
```

### Comparative Data Extraction
```
Task: Extract pricing data from competitor sites:
1. Visit https://shop-a.example.com/product/widget
2. Extract product name and price
3. Visit https://shop-b.example.com/product/widget
4. Extract product name and price
5. Visit https://shop-c.example.com/product/widget
6. Extract product name and price
7. Return comparison table of all three
```

## Best Practices for Extraction

### Handle Missing Data
```
For each product, attempt to extract rating. If rating is not present 
or visible, record it as "N/A" rather than failing the entire extraction.
```

### Verify Data Quality
```
After extracting all products, verify that:
- No product names are empty
- All prices are in valid currency format
- Count matches expected number of items on page
Return data quality summary along with extracted data.
```

### Efficient Selectors
```
Products are in a grid with class "product-grid". Each product card has 
class "product-card". Within each card:
- Title is in h3.product-title
- Price is in span.product-price
- Rating is in div.product-rating
Use these specific selectors for faster extraction.
```

## Common Extraction Patterns

### List/Grid Items
```
Extract all items from the grid layout, including title, image, and 
metadata from each card.
```

### Structured Tables
```
Extract table data row by row, mapping column headers to values.
```

### Article Content
```
Extract main heading, author, publish date, and full article body text.
```

### Search Results
```
Extract result titles, URLs, descriptions, and metadata from search 
results page.
```

### Review Data
```
Extract reviews including reviewer name, rating, date, and review text.
```
