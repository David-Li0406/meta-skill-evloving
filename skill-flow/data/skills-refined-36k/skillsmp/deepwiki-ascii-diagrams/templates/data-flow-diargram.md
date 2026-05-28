# Data Flow Diagram Templates

Data flow diagrams illustrate how data moves through a system, including transformations, storage, and processing steps. They focus on data sources, destinations, and the flow of information.

---

## Template 1: E-Commerce Data Flow

**Purpose**: Show how customer data flows through an e-commerce system

```
┌─────────────────────────────────────────────────────────────────┐
│                    E-Commerce Data Flow                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐                                                │
│  │   User     │                                                 │
│  │  Frontend  │                                                 │
│  └──────┬──────┘                                                │
│         │                                                       │
│         │ "customer_id, product_id, quantity"                 │
│         │ (JSON payload)                                      │
│         ▼                                                       │
│  ┌──────────────────┐                                          │
│  │  API Gateway     │                                          │
│  │                  │                                          │
│  │ POST /orders     │                                          │
│  └──────┬───────────┘                                          │
│         │                                                       │
│         │ "order_data + timestamp"                            │
│         ▼                                                       │
│  ┌──────────────────────────┐                                  │
│  │ Order Validation Service │                                  │
│  │                          │                                  │
│  │ - Check inventory        │                                  │
│  │ - Validate customer      │                                  │
│  │ - Calculate price        │                                  │
│  └──────┬───────────────────┘                                  │
│         │                                                       │
│    ┌────┴────┐                                                 │
│    │          │                                                │
│    ▼ Valid    ▼ Invalid                                        │
│  ┌─────┐  ┌──────────────┐                                     │
│  │     │  │ Error Logger │                                     │
│  │     │  │              │                                     │
│  │     │  │ - Log error  │                                     │
│  │     │  │ - Send alert │                                     │
│  │     │  └──────┬───────┘                                     │
│  │     │         │                                             │
│  │     │         ▼                                             │
│  │     │    ┏━━━━━━━━━━━━━━┓                                  │
│  │     │    ┃  Error DB    ┃                                  │
│  │     │    ┗━━━━━━━━━━━━━━┛                                  │
│  │     │                                                       │
│  │     └────────────────┐                                     │
│  │                      │                                     │
│  ▼                      ▼                                      │
│  ┌─────────────────────────────────┐                          │
│  │ Event Stream (Message Queue)    │                          │
│  │                                 │                          │
│  │ "order_created" event           │                          │
│  │ {order_id, items, price, ...}   │                          │
│  └──────────┬──────────┬──────┬────┘                          │
│             │          │      │                               │
│      ┌──────┘          │      └──────┐                         │
│      │                 │             │                        │
│      ▼                 ▼             ▼                        │
│  ┌─────────┐  ┌──────────┐  ┌─────────────┐                  │
│  │Inventory│  │ Payment  │  │ Notification│                  │
│  │Service  │  │ Service  │  │ Service     │                  │
│  │         │  │          │  │             │                  │
│  │ Reduce  │  │ Charge   │  │ Send email  │                  │
│  │ stock   │  │ card     │  │ to customer │                  │
│  └─────┬───┘  └────┬─────┘  └──────┬──────┘                  │
│        │           │               │                         │
│        │ "stock_   │ "payment_     │ "notification"          │
│        │  updated" │  processed"   │ "sent"                  │
│        ▼           ▼               ▼                         │
│  ┌──────────────────────────────────────────┐                │
│  │        Order Database (PostgreSQL)       │                │
│  │                                          │                │
│  │ ┏━━━━━━━━━━━━┓  ┏━━━━━━━━━━━━━━┓       │                │
│  │ ┃  Orders    ┃  ┃ Transactions ┃       │                │
│  │ ┃ - order_id ┃  ┃ - tx_id      ┃       │                │
│  │ ┃ - status   ┃  ┃ - amount     ┃       │                │
│  │ ┃ - total    ┃  ┃ - status     ┃       │                │
│  │ ┗━━━━━━━━━━━━┛  ┗━━━━━━━━━━━━━━┛       │                │
│  └──────────────────────────────────────────┘                │
│                                                               │
│  ┌──────────────────────────────────────────┐                │
│  │         Data Warehouse (Analytics)       │                │
│  │  [Periodic batch sync every 6 hours]     │                │
│  │                                          │                │
│  │ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │                │
│  │ ┃ Fact Table: Orders                ┃  │                │
│  │ ┃ - customer_id, product_id, date   ┃  │                │
│  │ ┃ - amount, revenue                 ┃  │                │
│  │ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │                │
│  │                                          │                │
│  │ Reports & Dashboards                     │                │
│  │ - Daily revenue                          │                │
│  │ - Top products                           │                │
│  │ - Customer trends                        │                │
│  └──────────────────────────────────────────┘                │
│                                                               │
└─────────────────────────────────────────────────────────────────┘

[Shows data flow from user creation through services to persistent storage]
```

