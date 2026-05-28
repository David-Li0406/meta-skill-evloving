# htmx Server-Side Patterns

## Core Principle

htmx servers return **HTML fragments**, not JSON. The server renders HTML that gets swapped directly into the DOM.

## Detecting htmx Requests

### Python (Flask)

```python
from flask import request, render_template

@app.route('/items')
def get_items():
    items = Item.query.all()

    if request.headers.get('HX-Request'):
        # htmx request - return partial
        return render_template('_items_list.html', items=items)
    else:
        # Regular request - return full page
        return render_template('items.html', items=items)
```

### Python (Django)

```python
from django.shortcuts import render

def items_view(request):
    items = Item.objects.all()

    if request.headers.get('HX-Request'):
        return render(request, 'partials/_items_list.html', {'items': items})
    else:
        return render(request, 'items.html', {'items': items})
```

### JavaScript (Express)

```javascript
app.get('/items', (req, res) => {
  const items = getItems();

  if (req.headers['hx-request']) {
    res.render('partials/items-list', { items });
  } else {
    res.render('items', { items });
  }
});
```

### Ruby (Rails)

```ruby
def index
  @items = Item.all

  if request.headers['HX-Request']
    render partial: 'items/list', locals: { items: @items }
  else
    render :index
  end
end
```

### Go (net/http)

```go
func itemsHandler(w http.ResponseWriter, r *http.Request) {
    items := getItems()

    if r.Header.Get("HX-Request") == "true" {
        tmpl.ExecuteTemplate(w, "_items_list.html", items)
    } else {
        tmpl.ExecuteTemplate(w, "items.html", items)
    }
}
```

## Response Headers

### Triggering Client Events

```python
from flask import make_response

@app.route('/items', methods=['POST'])
def create_item():
    item = create_new_item(request.form)

    response = make_response(render_template('_item.html', item=item))
    response.headers['HX-Trigger'] = 'itemCreated'
    return response
```

With data:

```python
import json

response.headers['HX-Trigger'] = json.dumps({
    'itemCreated': {'id': item.id, 'name': item.name}
})
```

### Client-Side Redirect

```python
@app.route('/login', methods=['POST'])
def login():
    if authenticate(request.form):
        response = make_response()
        response.headers['HX-Redirect'] = '/dashboard'
        return response
    return render_template('_login_error.html'), 401
```

### Override Swap Behavior

```python
@app.route('/submit', methods=['POST'])
def submit():
    response = make_response(render_template('_success.html'))
    response.headers['HX-Retarget'] = '#notifications'
    response.headers['HX-Reswap'] = 'beforeend'
    return response
```

### Push URL to History

```python
@app.route('/items/<int:id>')
def get_item(id):
    item = Item.query.get_or_404(id)

    response = make_response(render_template('_item_detail.html', item=item))
    response.headers['HX-Push-Url'] = f'/items/{id}'
    return response
```

## Out-of-Band Updates

Update multiple elements with a single response:

```html
<!-- _create_item_response.html -->

<!-- Main content goes to hx-target -->
<tr id="item-{{ item.id }}">
    <td>{{ item.name }}</td>
    <td>{{ item.price }}</td>
</tr>

<!-- OOB updates go to elements matching their id -->
<span id="item-count" hx-swap-oob="true">{{ total_items }}</span>
<div id="notification" hx-swap-oob="true">
    Item "{{ item.name }}" created!
</div>
```

### OOB Swap Strategies

```html
<!-- Replace content -->
<div id="target" hx-swap-oob="true">New content</div>

<!-- Append to element -->
<div id="target" hx-swap-oob="beforeend">Appended content</div>

<!-- Delete element -->
<div id="target" hx-swap-oob="delete"></div>
```

## Error Handling

### Return Appropriate Status Codes

```python
@app.route('/items', methods=['POST'])
def create_item():
    try:
        item = create_new_item(request.form)
        return render_template('_item.html', item=item), 201
    except ValidationError as e:
        return render_template('_form_errors.html', errors=e.messages), 422
    except Exception as e:
        return render_template('_error.html', message=str(e)), 500
```

### Client-Side Error Handling

Configure htmx to swap on error responses:

