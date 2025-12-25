# System Design

# System Design – Highly Scalable Systems

## Table of Contents

1. [Foundations of Scalability – Q&A](#foundations-of-scalability--qa)
2. [Vertical vs Horizontal Scaling](#vertical-vs-horizontal-scaling)
3. [Load Balancing](#load-balancing)
4. [Caching Strategies](#caching-strategies)
5. [Databases, Sharding, and Replication](#databases-sharding-and-replication)
6. [Message Queues and Asynchronous Processing](#message-queues-and-asynchronous-processing)
7. [CDNs and Global Distribution](#cdns-and-global-distribution)
8. [CAP Theorem and Consistency Models](#cap-theorem-and-consistency-models)
9. [High-Level System Design Diagrams (Mermaid)](#high-level-system-design-diagrams-mermaid)
10. [Example Designs – URL Shortener, News Feed, Ride Sharing](#example-designs--url-shortener-news-feed-ride-sharing)
11. [Observability: Logging, Metrics, and Tracing](#observability-logging-metrics-and-tracing)
12. [System Design Interview Questions & Answers](#system-design-interview-questions--answers)

---

## Foundations of Scalability – Q&A

### Q1. What is scalability in system design?

**Scalability** is the ability of a system to handle increasing load – more users, more requests, more data – by adding resources, without requiring major redesign or sacrificing performance.

A scalable system:

* Maintains acceptable response times as traffic grows.
* Allows capacity to be increased in a **predictable, cost-effective** way.
* Can be expanded along different dimensions (compute, storage, network).

---

### Q2. What are the main factors that influence scalability?

Key factors:

* **Architecture choice** – monolith vs microservices.
* **Data model and database design** – indexes, normalization/denormalization.
* **Caching** – how effectively we avoid recomputing or refetching.
* **Load distribution** – via load balancers and partitioning.
* **Concurrency handling** – thread model, async I/O, connection pooling.
* **Bottlenecks** – the slowest component limits performance.

Understanding where the system will experience pressure is critical to designing scalability.

---

### Q3. What are the typical scalability goals?

Common goals:

* Maintain **low latency** (e.g. p95 < 200 ms).
* Maintain **high availability** (e.g. 99.9% or 99.99%).
* Handle **peak load** (e.g. 10x traffic spikes) gracefully.
* Scale **horizontally** across multiple machines or regions.
* Keep **costs under control** while scaling.

---

## Vertical vs Horizontal Scaling

### Q4. What is vertical scaling?

**Vertical scaling (scaling up)** means adding more resources to a single machine: more CPU cores, more RAM, faster disks.

* Pros: simpler architecture, fewer nodes to manage.
* Cons: hard limits (max machine size), not always cost-effective, single point of failure.

### Q5. What is horizontal scaling?

**Horizontal scaling (scaling out)** means adding more machines or instances and distributing load across them.

* Pros: increases capacity by adding more nodes, tolerates failure of individual nodes.
* Cons: requires distributed system design (state sharing, coordination, consistency).

Modern large-scale systems overwhelmingly rely on **horizontal scaling**.

---

## Load Balancing

### Q6. What is a load balancer and why is it important?

A **load balancer** distributes incoming network traffic across multiple servers to achieve:

* Better utilization of resources.
* Increased throughput and capacity.
* Improved availability and fault tolerance.

If one server goes down, the load balancer can stop sending traffic to it.

### Q7. What load balancing strategies are common?

* **Round Robin** – each request goes to the next server in order.
* **Least Connections** – send to server with fewest active connections.
* **IP Hash** – choose server based on client IP hash (for simple session stickiness).
* **Weighted Round Robin** – some servers get more traffic based on weights.

### Simple Load Balancer Diagram (Mermaid)

`mermaid
graph LR
C[Clients] --> LB[Load Balancer]
LB --> S1[Server 1]
LB --> S2[Server 2]
LB --> S3[Server 3]`

---

## Caching Strategies

### Q8. What is caching in system design?

**Caching** is storing the result of expensive operations (database queries, computations, API calls) in a fast storage layer so future requests can be served quickly.

Benefits:

* Reduces load on the database/backend.
* Reduces latency for clients.
* Can dramatically increase throughput.

### Q9. What are common caching layers?

* **Client-side cache** – browser caching of static assets.
* **CDN** – network of edge servers caching static and sometimes dynamic content.
* **Application cache** – in-process caches.
* **Distributed cache** – Redis, Memcached, used by multiple app instances.
* **Database cache** – query caching within the DB engine.

### Q10. What are typical cache invalidation strategies?

* **Time-based** – TTL (time-to-live) expiration.
* **Write-through** – data written to cache and DB simultaneously.
* **Write-back** – data written to cache first, flushed to DB later.
* **Explicit invalidation** – cache entries removed when data changes.

Cache invalidation is one of the hardest problems in system design. Good strategies balance freshness and performance.

---

## Databases, Sharding, and Replication

### Q11. What is database replication?

**Replication** means maintaining copies of the same data on multiple database servers.

* **Primary–Replica (Master–Slave)**:
* Primary handles writes; replicas handle reads.
* Improves read scalability and availability.
* **Multi-primary (Multi-master)**:
* Multiple nodes accept writes; requires conflict resolution.
* Increased complexity and careful design needed.

### Q12. What is sharding (partitioning)?

**Sharding** means splitting data horizontally across multiple database instances based on a shard key (e.g. user ID).

* Each shard holds a subset of rows.
* Improves both read and write scalability by reducing the data each node handles.
* Requires a strategy to map keys to shards (hashing, range partitioning, etc.).

### Q13. What are common sharding strategies?

* **Range-based** – users 1–1M on shard 1, 1M–2M on shard 2.
* **Hash-based** – hash(user\_id) mod N chooses shard.
* **Directory-based** – a lookup service tells you which shard holds which key.

---

## Message Queues and Asynchronous Processing

### Q14. Why do we use message queues?

Message queues (like Kafka, RabbitMQ, AWS SQS) decouple producers from consumers and enable **asynchronous processing**.

Benefits:

* Smooth out traffic spikes (buffering).
* Increase reliability (messages not lost if consumer is down).
* Allow slower tasks to be processed in background (emails, report generation).

### Q15. What does a typical queue-based architecture look like?

`mermaid
graph LR
C[Client] --> API[API Service]
API --> MQ[Message Queue]
MQ --> W1[Worker 1]
MQ --> W2[Worker 2]
W1 --> DB[(Database)]
W2 --> DB`

The API responds quickly after enqueuing work; workers process tasks asynchronously.

---

## CDNs and Global Distribution

### Q16. What is a CDN?

A **Content Delivery Network (CDN)** is a distributed network of edge servers that cache static (and some dynamic) content closer to users around the globe.

Benefits:

* Reduces latency by serving content from geographically closer locations.
* Offloads traffic from the origin server.
* Improves user experience for static assets (images, JS, CSS, videos).

### Q17. When should you use a CDN?

Any time you serve static assets or large media files at scale, or when users are globally distributed.

---

## CAP Theorem and Consistency Models

### Q18. What is the CAP theorem?

The **CAP theorem** states that in a distributed data store, you can only fully achieve two of the following three properties at the same time:

* **Consistency (C)** – every read receives the latest write or an error.
* **Availability (A)** – every request receives a non-error response, without guarantee it contains the latest write.
* **Partition Tolerance (P)** – the system continues to operate despite network partitions.

Since network partitions are unavoidable in distributed systems, you must trade between **strong consistency** and **high availability** during partitions.

### Q19. What is eventual consistency?

**Eventual consistency** means that, given enough time and no new updates, all replicas will converge to the same value. Reads may see stale data, but the system is easier to scale and more available.

Used by many large-scale systems where slight staleness is acceptable (counters, feeds, analytics).

---

## High-Level System Design Diagrams (Mermaid)

### 1. Classic Web Application

`mermaid
graph LR
U[User] --> LB[Load Balancer]
LB --> A1[App Server 1]
LB --> A2[App Server 2]
A1 --> Cache[(Redis Cache)]
A2 --> Cache
Cache --> DB[(Primary DB)]
DB --> R1[(Read Replica)]
DB --> R2[(Read Replica)]`

---

### 2. Microservices with API Gateway

`mermaid
graph LR
C[Clients] --> GW[API Gateway]
GW --> S1[User Service]
GW --> S2[Order Service]
GW --> S3[Payment Service]
S1 --> DB1[(User DB)]
S2 --> DB2[(Order DB)]
S3 --> DB3[(Payment DB)]`

Each service has its own database (**database per service**), reducing coupling and improving scalability.

---

### 3. Global Architecture with CDN and Queue

`mermaid
graph LR
U[User] --> CDN[CDN/Edge Cache]
CDN --> LB[Load Balancer]
LB --> APP[Application Servers]
APP --> MQ[Message Queue]
MQ --> W[Workers]
APP --> DB[(Database)]
W --> DB`

This pattern is common for high-traffic web apps where writes are offloaded to background workers.

---

## Example Designs – URL Shortener, News Feed, Ride Sharing

### URL Shortener – High Level

Key requirements:

* Shorten long URLs to unique short codes.
* Fast redirects.
* Analytics (click counts).
* High read volume.

Basic design:

* Store mappings: `short_code -> long_url`.
* Use cache to speed up reads.
* Use DB with auto-increment ID or hash-based keys.

`mermaid
graph LR
C[Client] --> API[URL API]
API --> Cache[(Redis)]
API --> DB[(URLs DB)]
Cache --> DB`

Redirect flow:

1. Client hits `https://short.ly/abc123`.
2. API checks cache for `abc123`.
3. If not present, check DB, then populate cache.
4. Return HTTP redirect (`301/302`) to the long URL.

---

### News Feed – High Level

Simplified design:

* **Write path**: when user posts, write to a posts store and fan-out to followers’ feeds (for small–medium scale) or compute feeds on read (for huge scale).
* **Read path**: read latest posts from feed store, use cache for hot feeds.

Challenges:

* High write and read volume.
* Ranking algorithms.
* Personalized feeds.

---

### Ride Sharing (e.g., Uber) – Very Simplified View

Key pieces:

* **Real-time location tracking** (drivers & riders).
* **Matching service** – match riders with nearby drivers.
* **Pricing and surge logic**.
* **Trip management**, **payments**, **notifications**.

Design aspects:

* Use **Geo-distributed stores** and **geo-indexing** (e.g. geohash).
* Use **message queues** for handling events (ride requested, driver accepted).
* Use **WebSockets** or long polling for real-time updates.

---

## Observability: Logging, Metrics, and Tracing

### Q20. Why is observability important?

As systems become distributed and complex, we need visibility to:

* Detect issues early.
* Understand performance bottlenecks.
* Debug failures across multiple services.

### Q21. What are the pillars of observability?

1. **Logs** – detailed event records (e.g., request logs, error logs).
2. **Metrics** – numeric time series (e.g., requests/sec, latency, CPU).
3. **Traces** – distributed traces showing a request’s path through microservices.

Tools: Prometheus, Grafana, ELK/EFK, Jaeger, Zipkin, CloudWatch, Datadog.

---

## System Design Interview Questions & Answers

### Q1. How would you design a URL shortener? (high level answer)

Key points:

* API to create short URLs: `POST /shorten`.
* API to redirect: `GET /{short_code}`.
* Data model: mapping from short code to original URL, plus metadata.
* Use **hash function** or base62 encoding of an ID to create short codes.
* Use **cache** for redirects (short\_code → long\_url).
* Plan for **analytics**, **rate limiting**, and preventing abuse.
* Consider sharding DB by short code prefix for very large scale.

### Q2. How would you design a rate limiter?

Common approaches:

* **Token Bucket** or **Leaky Bucket** algorithms.
* Store counters in Redis with TTL.
* Key format: `rate:{user_id}:{time_window}`.
* On each request, increment the counter; if above threshold, reject with `429 Too Many Requests`.

### Q3. How would you design a highly available database?

* Use **replication**: primary for writes, replicas for reads.
* Use **automatic failover**: if primary dies, promote a replica.
* Store data across **multiple availability zones** or regions.
* Use **backups** and **point-in-time recovery**.
* For global apps, consider **multi-region replication**.

### Q4. How do you decide between SQL and NoSQL?

Consider:

* Data model – relational vs document/graph/key-value.
* Query patterns – complex joins vs simple lookups.
* Consistency and transaction requirements.
* Scalability needs – some NoSQL stores scale horizontally more easily.
* Existing ecosystem, tooling, and team expertise.

Often, large systems use a mix of both.

### Q5. How would you design a chat system? (very high level)

* Use **WebSockets** or long-lived connections for real-time messaging.
* Partition users or chat rooms across servers.
* Use **message queue** or pub/sub for delivering messages.
* Persist messages in a database for history.
* Use **presence service** to track who is online.
* Handle **typing indicators**, **read receipts**, **delivery status**.

### Q6. How do you handle hot keys or hotspots in a distributed cache?

* Add another layer of **local cache** inside the app process.
* Use **sharding** with consistent hashing to distribute load.
* Replicate hot keys across multiple nodes.
* Adjust data model to avoid extreme skew.

### Q7. What’s your strategy for breaking a monolith into microservices?

* Identify bounded contexts or modules with clear boundaries.
* Extract services one at a time, starting with less risky domains.
* Introduce an **API Gateway** as a single entry point.
* Ensure good **observability** and **automation** before migration.
* Maintain data consistency using events or saga patterns.