### Key Flows
- **Order Creation**: From UI through validation to event stream
- **Event Distribution**: Single event triggers multiple downstream services
- **Data Persistence**: Transactional data stored in operational database
- **Analytics Pipeline**: Regular sync to data warehouse for reporting

---

## Template 2: Real-Time Analytics Data Pipeline

**Purpose**: Show streaming data flow for real-time processing

```
┌─────────────────────────────────────────────────────────────┐
│              Real-Time Analytics Pipeline                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Data Sources:                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Website Events          │ Mobile App Events         │   │
│  │ (pageviews, clicks)     │ (taps, gestures)         │   │
│  │                         │                          │   │
│  │ Server Logs             │ IoT Sensors              │   │
│  │ (requests, errors)      │ (temp, pressure)         │   │
│  └────────────┬────────────┴──────────┬────────────────┘   │
│               │                       │                    │
│               └───────────┬───────────┘                     │
│                           │                                │
│                           │ "raw_events" stream            │
│                           ▼                                │
│            ┌──────────────────────────┐                   │
│            │   Apache Kafka / PubSub  │                   │
│            │   (Event Stream)         │                   │
│            │                          │                   │
│            │ Topic: events            │                   │
│            │ 3 partitions             │                   │
│            │ 24hr retention           │                   │
│            └────────┬──────────┬──────┘                   │
│                     │          │                         │
│          ┌──────────┘          └──────────┐              │
│          │                                 │              │
│          ▼                                 ▼              │
│   ┌─────────────────┐            ┌──────────────────┐   │
│   │ Stream Processor│            │ Stream Processor │   │
│   │  (Apache Flink) │            │  (Spark Streaming)   │
│   │                 │            │                  │   │
│   │ Processing:     │            │ Processing:      │   │
│   │ - Deduplicate   │            │ - Aggregation    │   │
│   │ - Filter events │            │ - Windowing      │   │
│   │ - Enrich data   │            │ - Joining streams│   │
│   │ - State mgmt    │            │ - Feature eng.   │   │
│   └────────┬────────┘            └────────┬─────────┘   │
│            │                              │             │
│            │ "processed_events"           │             │
│            ▼                              ▼             │
│    ┌─────────────────────────────────────────────┐    │
│    │  Real-Time Data Storage Layer               │    │
│    │                                             │    │
│    │ ┌──────────────┐    ┌────────────────────┐ │    │
│    │ │ Time-Series  │    │ Key-Value Store    │ │    │
│    │ │ DB (InfluxDB)│    │ (Redis)            │ │    │
│    │ │              │    │                    │ │    │
│    │ │ - Metrics    │    │ - User aggregates  │ │    │
│    │ │ - Events     │    │ - Counters         │ │    │
│    │ │ - Traces     │    │ - Feature cache    │ │    │
│    │ └──────────────┘    └────────────────────┘ │    │
│    │                                             │    │
│    │ ┌──────────────────────────────────────┐   │    │
│    │ │ Vector Database (Pinecone/Weaviate)  │   │    │
│    │ │ - Embeddings for similarity search   │   │    │
│    │ │ - Real-time recommendations         │   │    │
│    │ └──────────────────────────────────────┘   │    │
│    └─────────────────────────────────────────────┘    │
│            │              │              │             │
│            ▼              ▼              ▼             │
│    ┌────────────────────────────────────────────┐    │
│    │   Live Dashboards & Real-Time Apps        │    │
│    │                                            │    │
│    │ - User activity heatmaps                  │    │
│    │ - Real-time anomaly alerts                │    │
│    │ - Live conversion funnels                 │    │
│    │ - Performance metrics                     │    │
│    └────────────────────────────────────────────┘    │
│                                                       │
│    ┌────────────────────────────────────────────┐    │
│    │   Batch Layer (Historical Analysis)        │    │
│    │   [Daily ETL at 2 AM UTC]                  │    │
│    │                                            │    │
│    │ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │    │
│    │ ┃ Data Lake (S3/HDFS)                  ┃ │    │
│    │ ┃ - Raw events archive                 ┃ │    │
│    │ ┃ - Processed data store               ┃ │    │
│    │ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ │    │
│    │                                            │    │
│    │ ┌──────────────────────────────────────┐  │    │
│    │ │ Data Warehouse (Snowflake/BigQuery)  │  │    │
│    │ │ - Fact tables                        │  │    │
│    │ │ - Dimension tables                   │  │    │
│    │ │ - Aggregated metrics                 │  │    │
│    │ └──────────────────────────────────────┘  │    │
│    └────────────────────────────────────────────┘    │
│                                                       │
└─────────────────────────────────────────────────────────┘

[Shows streaming data from multiple sources through processors to real-time and batch storage]
```

