# Reference: Service Map

Key services involved in the X algorithm architecture, mapped to their role in the `x-algorithm` repository.

| Service | Internal Name | Tech Stack | Primary Responsibility |
| :--- | :--- | :--- | :--- |
| **HomeMixer** | `home-mixer` | Scala | **Orchestrator**. The "Brain" of the For You feed. Runs the ProductMixer pipelines. |
| **Content Recommender** | `cr-mixer` | Scala/Rust | **Out-of-Network**. Manages retrieval logic for content outside the user's graph. |
| **Search Index** | `earlybird` | Java/Scala | **Retrieval**. Real-time Lucene-based index for tweets. Performs "Light Ranking". |
| **User Signal** | `user-signal-service` | Scala | **Data**. Central platform for retrieving explicit (likes) and implicit (dwell time) signals. |
| **Graph Engine** | `social-graph` / `thunder` | Rust | **Graph**. Manages following lists and mute/block relationships. |
| **Model Serving** | `navi` | Rust | **ML Compute**. Hosts the Heavy Ranker neural networks. Optimized for high-throughput inference. |
| **Feature Store** | `twhin` / `simclusters` | Scala/Python | **Embeddings**. Provides dense vector representations of users and communities. |
| **Tweet Store** | `tweetypie` | Scala | **Object Store**. The canonical source of truth for a Tweet object (text, media entities). |
| **Safety Engine** | `visibility-lib` | Rust | **Filtering**. Central library for legal compliance, safety labeling, and visibility rules. |
| **KV Store** | `manhattan` | C++ | **Storage**. Distributed Key-Value store used for user profiles and interaction counts. |

### Technical Interaction Model

1.  **Thrift/Finagle:** All inter-service communication uses Apache Thrift over Finagle.
2.  **Strato:** A catalog service often used as a query layer over `Manhattan` and `Tweetypie` to simplify data fetching.
3.  **Data Flow:**
    * `HomeMixer` (Scala) -> Calls `Earlybird`/`Cr-Mixer` (Retrieval)
    * `HomeMixer` -> Calls `SignalService` (Feature Hydration)
    * `HomeMixer` -> Calls `Navi` (Scoring)
    * `Navi` returns Scores -> `HomeMixer` sorts and filters.
