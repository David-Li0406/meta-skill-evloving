# Widget Reference

Complete specifications for each widget type.

## Table of Contents

1. [Bar Chart](#bar-chart)
2. [Line Chart](#line-chart)
3. [Area Chart](#area-chart)
4. [Pie Chart](#pie-chart)
5. [Counter](#counter)
6. [Table](#table)
7. [Scatter Plot](#scatter-plot)
8. [Heatmap](#heatmap)
9. [Combo Chart](#combo-chart)
10. [Pivot Table](#pivot-table)
11. [Filters](#filters)
12. [Text Widget](#text-widget)
13. [Frame Structure](#frame-structure)
14. [Scale Types](#scale-types)
15. [Expression Functions](#expression-functions)

---

## Bar Chart

```json
{
  "widget": {
    "name": "b1a2c3d4",
    "queries": [{
      "name": "main_query",
      "query": {
        "datasetName": "01f0ac01",
        "fields": [
          {"name": "category", "expression": "`category_column`"},
          {"name": "value", "expression": "SUM(`value_column`)"}
        ],
        "disaggregated": false
      }
    }],
    "spec": {
      "version": 3,
      "widgetType": "bar",
      "encodings": {
        "x": {"fieldName": "category", "scale": {"type": "categorical"}, "displayName": "Category"},
        "y": {"fieldName": "value", "scale": {"type": "quantitative"}, "displayName": "Value"}
      },
      "frame": {
        "showTitle": true,
        "title": "Bar Chart Title"
      }
    }
  },
  "position": {"x": 0, "y": 0, "width": 6, "height": 4}
}
```

### With Color Grouping

```json
"encodings": {
  "x": {"fieldName": "category", "scale": {"type": "categorical"}, "displayName": "Category"},
  "y": {"fieldName": "value", "scale": {"type": "quantitative"}, "displayName": "Value"},
  "color": {"fieldName": "group", "scale": {"type": "categorical"}, "displayName": "Group"}
}
```

---

## Line Chart

```json
{
  "widget": {
    "name": "l1e2n3e4",
    "queries": [{
      "name": "main_query",
      "query": {
        "datasetName": "01f0ac02",
        "fields": [
          {"name": "date", "expression": "DATE_TRUNC('DAY', `timestamp`)"},
          {"name": "metric", "expression": "AVG(`metric_column`)"}
        ],
        "disaggregated": false
      }
    }],
    "spec": {
      "version": 3,
      "widgetType": "line",
      "encodings": {
        "x": {"fieldName": "date", "scale": {"type": "temporal"}, "displayName": "Date"},
        "y": {"fieldName": "metric", "scale": {"type": "quantitative"}, "displayName": "Metric"}
      },
      "frame": {
        "showTitle": true,
        "title": "Line Chart Title"
      }
    }
  },
  "position": {"x": 0, "y": 0, "width": 6, "height": 4}
}
```

---

## Area Chart

```json
{
  "widget": {
    "name": "a1r2e3a4",
    "queries": [{
      "name": "main_query",
      "query": {
        "datasetName": "01f0ac03",
        "fields": [
          {"name": "date", "expression": "`date`"},
          {"name": "value", "expression": "SUM(`value`)"},
          {"name": "category", "expression": "`category`"}
        ],
        "disaggregated": false
      }
    }],
    "spec": {
      "version": 3,
      "widgetType": "area",
      "encodings": {
        "x": {"fieldName": "date", "scale": {"type": "temporal"}, "displayName": "Date"},
        "y": {"fieldName": "value", "scale": {"type": "quantitative"}, "displayName": "Value"},
        "color": {"fieldName": "category", "scale": {"type": "categorical"}, "displayName": "Category"}
      },
      "frame": {
        "showTitle": true,
        "title": "Area Chart Title"
      }
    }
  },
  "position": {"x": 0, "y": 0, "width": 6, "height": 4}
}
```

---

## Pie Chart

```json
{
  "widget": {
    "name": "p1i2e3c4",
    "queries": [{
      "name": "main_query",
      "query": {
        "datasetName": "01f0ac04",
        "fields": [
          {"name": "category", "expression": "`category`"},
          {"name": "value", "expression": "SUM(`amount`)"}
        ],
        "disaggregated": false
      }
    }],
    "spec": {
      "version": 3,
      "widgetType": "pie",
      "encodings": {
        "angle": {
          "fieldName": "value",
          "displayName": "Amount",
          "scale": {"type": "quantitative"}
        },
        "color": {
          "fieldName": "category",
          "displayName": "Category",
          "scale": {"type": "categorical"}
        },
        "label": {"show": true}
      },
      "frame": {
        "showTitle": true,
        "title": "Pie Chart Title"
      }
    }
  },
  "position": {"x": 0, "y": 0, "width": 4, "height": 4}
}
```

**Note:** Pie charts use `angle` (quantitative, the measure) and `color` (categorical, the dimension) encodings, not `label`/`value`.

---

## Counter

Single value display. **Note: Counter uses spec.version 2.**

```json
{
  "widget": {
    "name": "c1d2e3f4",
    "queries": [{
      "name": "main_query",
      "query": {
        "datasetName": "01f0ab72",
        "fields": [
          {"name": "total", "expression": "SUM(`amount`)"}
        ],
        "disaggregated": false
      }
    }],
    "spec": {
      "version": 2,
      "widgetType": "counter",
      "encodings": {
        "value": {"fieldName": "total", "displayName": "Total Amount"}
      },
      "frame": {
        "title": "Total Revenue",
        "showTitle": true
      }
    }
  },
  "position": {"x": 0, "y": 0, "width": 3, "height": 2}
}
```

### Counter with Row Count

```json
"fields": [{"name": "count", "expression": "COUNT(*)"}]
```

---

## Table

**Note: Table uses spec.version 1.**

**Important:** Table widgets require complete column definitions with all required properties. Simplified column definitions will fail.

### Complete Example

```json
{
  "widget": {
    "name": "a1b2c3d4",
    "queries": [{
      "name": "main_query",
      "query": {
        "datasetName": "01f0ab72",
        "fields": [
          {"name": "id", "expression": "`id`"},
          {"name": "name", "expression": "`name`"},
          {"name": "amount", "expression": "`amount`"},
          {"name": "created_at", "expression": "`created_at`"}
        ],
        "disaggregated": true
      }
    }],
    "spec": {
      "version": 1,
      "widgetType": "table",
      "encodings": {
        "columns": [
          {
            "fieldName": "id",
            "type": "integer",
            "displayAs": "number",
            "title": "ID",
            "visible": true,
            "order": 100000,
            "alignContent": "right",
            "booleanValues": ["false", "true"],
            "allowSearch": true,
            "allowHTML": false,
            "highlightLinks": true,
            "useMonospaceFont": false,
            "preserveWhitespace": false,
            "linkOpenInNewTab": true,
            "imageUrlTemplate": "{{ @ }}",
            "imageTitleTemplate": "{{ @ }}",
            "imageWidth": "",
            "imageHeight": "",
            "linkUrlTemplate": "{{ @ }}",
            "linkTextTemplate": "{{ @ }}",
            "linkTitleTemplate": "{{ @ }}",
            "numberFormat": "0"
          },
          {
            "fieldName": "name",
            "type": "string",
            "displayAs": "string",
            "title": "Name",
            "visible": true,
            "order": 100001,
            "alignContent": "left",
            "booleanValues": ["false", "true"],
            "allowSearch": true,
            "allowHTML": false,
            "highlightLinks": true,
            "useMonospaceFont": false,
            "preserveWhitespace": false,
            "linkOpenInNewTab": true,
            "imageUrlTemplate": "{{ @ }}",
            "imageTitleTemplate": "{{ @ }}",
            "imageWidth": "",
            "imageHeight": "",
            "linkUrlTemplate": "{{ @ }}",
            "linkTextTemplate": "{{ @ }}",
            "linkTitleTemplate": "{{ @ }}"
          },
          {
            "fieldName": "amount",
            "type": "float",
            "displayAs": "number",
            "title": "Amount",
            "visible": true,
            "order": 100002,
            "alignContent": "right",
            "booleanValues": ["false", "true"],
            "allowSearch": true,
            "allowHTML": false,
            "highlightLinks": true,
            "useMonospaceFont": false,
            "preserveWhitespace": false,
            "linkOpenInNewTab": true,
            "imageUrlTemplate": "{{ @ }}",
            "imageTitleTemplate": "{{ @ }}",
            "imageWidth": "",
            "imageHeight": "",
            "linkUrlTemplate": "{{ @ }}",
            "linkTextTemplate": "{{ @ }}",
            "linkTitleTemplate": "{{ @ }}",
            "numberFormat": "0.00"
          },
          {
            "fieldName": "created_at",
            "type": "datetime",
            "displayAs": "datetime",
            "title": "Created At",
            "visible": true,
            "order": 100003,
            "alignContent": "left",
            "booleanValues": ["false", "true"],
            "allowSearch": true,
            "allowHTML": false,
            "highlightLinks": true,
            "useMonospaceFont": false,
            "preserveWhitespace": false,
            "linkOpenInNewTab": true,
            "imageUrlTemplate": "{{ @ }}",
            "imageTitleTemplate": "{{ @ }}",
            "imageWidth": "",
            "imageHeight": "",
            "linkUrlTemplate": "{{ @ }}",
            "linkTextTemplate": "{{ @ }}",
            "linkTitleTemplate": "{{ @ }}"
          }
        ]
      },
      "invisibleColumns": [],
      "allowHTMLByDefault": false,
      "itemsPerPage": 25,
      "paginationSize": "default",
      "condensed": true,
      "withRowNumber": false,
      "frame": {
        "title": "Data Table",
        "showTitle": true
      }
    }
  },
  "position": {"x": 0, "y": 0, "width": 12, "height": 6}
}
```

### Required Column Properties

Every column definition must include all of these properties:

| Property | Type | Description |
|----------|------|-------------|
| `fieldName` | string | Field name matching query field |
| `type` | string | Data type: `string`, `integer`, `float`, `datetime` |
| `displayAs` | string | Display format: `string`, `number`, `datetime` |
| `title` | string | Column header title |
| `visible` | boolean | Show/hide column |
| `order` | number | Column order (start from 100000, increment by 1) |
| `alignContent` | string | Alignment: `left`, `right`, `center` |
| `booleanValues` | array | Always `["false", "true"]` |
| `allowSearch` | boolean | Enable search (typically `true`) |
| `allowHTML` | boolean | Allow HTML rendering |
| `highlightLinks` | boolean | Highlight links (typically `true`) |
| `useMonospaceFont` | boolean | Use monospace font |
| `preserveWhitespace` | boolean | Preserve whitespace |
| `linkOpenInNewTab` | boolean | Open links in new tab (typically `true`) |
| `imageUrlTemplate` | string | Always `"{{ @ }}"` |
| `imageTitleTemplate` | string | Always `"{{ @ }}"` |
| `imageWidth` | string | Always `""` |
| `imageHeight` | string | Always `""` |
| `linkUrlTemplate` | string | Always `"{{ @ }}"` |
| `linkTextTemplate` | string | Always `"{{ @ }}"` |
| `linkTitleTemplate` | string | Always `"{{ @ }}"` |

### Numeric Type Additional Property

For `integer` and `float` types, add:

| Property | Type | Description |
|----------|------|-------------|
| `numberFormat` | string | Format: `"0"` (integer), `"0.00"` (2 decimals), `"$0.00"` (currency) |

### Required Spec-Level Properties

These properties must be included at the spec level:

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `invisibleColumns` | array | `[]` | List of hidden column field names |
| `allowHTMLByDefault` | boolean | `false` | Default HTML rendering setting |
| `itemsPerPage` | number | `25` | Rows per page |
| `paginationSize` | string | `"default"` | Pagination size |
| `condensed` | boolean | `true` | Use condensed row height |
| `withRowNumber` | boolean | `false` | Show row numbers |

### Column Templates by Type

#### String Column

```json
{
  "fieldName": "name",
  "type": "string",
  "displayAs": "string",
  "title": "Name",
  "visible": true,
  "order": 100000,
  "alignContent": "left",
  "booleanValues": ["false", "true"],
  "allowSearch": true,
  "allowHTML": false,
  "highlightLinks": true,
  "useMonospaceFont": false,
  "preserveWhitespace": false,
  "linkOpenInNewTab": true,
  "imageUrlTemplate": "{{ @ }}",
  "imageTitleTemplate": "{{ @ }}",
  "imageWidth": "",
  "imageHeight": "",
  "linkUrlTemplate": "{{ @ }}",
  "linkTextTemplate": "{{ @ }}",
  "linkTitleTemplate": "{{ @ }}"
}
```

#### Integer Column

```json
{
  "fieldName": "count",
  "type": "integer",
  "displayAs": "number",
  "title": "Count",
  "visible": true,
  "order": 100001,
  "alignContent": "right",
  "booleanValues": ["false", "true"],
  "allowSearch": true,
  "allowHTML": false,
  "highlightLinks": true,
  "useMonospaceFont": false,
  "preserveWhitespace": false,
  "linkOpenInNewTab": true,
  "imageUrlTemplate": "{{ @ }}",
  "imageTitleTemplate": "{{ @ }}",
  "imageWidth": "",
  "imageHeight": "",
  "linkUrlTemplate": "{{ @ }}",
  "linkTextTemplate": "{{ @ }}",
  "linkTitleTemplate": "{{ @ }}",
  "numberFormat": "0"
}
```

#### Float Column

```json
{
  "fieldName": "amount",
  "type": "float",
  "displayAs": "number",
  "title": "Amount",
  "visible": true,
  "order": 100002,
  "alignContent": "right",
  "booleanValues": ["false", "true"],
  "allowSearch": true,
  "allowHTML": false,
  "highlightLinks": true,
  "useMonospaceFont": false,
  "preserveWhitespace": false,
  "linkOpenInNewTab": true,
  "imageUrlTemplate": "{{ @ }}",
  "imageTitleTemplate": "{{ @ }}",
  "imageWidth": "",
  "imageHeight": "",
  "linkUrlTemplate": "{{ @ }}",
  "linkTextTemplate": "{{ @ }}",
  "linkTitleTemplate": "{{ @ }}",
  "numberFormat": "0.00"
}
```

#### Datetime Column

```json
{
  "fieldName": "created_at",
  "type": "datetime",
  "displayAs": "datetime",
  "title": "Created At",
  "visible": true,
  "order": 100003,
  "alignContent": "left",
  "booleanValues": ["false", "true"],
  "allowSearch": true,
  "allowHTML": false,
  "highlightLinks": true,
  "useMonospaceFont": false,
  "preserveWhitespace": false,
  "linkOpenInNewTab": true,
  "imageUrlTemplate": "{{ @ }}",
  "imageTitleTemplate": "{{ @ }}",
  "imageWidth": "",
  "imageHeight": "",
  "linkUrlTemplate": "{{ @ }}",
  "linkTextTemplate": "{{ @ }}",
  "linkTitleTemplate": "{{ @ }}"
}
```

### Table with Conditional Formatting

```json
{
  "fieldName": "status",
  "type": "string",
  "displayAs": "string",
  "title": "Status",
  "visible": true,
  "order": 100004,
  "alignContent": "left",
  "booleanValues": ["false", "true"],
  "allowSearch": true,
  "allowHTML": false,
  "highlightLinks": true,
  "useMonospaceFont": false,
  "preserveWhitespace": false,
  "linkOpenInNewTab": true,
  "imageUrlTemplate": "{{ @ }}",
  "imageTitleTemplate": "{{ @ }}",
  "imageWidth": "",
  "imageHeight": "",
  "linkUrlTemplate": "{{ @ }}",
  "linkTextTemplate": "{{ @ }}",
  "linkTitleTemplate": "{{ @ }}",
  "colorMode": "text",
  "conditions": [
    {"condition": {"operator": "=", "value": "SUCCESS"}, "color": "#00A972"},
    {"condition": {"operator": "=", "value": "FAILED"}, "color": "#FF3621"}
  ]
}
```

---

## Scatter Plot

```json
{
  "widget": {
    "name": "s1c2a3t4",
    "queries": [{
      "name": "main_query",
      "query": {
        "datasetName": "01f0ac05",
        "fields": [
          {"name": "x_val", "expression": "`metric_x`"},
          {"name": "y_val", "expression": "`metric_y`"},
          {"name": "category", "expression": "`category`"}
        ],
        "disaggregated": true
      }
    }],
    "spec": {
      "version": 3,
      "widgetType": "scatter",
      "encodings": {
        "x": {"fieldName": "x_val", "scale": {"type": "quantitative"}, "displayName": "Metric X"},
        "y": {"fieldName": "y_val", "scale": {"type": "quantitative"}, "displayName": "Metric Y"},
        "color": {"fieldName": "category", "scale": {"type": "categorical"}, "displayName": "Category"}
      },
      "frame": {
        "showTitle": true,
        "title": "Scatter Plot Title"
      }
    }
  },
  "position": {"x": 0, "y": 0, "width": 6, "height": 4}
}
```

---

## Heatmap

```json
{
  "widget": {
    "name": "h1e2a3t4",
    "queries": [{
      "name": "main_query",
      "query": {
        "datasetName": "01f0ac06",
        "fields": [
          {"name": "x_dim", "expression": "`dimension_x`"},
          {"name": "y_dim", "expression": "`dimension_y`"},
          {"name": "intensity", "expression": "SUM(`value`)"}
        ],
        "disaggregated": false
      }
    }],
    "spec": {
      "version": 3,
      "widgetType": "heatmap",
      "encodings": {
        "x": {"fieldName": "x_dim", "scale": {"type": "categorical"}, "displayName": "X Dimension"},
        "y": {"fieldName": "y_dim", "scale": {"type": "categorical"}, "displayName": "Y Dimension"},
        "color": {"fieldName": "intensity", "scale": {"type": "quantitative"}, "displayName": "Intensity"}
      },
      "frame": {
        "showTitle": true,
        "title": "Heatmap Title"
      }
    }
  },
  "position": {"x": 0, "y": 0, "width": 6, "height": 4}
}
```

---

## Combo Chart

Bar and line on the same chart:

```json
{
  "widget": {
    "name": "c1o2m3b4",
    "queries": [{
      "name": "main_query",
      "query": {
        "datasetName": "01f0ac07",
        "fields": [
          {"name": "month", "expression": "`month`"},
          {"name": "revenue", "expression": "SUM(`revenue`)"},
          {"name": "growth_rate", "expression": "AVG(`growth_rate`)"}
        ],
        "disaggregated": false
      }
    }],
    "spec": {
      "version": 3,
      "widgetType": "combo",
      "encodings": {
        "x": {"fieldName": "month", "scale": {"type": "categorical"}, "displayName": "Month"},
        "y": {"fieldName": "revenue", "scale": {"type": "quantitative"}, "displayName": "Revenue", "seriesType": "bar"},
        "y2": {"fieldName": "growth_rate", "scale": {"type": "quantitative"}, "displayName": "Growth Rate", "seriesType": "line"}
      },
      "frame": {
        "showTitle": true,
        "title": "Combo Chart Title"
      }
    }
  },
  "position": {"x": 0, "y": 0, "width": 6, "height": 4}
}
```

---

## Pivot Table

```json
{
  "widget": {
    "name": "p1v2o3t4",
    "queries": [{
      "name": "main_query",
      "query": {
        "datasetName": "01f0ac08",
        "fields": [
          {"name": "row_dim", "expression": "`category`"},
          {"name": "col_dim", "expression": "`region`"},
          {"name": "measure", "expression": "SUM(`sales`)"}
        ],
        "disaggregated": false
      }
    }],
    "spec": {
      "version": 3,
      "widgetType": "pivot",
      "encodings": {
        "rows": [{"fieldName": "row_dim", "displayName": "Category"}],
        "columns": [{"fieldName": "col_dim", "displayName": "Region"}],
        "values": [{"fieldName": "measure", "displayName": "Sales"}]
      },
      "frame": {
        "showTitle": true,
        "title": "Pivot Table Title"
      }
    }
  },
  "position": {"x": 0, "y": 0, "width": 8, "height": 5}
}
```

---

## Filters

**Note: All filter widgets use spec.version 2.**

### Date Range Picker

```json
{
  "widget": {
    "name": "f1d2r3p4",
    "queries": [{
      "name": "parameter_dashboards/01f0a403a6891cc1b5cf06c4960354b8/datasets/01f0ac09065f117db5bbc92371902e19_param_date",
      "query": {
        "datasetName": "01f0ac09",
        "fields": [{"name": "date", "expression": "`date_column`"}],
        "disaggregated": true
      }
    }],
    "spec": {
      "version": 2,
      "widgetType": "filter-date-range-picker",
      "encodings": {
        "fields": {"fieldName": "date", "displayName": "Date Range"}
      }
    }
  },
  "position": {"x": 0, "y": 0, "width": 3, "height": 1}
}
```

### Multi-Select Filter

```json
{
  "widget": {
    "name": "f1m2s3f4",
    "queries": [{
      "name": "parameter_dashboards/01f0a403a6891cc1b5cf06c4960354b8/datasets/01f0ac0a065f117db5bbc92371902e20_param_category",
      "query": {
        "datasetName": "01f0ac0a",
        "fields": [{"name": "category", "expression": "`category`"}],
        "disaggregated": true
      }
    }],
    "spec": {
      "version": 2,
      "widgetType": "filter-multi-select",
      "encodings": {
        "fields": {"fieldName": "category", "displayName": "Category"}
      }
    }
  },
  "position": {"x": 3, "y": 0, "width": 3, "height": 1}
}
```

### Single-Select Filter

Single-select filters allow selecting one value to filter other widgets. They can have multiple queries: one for the options list and parameter queries to apply the filter to other datasets.

```json
{
  "widget": {
    "name": "81999930",
    "queries": [
      {
        "name": "dashboards/{dashboard_id}/datasets/{dataset_id}_time_key",
        "query": {
          "datasetName": "select_time_key_overview",
          "fields": [
            {"name": "time_key", "expression": "`time_key`"},
            {"name": "time_key_associativity", "expression": "COUNT_IF(`associative_filter_predicate_group`)"}
          ],
          "disaggregated": false
        }
      },
      {
        "name": "parameter_dashboards/{dashboard_id}/datasets/{dataset_id}_param_time_key",
        "query": {
          "datasetName": "dd0ba138",
          "parameters": [
            {"name": "param_time_key", "keyword": "param_time_key"}
          ],
          "disaggregated": false
        }
      }
    ],
    "spec": {
      "version": 2,
      "widgetType": "filter-single-select",
      "encodings": {
        "fields": [
          {
            "fieldName": "time_key",
            "queryName": "dashboards/{dashboard_id}/datasets/{dataset_id}_time_key"
          },
          {
            "parameterName": "param_time_key",
            "queryName": "parameter_dashboards/{dashboard_id}/datasets/{dataset_id}_param_time_key"
          }
        ]
      },
      "frame": {
        "showTitle": true,
        "title": "View date by"
      },
      "selection": {
        "defaultSelection": {
          "values": {
            "dataType": "STRING",
            "values": [{"value": "Week"}]
          }
        }
      }
    }
  },
  "position": {"x": 0, "y": 3, "width": 3, "height": 1}
}
```

**Key points:**
- First query: provides the options list (with optional associativity count)
- Parameter queries: apply the selected value to other datasets via `parameters`
- `encodings.fields`: link field/parameter names to their query names
- `selection.defaultSelection`: sets the initial selected value

---

## Text Widget

Markdown-enabled text display:

```json
{
  "widget": {
    "name": "t1e2x3t4",
    "multilineTextboxSpec": {
      "lines": [
        "# Dashboard Title",
        "",
        "**Description:** This dashboard shows key metrics.",
        "",
        "- Item 1",
        "- Item 2"
      ]
    }
  },
  "position": {"x": 0, "y": 0, "width": 12, "height": 2}
}
```

**Note:** Use `multilineTextboxSpec` with `lines` array. Each element represents a line of markdown content.

---

## Frame Structure

Widget title and description configuration.

**Important:** `title` and `showTitle: true` are practically required. Widgets without titles make it difficult to understand their content and severely degrade dashboard readability.

```json
"frame": {
  "showTitle": true,
  "title": "Widget Title",
  "showDescription": true,
  "description": "Optional description text displayed below the title."
}
```

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `showTitle` | boolean | **Yes** | Always set to `true` |
| `title` | string | **Yes** | Title describing widget content |
| `showDescription` | boolean | No | Show/hide the description |
| `description` | string | No | Description text (displayed below title) |

---

## Scale Types

| Scale Type | Use For |
|------------|---------|
| `quantitative` | Numeric measures (sums, averages, counts) |
| `categorical` | Discrete categories (names, IDs) |
| `temporal` | Dates and timestamps |

---

## Expression Functions

Common SQL expressions for fields:

| Function | Example |
|----------|---------|
| Direct reference | `` `column_name` `` |
| Sum | `SUM(\`amount\`)` |
| Count | `COUNT(*)` |
| Average | `AVG(\`value\`)` |
| Min/Max | `MIN(\`date\`)`, `MAX(\`date\`)` |
| Date truncate | `DATE_TRUNC('DAY', \`timestamp\`)` |
| Conditional | `CASE WHEN \`status\` = 'A' THEN 1 ELSE 0 END` |