### Key Components
- **Data Sources**: Diverse event streams (web, mobile, servers, IoT)
- **Event Stream**: Kafka/PubSub for distributed event buffering
- **Stream Processing**: Real-time transformation and enrichment
- **Storage Tiers**: Hot (Redis), Warm (Time-series DB), Cold (Data Lake)
- **Consumption**: Live dashboards and batch analytics

---

## Template 3: Data Lake & Data Warehouse Architecture

**Purpose**: Show how data flows from raw to analytics-ready

```
┌──────────────────────────────────────────────────────────────┐
│            Data Lake & Warehouse Architecture                │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  Ingestion Layer:                                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Data Sources                                           │ │
│  │ ┌──────────┐ ┌──────────┐ ┌──────────┐               │ │
│  │ │Databases │ │CSV Files │ │ API Data │ ┌─────────┐  │ │
│  │ │(MySQL)   │ │(S3)      │ │(Webhooks)│ │  Logs   │  │ │
│  │ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬────┘  │ │
│  │      │            │            │            │        │ │
│  └──────┼────────────┼────────────┼────────────┼────────┘ │
│         │            │            │            │           │
│         │ "raw_data" │            │            │           │
│         ▼            ▼            ▼            ▼           │
│  ┌───────────────────────────────────────────────────┐   │
│  │         Apache Airflow / Prefect                  │   │
│  │         (ETL/ELT Orchestration)                   │   │
│  │                                                   │   │
│  │ DAG: daily_etl_pipeline                          │   │
│  │ ├─ extract_from_databases                        │   │
│  │ ├─ validate_schema                               │   │
│  │ ├─ transform_to_parquet                          │   │
│  │ └─ load_to_data_lake                             │   │
│  └───────────────────┬───────────────────────────────┘   │
│                      │                                    │
│          ┌───────────┴──────────┐                        │
│          │                      │                        │
│          ▼                      ▼                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │      Data Lake (S3 / Azure Data Lake)            │  │
│  │                                                  │  │
│  │  Bronze Layer (Raw):                            │  │
│  │  ┌─────────────────────────────────────────┐   │  │
│  │  │ /bronze/raw_data/                       │   │  │
│  │  │ ├─ 2026-01-02/                          │   │  │
│  │  │ │  ├─ database_dump.parquet             │   │  │
│  │  │ │  ├─ api_events.json                   │   │  │
│  │  │ │  └─ logs.csv                          │   │  │
│  │  │ └─ 2026-01-01/                          │   │  │
│  │  └─────────────────────────────────────────┘   │  │
│  │                                                  │  │
│  │  Silver Layer (Cleaned):                        │  │
│  │  ┌─────────────────────────────────────────┐   │  │
│  │  │ /silver/curated_data/                   │   │  │
│  │  │ ├─ customers/ (deduplicated)            │   │  │
│  │  │ ├─ orders/ (validated)                  │   │  │
│  │  │ └─ products/ (enriched)                 │   │  │
│  │  └─────────────────────────────────────────┘   │  │
│  │                                                  │  │
│  │  Gold Layer (Analytics):                        │  │
│  │  ┌─────────────────────────────────────────┐   │  │
│  │  │ /gold/analytics/                        │   │  │
│  │  │ ├─ customer_360/ (360° view)            │   │  │
│  │  │ ├─ sales_metrics/ (aggregated)          │   │  │
│  │  │ └─ monthly_reports/ (processed)         │   │  │
│  │  └─────────────────────────────────────────┘   │  │
│  │                                                  │  │
│  └──────────────────┬───────────────────────────────┘  │
│                     │                                  │
│                     │ "gold_data"                      │
│                     ▼                                  │
│  ┌──────────────────────────────────────────────────┐  │
│  │   Data Warehouse (Snowflake / BigQuery)          │  │
│  │                                                  │  │
│  │  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │  │
│  │  ┃ Dimension Tables:                       ┃  │  │
│  │  ┃ - dim_customer (id, name, segment...)   ┃  │  │
│  │  ┃ - dim_product (id, category, price...)  ┃  │  │
│  │  ┃ - dim_date (date, month, quarter...)    ┃  │  │
│  │  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │  │
│  │                                                  │  │
│  │  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │  │
│  │  ┃ Fact Tables:                            ┃  │  │
│  │  ┃ - fact_sales (customer_id, product_id,  ┃  │  │
│  │  ┃            date_id, amount, quantity)   ┃  │  │
│  │  ┃ - fact_inventory (product_id, date_id,  ┃  │  │
│  │  ┃                   quantity_on_hand)     ┃  │  │
│  │  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │  │
│  │                                                  │  │
│  └──────────────────┬───────────────────────────────┘  │
│                     │                                  │
│          ┌──────────┴──────────┐                     │
│          │                     │                     │
│          ▼                     ▼                     │
│  ┌─────────────────┐  ┌──────────────────────┐     │
│  │ BI Tools        │  │ ML Features          │     │
│  │ (Tableau,Power) │  │ (Feature Store)      │     │
│  │                 │  │                      │     │
│  │ - Dashboards    │  │ - Compute features   │     │
│  │ - Reports       │  │ - Store vectors      │     │
│  │ - Ad-hoc queries│  │ - Serve ML models    │     │
│  └─────────────────┘  └──────────────────────┘     │
│                                                      │
└──────────────────────────────────────────────────────┘

[Shows data progression from raw (bronze) through cleaned (silver) to analytics-ready (gold)]
```

