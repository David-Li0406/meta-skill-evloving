# Dashboard Examples

Complete dashboard examples for common use cases.

## Table of Contents

1. [Retail Revenue & Supply Chain Dashboard](#retail-dashboard)
2. [NYC Taxi Trip Analysis Dashboard](#nyc-taxi-trip-analysis-dashboard)

---

## Retail Revenue & Supply Chain Dashboard

```json
{
  "datasets": [
    {
      "name": "1bb727fb",
      "displayName": "Orders and Customers",
      "queryLines": [
        "SELECT\n",
        "  o_orderdate,\n",
        "  o_custkey\n",
        "FROM\n",
        "  `samples`.`tpch`.`orders`"
      ]
    },
    {
      "name": "3530ec9c",
      "displayName": "Orders vs Returns",
      "queryLines": [
        "SELECT\n",
        "    l_shipdate,\n",
        "    l_suppkey,\n",
        "    COUNT(*) AS total_orders,\n",
        "    SUM(CASE WHEN l_returnflag = 'R' THEN 1 ELSE 0 END) AS return_count\n",
        "FROM\n",
        "    samples.tpch.lineitem\n",
        "GROUP BY\n",
        "    l_shipdate,\n",
        "    l_suppkey\n",
        "ORDER BY\n",
        "    l_shipdate;"
      ]
    },
    {
      "name": "3b52879a",
      "displayName": "Overall Supplier Count",
      "queryLines": [
        "SELECT\n",
        "  COUNT(distinct(s_suppkey)) AS num_suppliers\n",
        "FROM\n",
        "  `samples`.`tpch`.`supplier`"
      ]
    },
    {
      "name": "a91573ca",
      "displayName": "Order count by priority and ship mode",
      "queryLines": [
        "SELECT\n",
        "    o.o_orderpriority AS priority,\n",
        "    l.l_shipmode AS ship_mode,\n",
        "    COUNT(*) AS order_count,\n",
        "    o.o_orderdate\n",
        "FROM\n",
        "    samples.tpch.orders AS o\n",
        "JOIN\n",
        "    samples.tpch.lineitem AS l\n",
        "ON\n",
        "    o.o_orderkey = l.l_orderkey\n",
        "GROUP BY\n",
        "    o.o_orderpriority,\n",
        "    l.l_shipmode,\n",
        "    o.o_orderdate\n",
        "ORDER BY\n",
        "    priority,\n",
        "    ship_mode;"
      ]
    },
    {
      "name": "ced91012",
      "displayName": "Revenue Trends by Nation",
      "queryLines": [
        "SELECT\n",
        "    o_orderdate,\n",
        "    n_name AS nation,\n",
        "    sum(l_extendedprice * (1 - l_discount) * (((length(n_name))/100) + (year(o_orderdate)-1993)/100)) AS revenue\n",
        "FROM\n",
        "    `samples`.`tpch`.`customer`,\n",
        "    `samples`.`tpch`.`orders`,\n",
        "    `samples`.`tpch`.`lineitem`,\n",
        "    `samples`.`tpch`.`nation`\n",
        "WHERE\n",
        "    c_custkey = o_custkey\n",
        "    AND l_orderkey = o_orderkey\n",
        "    AND c_nationkey = n_nationkey\n",
        "    AND n_name in ('ARGENTINA', 'UNITED KINGDOM', 'FRANCE', 'BRAZIL', 'CHINA', 'UNITED STATES', 'JAPAN', 'JORDAN')\n",
        "GROUP BY\n",
        "    o_orderdate,\n",
        "    nation\n",
        "ORDER BY\n",
        "    nation ASC,\n",
        "    o_orderdate ASC;"
      ]
    },
    {
      "name": "e7a62da2",
      "displayName": "Revenue by Order Priority",
      "queryLines": [
        "SELECT\n",
        "  o_orderdate AS Date,\n",
        "  o_orderpriority AS Priority,\n",
        "  sum(o_totalprice) AS `Total Price`\n",
        "FROM\n",
        "  `samples`.`tpch`.`orders`\n",
        "WHERE\n",
        "  o_orderdate > '1994-01-01'\n",
        "  AND o_orderdate < '1994-01-31'\n",
        "GROUP BY\n",
        "  1,\n",
        "  2\n",
        "ORDER BY\n",
        "  1,\n",
        "  2"
      ]
    },
    {
      "name": "ee8e48ce",
      "displayName": "Most Valuable Customers",
      "queryLines": [
        "SELECT\n",
        "  revenue_per_customer.customer_id AS `Customer ID #`,\n",
        "  customers.c_mktsegment AS `Customer Segment`,\n",
        "  concat(\n",
        "    '<div style=\"background-color:#',\n",
        "    CASE\n",
        "      WHEN revenue_per_customer.total_revenue BETWEEN 0 AND 1500000 THEN '88BFE0'\n",
        "      WHEN revenue_per_customer.total_revenue BETWEEN 1500001 AND 3000000 THEN 'FCED9F'\n",
        "      WHEN revenue_per_customer.total_revenue BETWEEN 3000001 AND 5000000 THEN 'ED9A93'\n",
        "      ELSE 'CACFD3'\n",
        "    END,\n",
        "    '; text-align:center;\"> $',\n",
        "    format_number(revenue_per_customer.total_revenue, 0),\n",
        "    '</div>'\n",
        "  ) AS `Total Customer Revenue`\n",
        "FROM\n",
        "  (\n",
        "    SELECT\n",
        "      o_custkey AS customer_id,\n",
        "      sum(o_totalprice) AS total_revenue\n",
        "    FROM\n",
        "      `samples`.`tpch`.`orders`\n",
        "    GROUP BY\n",
        "      1\n",
        "    HAVING\n",
        "      total_revenue > 0\n",
        "  ) AS revenue_per_customer\n",
        "JOIN `samples`.`tpch`.`customer` AS customers\n",
        "  ON revenue_per_customer.customer_id = customers.c_custkey\n",
        "JOIN `samples`.`tpch`.`region` AS region\n",
        "  ON customers.c_nationkey = region.r_regionkey\n",
        "ORDER BY\n",
        "  revenue_per_customer.customer_id\n",
        "LIMIT\n",
        "  400"
      ]
    }
  ],
  "pages": [
    {
      "name": "e04b37dc",
      "displayName": "Summary",
      "layout": [
        {
          "widget": {
            "name": "0387035e",
            "queries": [
              {
                "name": "main_query",
                "query": {
                  "datasetName": "3530ec9c",
                  "fields": [
                    {
                      "name": "countdistinct(l_suppkey)",
                      "expression": "COUNT(DISTINCT `l_suppkey`)"
                    }
                  ],
                  "disaggregated": false
                }
              }
            ],
            "spec": {
              "encodings": {
                "value": {
                  "displayName": "Count of Unique l_suppkey",
                  "fieldName": "countdistinct(l_suppkey)"
                }
              },
              "frame": {
                "description": "Unique Suppliers",
                "showDescription": false,
                "showTitle": true,
                "title": "Unique Suppliers"
              },
              "version": 2,
              "widgetType": "counter"
            }
          },
          "position": {
            "x": 1,
            "y": 2,
            "width": 1,
            "height": 2
          }
        },
        {
          "widget": {
            "name": "08bf1423",
            "queries": [
              {
                "name": "main_query",
                "query": {
                  "datasetName": "1bb727fb",
                  "fields": [
                    {
                      "name": "countdistinct(o_custkey)",
                      "expression": "COUNT(DISTINCT `o_custkey`)"
                    }
                  ],
                  "disaggregated": false
                }
              }
            ],
            "spec": {
              "encodings": {
                "value": {
                  "displayName": "Count of Unique o_custkey",
                  "fieldName": "countdistinct(o_custkey)"
                }
              },
              "frame": {
                "description": "Unique Customers",
                "showDescription": false,
                "showTitle": true,
                "title": "Unique Customers"
              },
              "version": 2,
              "widgetType": "counter"
            }
          },
          "position": {
            "x": 0,
            "y": 2,
            "width": 1,
            "height": 2
          }
        },
        {
          "widget": {
            "name": "2185ae62",
            "queries": [
              {
                "name": "main_query",
                "query": {
                  "datasetName": "e7a62da2",
                  "fields": [
                    {
                      "name": "Priority",
                      "expression": "`Priority`"
                    },
                    {
                      "name": "sum(Total Price)",
                      "expression": "SUM(`Total Price`)"
                    }
                  ],
                  "disaggregated": false
                }
              }
            ],
            "spec": {
              "encodings": {
                "angle": {
                  "displayName": "Associated Revenue",
                  "fieldName": "sum(Total Price)",
                  "scale": {
                    "type": "quantitative"
                  }
                },
                "color": {
                  "displayName": "Order Priority",
                  "fieldName": "Priority",
                  "scale": {
                    "mappings": [
                      {
                        "color": "#B9486F",
                        "value": "5-LOW"
                      },
                      {
                        "color": "#FFBF73",
                        "value": "4-NOT SPECIFIED"
                      },
                      {
                        "color": "#FFEC93",
                        "value": "3-MEDIUM"
                      },
                      {
                        "color": "#C8CFD3",
                        "value": "2-HIGH"
                      },
                      {
                        "color": "#6B819C",
                        "value": "1-URGENT"
                      }
                    ],
                    "type": "categorical"
                  }
                },
                "label": {
                  "show": true
                }
              },
              "frame": {
                "description": "All Time",
                "showDescription": true,
                "showTitle": true,
                "title": "Revenue by Order Priority"
              },
              "version": 3,
              "widgetType": "pie"
            }
          },
          "position": {
            "x": 0,
            "y": 12,
            "width": 2,
            "height": 6
          }
        },
        {
          "widget": {
            "name": "2f27af07",
            "queries": [
              {
                "name": "main_query",
                "query": {
                  "datasetName": "ee8e48ce",
                  "fields": [
                    {
                      "name": "Customer ID #",
                      "expression": "`Customer ID #`"
                    },
                    {
                      "name": "Customer Segment",
                      "expression": "`Customer Segment`"
                    },
                    {
                      "name": "Total Customer Revenue",
                      "expression": "`Total Customer Revenue`"
                    }
                  ],
                  "disaggregated": true
                }
              }
            ],
            "spec": {
              "allowHTMLByDefault": true,
              "condensed": false,
              "encodings": {
                "columns": [
                  {
                    "alignContent": "right",
                    "allowHTML": true,
                    "allowSearch": false,
                    "booleanValues": [
                      "false",
                      "true"
                    ],
                    "displayAs": "number",
                    "displayName": "Customer ID #",
                    "fieldName": "Customer ID #",
                    "highlightLinks": false,
                    "imageHeight": "",
                    "imageTitleTemplate": "{{ @ }}",
                    "imageUrlTemplate": "{{ @ }}",
                    "imageWidth": "",
                    "linkOpenInNewTab": true,
                    "linkTextTemplate": "{{ @ }}",
                    "linkTitleTemplate": "{{ @ }}",
                    "linkUrlTemplate": "{{ @ }}",
                    "numberFormat": "",
                    "order": 100000,
                    "preserveWhitespace": false,
                    "title": "Customer ID #",
                    "type": "integer",
                    "useMonospaceFont": false,
                    "visible": true
                  },
                  {
                    "alignContent": "left",
                    "allowHTML": false,
                    "allowSearch": false,
                    "booleanValues": [
                      "false",
                      "true"
                    ],
                    "displayAs": "string",
                    "displayName": "Customer Segment",
                    "fieldName": "Customer Segment",
                    "highlightLinks": false,
                    "imageHeight": "",
                    "imageTitleTemplate": "{{ @ }}",
                    "imageUrlTemplate": "{{ @ }}",
                    "imageWidth": "",
                    "linkOpenInNewTab": true,
                    "linkTextTemplate": "{{ @ }}",
                    "linkTitleTemplate": "{{ @ }}",
                    "linkUrlTemplate": "{{ @ }}",
                    "order": 100001,
                    "preserveWhitespace": false,
                    "title": "Customer Segment",
                    "type": "string",
                    "useMonospaceFont": false,
                    "visible": true
                  },
                  {
                    "alignContent": "left",
                    "allowHTML": true,
                    "allowSearch": false,
                    "booleanValues": [
                      "false",
                      "true"
                    ],
                    "displayAs": "string",
                    "displayName": "Total Customer Revenue",
                    "fieldName": "Total Customer Revenue",
                    "highlightLinks": false,
                    "imageHeight": "",
                    "imageTitleTemplate": "{{ @ }}",
                    "imageUrlTemplate": "{{ @ }}",
                    "imageWidth": "",
                    "linkOpenInNewTab": true,
                    "linkTextTemplate": "{{ @ }}",
                    "linkTitleTemplate": "{{ @ }}",
                    "linkUrlTemplate": "{{ @ }}",
                    "order": 100003,
                    "preserveWhitespace": false,
                    "title": "Total Customer Revenue",
                    "type": "string",
                    "useMonospaceFont": false,
                    "visible": true
                  }
                ]
              },
              "frame": {
                "description": "All Time",
                "showDescription": true,
                "showTitle": true,
                "title": "Most Valuable Customers"
              },
              "invisibleColumns": [],
              "itemsPerPage": 25,
              "paginationSize": "default",
              "version": 1,
              "widgetType": "table",
              "withRowNumber": false
            }
          },
          "position": {
            "x": 2,
            "y": 12,
            "width": 4,
            "height": 6
          }
        },
        {
          "widget": {
            "name": "30fa90f0",
            "multilineTextboxSpec": {
              "lines": [
                "## Retail Revenue & Supply Chain Overview"
              ]
            }
          },
          "position": {
            "x": 0,
            "y": 0,
            "width": 6,
            "height": 1
          }
        },
        {
          "widget": {
            "name": "9d4b72c6",
            "queries": [
              {
                "name": "main_query",
                "query": {
                  "datasetName": "ced91012",
                  "fields": [
                    {
                      "name": "nation",
                      "expression": "`nation`"
                    },
                    {
                      "name": "sum(revenue)",
                      "expression": "SUM(`revenue`)"
                    },
                    {
                      "name": "yearly(o_orderdate)",
                      "expression": "DATE_TRUNC(\"YEAR\", `o_orderdate`)"
                    }
                  ],
                  "disaggregated": false
                }
              }
            ],
            "spec": {
              "encodings": {
                "color": {
                  "displayName": "Nation",
                  "fieldName": "nation",
                  "legend": {
                    "position": "bottom"
                  },
                  "scale": {
                    "mappings": [
                      {
                        "color": "#799CFF",
                        "value": "revenue"
                      },
                      {
                        "color": "#6B819C",
                        "value": "ARGENTINA"
                      },
                      {
                        "color": "#FFBF73",
                        "value": "UNITED KINGDOM"
                      },
                      {
                        "color": "#C8CFD3",
                        "value": "FRANCE"
                      },
                      {
                        "color": "#76C1E3",
                        "value": "BRAZIL"
                      },
                      {
                        "color": "#78B7C2",
                        "value": "CHINA"
                      },
                      {
                        "color": "#FFEC93",
                        "value": "UNITED STATES"
                      },
                      {
                        "color": "#FB9590",
                        "value": "JAPAN"
                      },
                      {
                        "color": "#B9486F",
                        "value": "JORDAN"
                      }
                    ],
                    "type": "categorical"
                  }
                },
                "x": {
                  "displayName": "Order Date",
                  "fieldName": "yearly(o_orderdate)",
                  "scale": {
                    "type": "temporal"
                  }
                },
                "y": {
                  "axis": {
                    "title": "Revenue"
                  },
                  "displayName": "Revenue",
                  "fieldName": "sum(revenue)",
                  "scale": {
                    "type": "quantitative"
                  }
                }
              },
              "frame": {
                "description": "By Nation",
                "showDescription": true,
                "showTitle": true,
                "title": "Revenue Trend"
              },
              "version": 3,
              "widgetType": "bar"
            }
          },
          "position": {
            "x": 0,
            "y": 4,
            "width": 2,
            "height": 8
          }
        },
        {
          "widget": {
            "name": "b9d722ef",
            "queries": [
              {
                "name": "dashboards/01eed1a58ea213dabed58b9c66678535/datasets/01eed1a58ea41d8abd497e3d322ed6cb_o_orderdate",
                "query": {
                  "datasetName": "ced91012",
                  "fields": [
                    {
                      "name": "o_orderdate",
                      "expression": "`o_orderdate`"
                    },
                    {
                      "name": "o_orderdate_associativity",
                      "expression": "COUNT_IF(`associative_filter_predicate_group`)"
                    }
                  ],
                  "disaggregated": false
                }
              },
              {
                "name": "dashboards/01eed1a58ea213dabed58b9c66678535/datasets/01eed1a58eb61207a6fe83b0fbe223bc_Date",
                "query": {
                  "datasetName": "e7a62da2",
                  "fields": [
                    {
                      "name": "Date",
                      "expression": "`Date`"
                    },
                    {
                      "name": "Date_associativity",
                      "expression": "COUNT_IF(`associative_filter_predicate_group`)"
                    }
                  ],
                  "disaggregated": false
                }
              },
              {
                "name": "dashboards/01eed1a58ea213dabed58b9c66678535/datasets/01eed1a58eb910c189ac48eb3557022d_o_orderdate",
                "query": {
                  "datasetName": "1bb727fb",
                  "fields": [
                    {
                      "name": "o_orderdate",
                      "expression": "`o_orderdate`"
                    },
                    {
                      "name": "o_orderdate_associativity",
                      "expression": "COUNT_IF(`associative_filter_predicate_group`)"
                    }
                  ],
                  "disaggregated": false
                }
              },
              {
                "name": "dashboards/01eed1a58ea213dabed58b9c66678535/datasets/01eed1ab760d1fa09512d065c91c1092_o_orderdate",
                "query": {
                  "datasetName": "a91573ca",
                  "fields": [
                    {
                      "name": "o_orderdate",
                      "expression": "`o_orderdate`"
                    },
                    {
                      "name": "o_orderdate_associativity",
                      "expression": "COUNT_IF(`associative_filter_predicate_group`)"
                    }
                  ],
                  "disaggregated": false
                }
              },
              {
                "name": "dashboards/01eed1a58ea213dabed58b9c66678535/datasets/01eed1aedd6c1a6ca2452baccaaf289d_l_shipdate",
                "query": {
                  "datasetName": "3530ec9c",
                  "fields": [
                    {
                      "name": "l_shipdate",
                      "expression": "`l_shipdate`"
                    },
                    {
                      "name": "l_shipdate_associativity",
                      "expression": "COUNT_IF(`associative_filter_predicate_group`)"
                    }
                  ],
                  "disaggregated": false
                }
              }
            ],
            "spec": {
              "encodings": {
                "fields": [
                  {
                    "displayName": "o_orderdate",
                    "fieldName": "o_orderdate",
                    "queryName": "dashboards/01eed1a58ea213dabed58b9c66678535/datasets/01eed1a58ea41d8abd497e3d322ed6cb_o_orderdate"
                  },
                  {
                    "displayName": "Date",
                    "fieldName": "Date",
                    "queryName": "dashboards/01eed1a58ea213dabed58b9c66678535/datasets/01eed1a58eb61207a6fe83b0fbe223bc_Date"
                  },
                  {
                    "displayName": "o_orderdate",
                    "fieldName": "o_orderdate",
                    "queryName": "dashboards/01eed1a58ea213dabed58b9c66678535/datasets/01eed1a58eb910c189ac48eb3557022d_o_orderdate"
                  },
                  {
                    "displayName": "o_orderdate",
                    "fieldName": "o_orderdate",
                    "queryName": "dashboards/01eed1a58ea213dabed58b9c66678535/datasets/01eed1ab760d1fa09512d065c91c1092_o_orderdate"
                  },
                  {
                    "displayName": "l_shipdate",
                    "fieldName": "l_shipdate",
                    "queryName": "dashboards/01eed1a58ea213dabed58b9c66678535/datasets/01eed1aedd6c1a6ca2452baccaaf289d_l_shipdate"
                  }
                ]
              },
              "frame": {
                "showTitle": true,
                "title": "Date Range"
              },
              "version": 2,
              "widgetType": "filter-date-range-picker"
            }
          },
          "position": {
            "x": 0,
            "y": 1,
            "width": 2,
            "height": 1
          }
        },
        {
          "widget": {
            "name": "d4d2ee35",
            "queries": [
              {
                "name": "main_query",
                "query": {
                  "datasetName": "a91573ca",
                  "fields": [
                    {
                      "name": "priority",
                      "expression": "`priority`"
                    },
                    {
                      "name": "ship_mode",
                      "expression": "`ship_mode`"
                    },
                    {
                      "name": "sum(order_count)",
                      "expression": "SUM(`order_count`)"
                    }
                  ],
                  "disaggregated": false
                }
              }
            ],
            "spec": {
              "encodings": {
                "color": {
                  "displayName": "Order Count",
                  "fieldName": "sum(order_count)",
                  "legend": {
                    "title": "Order Count"
                  },
                  "scale": {
                    "colorRamp": {
                      "colors": {
                        "end": "#536e96",
                        "start": "#97d8ff"
                      },
                      "mode": "custom-sequential"
                    },
                    "reverse": true,
                    "type": "quantitative"
                  }
                },
                "x": {
                  "displayName": "Order Priority",
                  "fieldName": "priority",
                  "scale": {
                    "type": "categorical"
                  }
                },
                "y": {
                  "displayName": "Shipping Method",
                  "fieldName": "ship_mode",
                  "scale": {
                    "type": "categorical"
                  }
                }
              },
              "frame": {
                "description": "By Order Priority",
                "showDescription": true,
                "showTitle": true,
                "title": "Top Shipping Methods"
              },
              "version": 3,
              "widgetType": "heatmap"
            }
          },
          "position": {
            "x": 2,
            "y": 7,
            "width": 4,
            "height": 5
          }
        },
        {
          "widget": {
            "name": "de550db9",
            "queries": [
              {
                "name": "main_query",
                "query": {
                  "datasetName": "e7a62da2",
                  "fields": [
                    {
                      "name": "Priority",
                      "expression": "`Priority`"
                    },
                    {
                      "name": "daily(Date)",
                      "expression": "DATE_TRUNC(\"DAY\", `Date`)"
                    },
                    {
                      "name": "sum(Total Price)",
                      "expression": "SUM(`Total Price`)"
                    }
                  ],
                  "disaggregated": false
                }
              }
            ],
            "spec": {
              "encodings": {
                "color": {
                  "displayName": "Priority",
                  "fieldName": "Priority",
                  "scale": {
                    "mappings": [
                      {
                        "color": "#70819A",
                        "value": "5-LOW"
                      },
                      {
                        "color": "#88BFE0",
                        "value": "4-NOT SPECIFIED"
                      },
                      {
                        "color": "#86B6C0",
                        "value": "3-MEDIUM"
                      },
                      {
                        "color": "#ED9A93",
                        "value": "2-HIGH"
                      },
                      {
                        "color": "#AC506F",
                        "value": "1-URGENT"
                      }
                    ],
                    "type": "categorical"
                  }
                },
                "x": {
                  "axis": {
                    "title": "Date"
                  },
                  "displayName": "Date",
                  "fieldName": "daily(Date)",
                  "scale": {
                    "type": "temporal"
                  }
                },
                "y": {
                  "displayName": "Sum of Total Price",
                  "fieldName": "sum(Total Price)",
                  "scale": {
                    "type": "quantitative"
                  }
                }
              },
              "frame": {
                "showTitle": true,
                "title": "Revenue by Order Priority"
              },
              "mark": {
                "colors": [
                  "#6B819C",
                  "#00A972",
                  "#FF3621",
                  "#8BCAE7",
                  "#AB4057",
                  "#99DDB4",
                  "#FCA4A1",
                  "#919191",
                  "#BF7080"
                ]
              },
              "version": 3,
              "widgetType": "line"
            }
          },
          "position": {
            "x": 2,
            "y": 1,
            "width": 4,
            "height": 6
          }
        }
      ],
      "pageType": "PAGE_TYPE_CANVAS"
    }
  ],
  "uiSettings": {
    "genieSpace": {
      "isEnabled": true,
      "enablementMode": "ENABLED"
    }
  }
}
```

---

## NYC Taxi Trip Analysis Dashboard

```json
{
  "datasets": [
    {
      "name": "0ca96e81",
      "displayName": "route revenue",
      "queryLines": [
        "SELECT\n",
        "  T.pickup_zip,\n",
        "  T.dropoff_zip,\n",
        "  T.route as `Route`,\n",
        "  T.frequency as `Number Trips`,\n",
        "  T.total_fare as `Total Revenue`\n",
        "FROM\n",
        "  (\n",
        "    SELECT\n",
        "      pickup_zip,\n",
        "      dropoff_zip,\n",
        "      concat(pickup_zip, '-', dropoff_zip) AS route,\n",
        "      count(*) as frequency,\n",
        "      SUM(fare_amount) as total_fare\n",
        "    FROM\n",
        "      `samples`.`nyctaxi`.`trips`\n",
        "    GROUP BY\n",
        "       1,2,3\n",
        "  ) T\n",
        "ORDER BY\n",
        "  1 ASC"
      ]
    },
    {
      "name": "3f5450e6",
      "displayName": "trips",
      "queryLines": [
        "SELECT\n",
        "  T.tpep_pickup_datetime,\n",
        "  T.tpep_dropoff_datetime,\n",
        "  T.fare_amount,\n",
        "  T.pickup_zip,\n",
        "  T.dropoff_zip,\n",
        "  T.trip_distance,\n",
        "  T.weekday,\n",
        "  CASE\n",
        "    WHEN T.weekday = 1 THEN 'Sunday'\n",
        "    WHEN T.weekday = 2 THEN 'Monday'\n",
        "    WHEN T.weekday = 3 THEN 'Tuesday'\n",
        "    WHEN T.weekday = 4 THEN 'Wednesday'\n",
        "    WHEN T.weekday = 5 THEN 'Thursday'\n",
        "    WHEN T.weekday = 6 THEN 'Friday'\n",
        "    WHEN T.weekday = 7 THEN 'Saturday'\n",
        "    ELSE 'N/A'\n",
        "  END AS day_of_week\n",
        "FROM\n",
        "  (\n",
        "    SELECT\n",
        "      dayofweek(tpep_pickup_datetime) as weekday,\n",
        "      *\n",
        "    FROM\n",
        "      `samples`.`nyctaxi`.`trips`\n",
        "    WHERE\n",
        "      trip_distance > 0\n",
        "      AND trip_distance < 10\n",
        "      AND fare_amount > 0\n",
        "      AND fare_amount < 50\n",
        "  ) T\n",
        "ORDER BY\n",
        "  T.weekday  "
      ]
    }
  ],
  "pages": [
    {
      "name": "5a35864d",
      "displayName": "Summary",
      "layout": [
        {
          "widget": {
            "name": "01e21234",
            "queries": [
              {
                "name": "dashboards/01ee564285a315dd80d473e76171660a/datasets/01ee564285a51daf810a8ffc5051bfee_tpep_dropoff_datetime",
                "query": {
                  "datasetName": "3f5450e6",
                  "fields": [
                    {
                      "name": "tpep_dropoff_datetime",
                      "expression": "`tpep_dropoff_datetime`"
                    },
                    {
                      "name": "tpep_dropoff_datetime_associativity",
                      "expression": "COUNT_IF(`associative_filter_predicate_group`)"
                    }
                  ],
                  "disaggregated": false
                }
              }
            ],
            "spec": {
              "encodings": {
                "fields": [
                  {
                    "displayName": "tpep_dropoff_datetime",
                    "fieldName": "tpep_dropoff_datetime",
                    "queryName": "dashboards/01ee564285a315dd80d473e76171660a/datasets/01ee564285a51daf810a8ffc5051bfee_tpep_dropoff_datetime"
                  }
                ]
              },
              "frame": {
                "showTitle": true,
                "title": "Time Range"
              },
              "version": 2,
              "widgetType": "filter-date-range-picker"
            }
          },
          "position": {
            "x": 0,
            "y": 1,
            "width": 2,
            "height": 1
          }
        },
        {
          "widget": {
            "name": "2c147a61",
            "queries": [
              {
                "name": "main_query",
                "query": {
                  "datasetName": "3f5450e6",
                  "fields": [
                    {
                      "name": "count(*)",
                      "expression": "COUNT(`*`)"
                    },
                    {
                      "name": "hourly(tpep_pickup_datetime)",
                      "expression": "DATE_TRUNC(\"HOUR\", `tpep_pickup_datetime`)"
                    }
                  ],
                  "disaggregated": false
                }
              }
            ],
            "spec": {
              "encodings": {
                "label": {
                  "show": false
                },
                "x": {
                  "axis": {
                    "title": "Pickup Hour"
                  },
                  "displayName": "Pickup Hour",
                  "fieldName": "hourly(tpep_pickup_datetime)",
                  "scale": {
                    "type": "temporal"
                  }
                },
                "y": {
                  "axis": {
                    "title": "Number of Rides"
                  },
                  "displayName": "Number of Rides",
                  "fieldName": "count(*)",
                  "scale": {
                    "type": "quantitative"
                  }
                }
              },
              "frame": {
                "showTitle": true,
                "title": "Pickup Hour Distribution"
              },
              "mark": {
                "colors": [
                  "#077A9D",
                  "#FFAB00",
                  "#00A972",
                  "#FF3621",
                  "#8BCAE7",
                  "#AB4057",
                  "#99DDB4",
                  "#FCA4A1",
                  "#919191",
                  "#BF7080"
                ]
              },
              "version": 3,
              "widgetType": "bar"
            }
          },
          "position": {
            "x": 0,
            "y": 10,
            "width": 3,
            "height": 4
          }
        },
        {
          "widget": {
            "name": "35a5a364",
            "queries": [
              {
                "name": "main_query",
                "query": {
                  "datasetName": "3f5450e6",
                  "fields": [
                    {
                      "name": "day_of_week",
                      "expression": "`day_of_week`"
                    },
                    {
                      "name": "fare_amount",
                      "expression": "`fare_amount`"
                    },
                    {
                      "name": "trip_distance",
                      "expression": "`trip_distance`"
                    }
                  ],
                  "disaggregated": true
                }
              }
            ],
            "spec": {
              "encodings": {
                "color": {
                  "displayName": "Day of Week",
                  "fieldName": "day_of_week",
                  "scale": {
                    "type": "categorical"
                  }
                },
                "x": {
                  "axis": {
                    "title": "Trip Distance (miles)"
                  },
                  "displayName": "trip_distance",
                  "fieldName": "trip_distance",
                  "scale": {
                    "type": "quantitative"
                  }
                },
                "y": {
                  "axis": {
                    "title": "Fare Amount (USD)"
                  },
                  "displayName": "fare_amount",
                  "fieldName": "fare_amount",
                  "scale": {
                    "type": "quantitative"
                  }
                }
              },
              "frame": {
                "showTitle": true,
                "title": "Daily Fare Trends by Day of Week"
              },
              "version": 3,
              "widgetType": "scatter"
            }
          },
          "position": {
            "x": 2,
            "y": 2,
            "width": 4,
            "height": 8
          }
        },
        {
          "widget": {
            "name": "4e04176c",
            "multilineTextboxSpec": {
              "lines": [
                "# NYC Taxi Trip Analysis"
              ]
            }
          },
          "position": {
            "x": 0,
            "y": 0,
            "width": 6,
            "height": 1
          }
        },
        {
          "widget": {
            "name": "64a2a1f5",
            "queries": [
              {
                "name": "main_query",
                "query": {
                  "datasetName": "3f5450e6",
                  "fields": [
                    {
                      "name": "count(*)",
                      "expression": "COUNT(`*`)"
                    },
                    {
                      "name": "hourly(tpep_dropoff_datetime)",
                      "expression": "DATE_TRUNC(\"HOUR\", `tpep_dropoff_datetime`)"
                    }
                  ],
                  "disaggregated": false
                }
              }
            ],
            "spec": {
              "encodings": {
                "x": {
                  "axis": {
                    "title": "Dropoff Hour"
                  },
                  "displayName": "Dropoff Hour",
                  "fieldName": "hourly(tpep_dropoff_datetime)",
                  "scale": {
                    "type": "temporal"
                  }
                },
                "y": {
                  "axis": {
                    "title": "Number of Rides"
                  },
                  "displayName": "Number of Rides",
                  "fieldName": "count(*)",
                  "scale": {
                    "type": "quantitative"
                  }
                }
              },
              "frame": {
                "showTitle": true,
                "title": "Dropoff Hour Distribution"
              },
              "mark": {
                "colors": [
                  "#FFAB00",
                  "#FFAB00",
                  "#00A972",
                  "#FF3621",
                  "#8BCAE7",
                  "#AB4057",
                  "#99DDB4",
                  "#FCA4A1",
                  "#919191",
                  "#BF7080"
                ]
              },
              "version": 3,
              "widgetType": "bar"
            }
          },
          "position": {
            "x": 3,
            "y": 10,
            "width": 3,
            "height": 4
          }
        },
        {
          "widget": {
            "name": "8a537060",
            "queries": [
              {
                "name": "main_query",
                "query": {
                  "datasetName": "3f5450e6",
                  "fields": [
                    {
                      "name": "count(*)",
                      "expression": "COUNT(`*`)"
                    }
                  ],
                  "disaggregated": false
                }
              }
            ],
            "spec": {
              "encodings": {
                "value": {
                  "displayName": "Count of Records",
                  "fieldName": "count(*)"
                }
              },
              "frame": {
                "showTitle": true,
                "title": "Total Trips"
              },
              "version": 2,
              "widgetType": "counter"
            }
          },
          "position": {
            "x": 0,
            "y": 2,
            "width": 2,
            "height": 2
          }
        },
        {
          "widget": {
            "name": "c4e14639",
            "queries": [
              {
                "name": "dashboards/01eed0e4082a1c7e903cac7e74114376/datasets/01eed0e4082d1205adc131b86b10198e_pickup_zip",
                "query": {
                  "datasetName": "0ca96e81",
                  "fields": [
                    {
                      "name": "pickup_zip",
                      "expression": "`pickup_zip`"
                    },
                    {
                      "name": "pickup_zip_associativity",
                      "expression": "COUNT_IF(`associative_filter_predicate_group`)"
                    }
                  ],
                  "disaggregated": false
                }
              },
              {
                "name": "dashboards/01eed0e4082a1c7e903cac7e74114376/datasets/01eed0e4082e1ff49c3209776820e82e_pickup_zip",
                "query": {
                  "datasetName": "3f5450e6",
                  "fields": [
                    {
                      "name": "pickup_zip",
                      "expression": "`pickup_zip`"
                    },
                    {
                      "name": "pickup_zip_associativity",
                      "expression": "COUNT_IF(`associative_filter_predicate_group`)"
                    }
                  ],
                  "disaggregated": false
                }
              }
            ],
            "spec": {
              "encodings": {
                "fields": [
                  {
                    "displayName": "pickup_zip",
                    "fieldName": "pickup_zip",
                    "queryName": "dashboards/01eed0e4082a1c7e903cac7e74114376/datasets/01eed0e4082e1ff49c3209776820e82e_pickup_zip"
                  },
                  {
                    "displayName": "pickup_zip",
                    "fieldName": "pickup_zip",
                    "queryName": "dashboards/01eed0e4082a1c7e903cac7e74114376/datasets/01eed0e4082d1205adc131b86b10198e_pickup_zip"
                  }
                ]
              },
              "frame": {
                "showTitle": true,
                "title": "Pickup Zip"
              },
              "version": 2,
              "widgetType": "filter-multi-select"
            }
          },
          "position": {
            "x": 2,
            "y": 1,
            "width": 2,
            "height": 1
          }
        },
        {
          "widget": {
            "name": "c532be56",
            "queries": [
              {
                "name": "main_query",
                "query": {
                  "datasetName": "0ca96e81",
                  "fields": [
                    {
                      "name": "Number Trips",
                      "expression": "`Number Trips`"
                    },
                    {
                      "name": "Route",
                      "expression": "`Route`"
                    },
                    {
                      "name": "Total Revenue",
                      "expression": "`Total Revenue`"
                    }
                  ],
                  "disaggregated": true
                }
              }
            ],
            "spec": {
              "allowHTMLByDefault": false,
              "condensed": true,
              "encodings": {
                "columns": [
                  {
                    "alignContent": "left",
                    "allowHTML": false,
                    "allowSearch": false,
                    "booleanValues": [
                      "false",
                      "true"
                    ],
                    "displayAs": "string",
                    "displayName": "Route",
                    "fieldName": "Route",
                    "highlightLinks": false,
                    "imageHeight": "",
                    "imageTitleTemplate": "{{ @ }}",
                    "imageUrlTemplate": "{{ @ }}",
                    "imageWidth": "",
                    "linkOpenInNewTab": true,
                    "linkTextTemplate": "{{ @ }}",
                    "linkTitleTemplate": "{{ @ }}",
                    "linkUrlTemplate": "{{ @ }}",
                    "order": 100000,
                    "preserveWhitespace": false,
                    "title": "Route",
                    "type": "string",
                    "useMonospaceFont": false,
                    "visible": true
                  },
                  {
                    "alignContent": "right",
                    "allowHTML": false,
                    "allowSearch": false,
                    "booleanValues": [
                      "false",
                      "true"
                    ],
                    "displayAs": "number",
                    "displayName": "Number Trips",
                    "fieldName": "Number Trips",
                    "highlightLinks": false,
                    "imageHeight": "",
                    "imageTitleTemplate": "{{ @ }}",
                    "imageUrlTemplate": "{{ @ }}",
                    "imageWidth": "",
                    "linkOpenInNewTab": true,
                    "linkTextTemplate": "{{ @ }}",
                    "linkTitleTemplate": "{{ @ }}",
                    "linkUrlTemplate": "{{ @ }}",
                    "numberFormat": "0",
                    "order": 100001,
                    "preserveWhitespace": false,
                    "title": "Number Trips",
                    "type": "integer",
                    "useMonospaceFont": false,
                    "visible": true
                  },
                  {
                    "alignContent": "right",
                    "allowHTML": false,
                    "allowSearch": false,
                    "booleanValues": [
                      "false",
                      "true"
                    ],
                    "cellFormat": {
                      "default": {
                        "foregroundColor": "#85CADE"
                      },
                      "rules": [
                        {
                          "if": {
                            "column": "Total Revenue",
                            "fn": "<",
                            "literal": "51"
                          },
                          "value": {
                            "foregroundColor": "#9C2638"
                          }
                        },
                        {
                          "if": {
                            "column": "Total Revenue",
                            "fn": "<",
                            "literal": "101"
                          },
                          "value": {
                            "foregroundColor": "#FFD465"
                          }
                        },
                        {
                          "if": {
                            "column": "Total Revenue",
                            "fn": "<",
                            "literal": "6001"
                          },
                          "value": {
                            "foregroundColor": "#1FA873"
                          }
                        }
                      ]
                    },
                    "displayAs": "number",
                    "displayName": "Total Revenue",
                    "fieldName": "Total Revenue",
                    "highlightLinks": false,
                    "imageHeight": "",
                    "imageTitleTemplate": "{{ @ }}",
                    "imageUrlTemplate": "{{ @ }}",
                    "imageWidth": "",
                    "linkOpenInNewTab": true,
                    "linkTextTemplate": "{{ @ }}",
                    "linkTitleTemplate": "{{ @ }}",
                    "linkUrlTemplate": "{{ @ }}",
                    "numberFormat": "$0.00",
                    "order": 100002,
                    "preserveWhitespace": false,
                    "title": "Total Revenue",
                    "type": "float",
                    "useMonospaceFont": false,
                    "visible": true
                  }
                ]
              },
              "frame": {
                "showTitle": true,
                "title": "Route Revenue Attribution"
              },
              "invisibleColumns": [
                {
                  "alignContent": "right",
                  "allowHTML": false,
                  "allowSearch": false,
                  "booleanValues": [
                    "false",
                    "true"
                  ],
                  "displayAs": "number",
                  "highlightLinks": false,
                  "imageHeight": "",
                  "imageTitleTemplate": "{{ @ }}",
                  "imageUrlTemplate": "{{ @ }}",
                  "imageWidth": "",
                  "linkOpenInNewTab": true,
                  "linkTextTemplate": "{{ @ }}",
                  "linkTitleTemplate": "{{ @ }}",
                  "linkUrlTemplate": "{{ @ }}",
                  "name": "pickup_zip",
                  "numberFormat": "0",
                  "order": 100000,
                  "preserveWhitespace": false,
                  "title": "pickup_zip",
                  "type": "integer",
                  "useMonospaceFont": false
                },
                {
                  "alignContent": "right",
                  "allowHTML": false,
                  "allowSearch": false,
                  "booleanValues": [
                    "false",
                    "true"
                  ],
                  "displayAs": "number",
                  "highlightLinks": false,
                  "imageHeight": "",
                  "imageTitleTemplate": "{{ @ }}",
                  "imageUrlTemplate": "{{ @ }}",
                  "imageWidth": "",
                  "linkOpenInNewTab": true,
                  "linkTextTemplate": "{{ @ }}",
                  "linkTitleTemplate": "{{ @ }}",
                  "linkUrlTemplate": "{{ @ }}",
                  "name": "dropoff_zip",
                  "numberFormat": "0",
                  "order": 100001,
                  "preserveWhitespace": false,
                  "title": "dropoff_zip",
                  "type": "integer",
                  "useMonospaceFont": false
                }
              ],
              "itemsPerPage": 25,
              "paginationSize": "default",
              "version": 1,
              "widgetType": "table",
              "withRowNumber": false
            }
          },
          "position": {
            "x": 0,
            "y": 4,
            "width": 2,
            "height": 6
          }
        },
        {
          "widget": {
            "name": "c6fc64a3",
            "queries": [
              {
                "name": "dashboards/01eed0e4082a1c7e903cac7e74114376/datasets/01eed0e4082d1205adc131b86b10198e_dropoff_zip",
                "query": {
                  "datasetName": "0ca96e81",
                  "fields": [
                    {
                      "name": "dropoff_zip",
                      "expression": "`dropoff_zip`"
                    },
                    {
                      "name": "dropoff_zip_associativity",
                      "expression": "COUNT_IF(`associative_filter_predicate_group`)"
                    }
                  ],
                  "disaggregated": false
                }
              },
              {
                "name": "dashboards/01eed0e4082a1c7e903cac7e74114376/datasets/01eed0e4082e1ff49c3209776820e82e_dropoff_zip",
                "query": {
                  "datasetName": "3f5450e6",
                  "fields": [
                    {
                      "name": "dropoff_zip",
                      "expression": "`dropoff_zip`"
                    },
                    {
                      "name": "dropoff_zip_associativity",
                      "expression": "COUNT_IF(`associative_filter_predicate_group`)"
                    }
                  ],
                  "disaggregated": false
                }
              }
            ],
            "spec": {
              "encodings": {
                "fields": [
                  {
                    "displayName": "dropoff_zip",
                    "fieldName": "dropoff_zip",
                    "queryName": "dashboards/01eed0e4082a1c7e903cac7e74114376/datasets/01eed0e4082e1ff49c3209776820e82e_dropoff_zip"
                  },
                  {
                    "displayName": "dropoff_zip",
                    "fieldName": "dropoff_zip",
                    "queryName": "dashboards/01eed0e4082a1c7e903cac7e74114376/datasets/01eed0e4082d1205adc131b86b10198e_dropoff_zip"
                  }
                ]
              },
              "frame": {
                "showTitle": true,
                "title": "Dropoff Zip"
              },
              "version": 2,
              "widgetType": "filter-multi-select"
            }
          },
          "position": {
            "x": 4,
            "y": 1,
            "width": 2,
            "height": 1
          }
        }
      ],
      "pageType": "PAGE_TYPE_CANVAS"
    }
  ],
  "uiSettings": {
    "genieSpace": {
      "isEnabled": true,
      "enablementMode": "ENABLED"
    }
  }
}
```

---

## Layout Guidelines

### Grid System

- 12 columns wide
- Position widgets using `x` (0-11), `y` (row), `width` (1-12), `height`
- Avoid overlapping widgets
- Suggested widths: 3 (1/4), 4 (1/3), 6 (1/2), 12 (full)

### Recommended Layout Pattern

```
Row 0: Header/Title (width: 12, height: 1)
Row 1: Filters (3-4 columns each, height: 1)
Row 2-3: Counters/KPIs (3-4 columns each, height: 2)
Row 4-7: Charts (6 columns each, height: 4)
Row 8+: Tables (12 columns, height: 4-6)
```