```javascript
htmx.config.responseHandling = [
    {code:"204", swap: false},
    {code:"[23]..", swap: true},
    {code:"422", swap: true, error: false, target: "#errors"},
    {code:"[45]..", swap: true, error: true}
];
```

## Validation Patterns

### Inline Validation

```python
@app.route('/validate/email', methods=['POST'])
def validate_email():
    email = request.form.get('email')

    if not email:
        return '<span class="error">Email is required</span>'
    if not is_valid_email(email):
        return '<span class="error">Invalid email format</span>'
    if email_exists(email):
        return '<span class="error">Email already registered</span>'

    return '<span class="success">Email available</span>'
```

HTML:

```html
<input type="email" name="email"
       hx-post="/validate/email"
       hx-trigger="blur changed"
       hx-target="next .validation">
<span class="validation"></span>
```

### Form Validation Response

```python
@app.route('/submit', methods=['POST'])
def submit_form():
    errors = validate_form(request.form)

    if errors:
        return render_template('_form.html',
                               data=request.form,
                               errors=errors), 422

    # Process valid submission
    return render_template('_success.html')
```

## Partial Templates

### Template Organization

```
templates/
├── base.html
├── items/
│   ├── index.html          # Full page
│   └── partials/
│       ├── _list.html      # Items list partial
│       ├── _item.html      # Single item row
│       ├── _form.html      # Item form
│       └── _detail.html    # Item detail view
```

### Jinja2 Example

`_item.html`:

```html
<tr id="item-{{ item.id }}">
    <td>{{ item.name }}</td>
    <td>{{ item.price | currency }}</td>
    <td>
        <button hx-get="/items/{{ item.id }}/edit"
                hx-target="closest tr"
                hx-swap="outerHTML">
            Edit
        </button>
        <button hx-delete="/items/{{ item.id }}"
                hx-target="closest tr"
                hx-swap="outerHTML"
                hx-confirm="Delete this item?">
            Delete
        </button>
    </td>
</tr>
```

`_list.html`:

```html
<table id="items-table">
    <thead>
        <tr>
            <th>Name</th>
            <th>Price</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for item in items %}
            {% include 'items/partials/_item.html' %}
        {% endfor %}
    </tbody>
</table>
```

## CSRF Protection

### Django

```html
<body hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
```

### Flask-WTF

```html
<body hx-headers='{"X-CSRF-Token": "{{ csrf_token() }}"}'>
```

### Rails

```erb
<body hx-headers='{"X-CSRF-Token": "<%= form_authenticity_token %>"}'>
```

### Express (csurf)

```html
<body hx-headers='{"X-CSRF-Token": "{{csrfToken}}"}'>
```

## Pagination

### Load More Pattern

```python
@app.route('/items')
def get_items():
    page = request.args.get('page', 1, type=int)
    items = Item.query.paginate(page=page, per_page=20)

    return render_template('_items_page.html',
                           items=items.items,
                           has_next=items.has_next,
                           next_page=page + 1)
```

`_items_page.html`:

```html
{% for item in items %}
<div class="item">{{ item.name }}</div>
{% endfor %}

{% if has_next %}
<div hx-get="/items?page={{ next_page }}"
     hx-trigger="revealed"
     hx-swap="outerHTML">
    Loading more...
</div>
{% endif %}
```

## Search with Debounce

```python
@app.route('/search')
def search():
    q = request.args.get('q', '')
    results = Item.query.filter(Item.name.ilike(f'%{q}%')).limit(20).all()
    return render_template('_search_results.html', results=results, query=q)
```

HTML:

```html
<input type="search" name="q"
       hx-get="/search"
       hx-trigger="input changed delay:300ms, search"
       hx-target="#results"
       hx-indicator="#search-spinner">
<span id="search-spinner" class="htmx-indicator">Searching...</span>
<div id="results"></div>
```

## WebSocket/SSE Integration

For real-time updates, combine htmx with SSE extension:

```html
<div hx-ext="sse" sse-connect="/events" sse-swap="message">
    <!-- Content updated via SSE -->
</div>
```

Server (Python/Flask):

```python
from flask import Response

@app.route('/events')
def events():
    def generate():
        while True:
            # Get new data
            data = get_latest_data()
            yield f'data: {render_template("_update.html", data=data)}\n\n'
            time.sleep(1)

    return Response(generate(), mimetype='text/event-stream')
```