### Key Layers
- **Bronze**: Raw, untransformed data as received
- **Silver**: Cleaned, deduplicated, validated data
- **Gold**: Aggregated, business-ready data for analytics
- **Warehouse**: Star schema with dimensions and facts for reporting
- **Consumption**: BI tools and ML feature stores

---

## Template 4: ETL vs ELT Comparison

**Purpose**: Show different data processing approaches

```
Traditional ETL:                  Modern ELT:

Source → Extract → Transform    Source → Extract → Load
    ↓        ↓         ↓             ↓        ↓       ↓
    ▼        ▼         ▼             ▼        ▼       ▼
┌──────┐ ┌────────┐ ┌────┐        ┌──────┐ ┌────┐ ┌─────────┐
│ Data │ │ Staging│ │DWH │        │ Data │ │DWH │ │Transform│
│Source│ │ Area   │ │    │        │Source│ │    │ │  (SQL)  │
└──────┘ └────────┘ └────┘        └──────┘ └────┘ └─────────┘
    │        │        │               │       │        │
    └────────┴────────┘               └───────┴────────┘
         │                                    │
         ▼                                    ▼
    Process-Heavy         Load-Heavy, Transform-Light
    Extract Format        Warehouse Scale
    Network Heavy         Parallel SQL Processing
```

---

## Best Practices

### Do's ✓
- Show data sources and destinations clearly
- Include transformation/processing steps
- Label data formats (JSON, Parquet, CSV, etc.)
- Show data quality checks and error handling
- Include frequency/timing information
- Show both real-time and batch paths
- Indicate data volume and velocity

### Don'ts ✗
- Omit error paths and dead letter queues
- Forget to show intermediate storage
- Mix structural and data flow concerns
- Skip mentioning data formats and schemas
- Ignore data latency requirements
- Overcomplicate with too many transformations

---

## Tips for Effective Data Flow Diagrams

1. **Identify Sources**: Clearly show all data entry points
2. **Track Transformations**: Each processing step should transform/enrich data
3. **Show Storage Tiers**: Raw, processed, aggregated, cached
4. **Error Handling**: Include validation and rejection paths
5. **Scale Indicators**: Show data volume and frequency
6. **Latency Labels**: Indicate real-time vs batch, SLAs
7. **Quality Gates**: Mark where validation occurs

---

**Template Version**: 1.0
**Best for**: Data architecture, ETL/ELT documentation, analytics pipeline design, data governance
