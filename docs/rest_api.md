# Rest Api

# REST API

## Table of Contents

1. [REST Fundamentals – Q&A](#rest-fundamentals--qa)
2. [HTTP Methods and Resources](#http-methods-and-resources)
3. [Requests, Responses, and Status Codes](#requests-responses-and-status-codes)
4. [Authentication and Authorization](#authentication-and-authorization)
5. [REST API Design Best Practices](#rest-api-design-best-practices)
6. [Versioning Strategies](#versioning-strategies)
7. [Error Handling and Validation](#error-handling-and-validation)
8. [Caching, Rate Limiting, and Pagination](#caching-rate-limiting-and-pagination)
9. [REST Architecture Diagrams (Mermaid)](#rest-architecture-diagrams-mermaid)
10. [Code Examples – FastAPI](#code-examples--fastapi)
11. [Code Examples – Flask](#code-examples--flask)
12. [AWS Reference Architecture – API Gateway + Lambda + DynamoDB](#aws-reference-architecture--api-gateway--lambda--dynamodb)
13. [REST API Interview Questions & Answers](#rest-api-interview-questions--answers)

---

## REST Fundamentals – Q&A

### Q1. What is a RESTful API?

A **RESTful API** (Representational State Transfer API) is a way for two computer systems to communicate over HTTP using a set of constraints defined by the REST architectural style. The API exposes **resources** (such as users, orders, or products) via unique URLs, and clients interact with these resources using standard HTTP methods like `GET`, `POST`, `PUT`, and `DELETE`.

Key properties of a RESTful API:

* Uses **HTTP** as the application protocol.
* Treats everything as a **resource** identified by a URL.
* Is typically **stateless** – the server does not store client session between requests.
* Favors **uniform interfaces** and uses standard status codes and formats (often JSON).
* Is well-suited for **web, mobile, and microservices** architectures.

### Q2. What is an API in general?

An **API (Application Programming Interface)** is a contract that defines how different software components can interact. It specifies:

* **What** can be done (operations/endpoints).
* **How** to call it (inputs, headers, authentication).
* **What** is returned (output schema, status codes).

APIs allow you to integrate systems without exposing internal implementation details. REST is one popular style for designing APIs.

### Q3. What is REST as an architectural style?

**REST** is not a protocol; it is an architectural style that defines a set of constraints for scalable and maintainable network systems. Some key REST constraints:

1. **Client–Server** – clients and servers are separate; the client handles UI, the server handles data and business logic.
2. **Stateless** – each request from client to server must contain all information needed to understand and process it; no session stored on server.
3. **Cacheable** – responses should define whether they are cacheable; caching can dramatically improve performance.
4. **Uniform Interface** – consistent, predictable resource URIs, HTTP methods, and response formats.
5. **Layered System** – intermediaries like load balancers, proxies, and gateways can be placed between client and server.

Following these constraints makes systems easier to scale and evolve.

### Q4. How do RESTful APIs work in practice?

Conceptually, a RESTful API works like this:

1. A **client** (browser, mobile app, backend service) sends an HTTP request to the API’s URL.
2. The request includes method, headers, path, query parameters, and optionally a body.
3. The **server** authenticates the request, validates inputs, and performs the required action (read/write/update/delete).
4. The server returns an HTTP response with:
5. A status code (e.g. `200 OK`, `201 Created`, `400 Bad Request`, `404 Not Found`).
6. A response body (often JSON).
7. Response headers (e.g. content type, cache headers).

Because the server is stateless, each request is independent.

### Q5. What are resources and resource representations?

A **resource** is any entity that the server manages: users, products, orders, blog posts, etc. Each resource has a unique URL, such as:

* `/users` – collection of users
* `/users/42` – specific user with ID 42
* `/orders/abc123` – specific order with ID `abc123`

The **representation** of a resource is how it is serialized over the wire – typically **JSON**, but it could be XML, YAML, or even binary formats. For example:

`json
{
"id": 42,
"name": "Alice",
"email": "alice@example.com"
}`

This is one representation of the `User` resource.

### Q6. What are the main HTTP methods used in REST?

Common HTTP methods and their typical REST semantics:

* `GET` – Read a resource or collection (no side effects).
* `POST` – Create a new resource or perform a non-idempotent operation.
* `PUT` – Replace the entire resource with the provided representation.
* `PATCH` – Partially update a resource.
* `DELETE` – Remove a resource.

Idempotency matters:

* **Idempotent methods**: `GET`, `PUT`, `DELETE` (calling them multiple times has same effect as once).
* **Non-idempotent**: `POST` (calling multiple times may create multiple resources).

### Q7. What does a REST API request typically contain?

A typical REST request has:

1. **HTTP method** – e.g., `GET`, `POST`.
2. **URL** – e.g., `https://api.example.com/v1/users?limit=10`.
3. **Headers** – metadata such as `Authorization`, `Content-Type`, `Accept`, etc.
4. **Query parameters** – for filtering and pagination (e.g., `?page=2&limit=20`).
5. **Body** – for `POST`, `PUT`, or `PATCH` requests (usually JSON).

Example `POST` request (conceptual):

```http
POST /v1/users HTTP/1.1
Host: api.example.com
Authorization: Bearer
Content-Type: application/json

{
"name": "Alice",
"email": "alice@example.com"
}
```

### Q8. What does a REST API response typically contain?

A typical REST response includes:

1. **Status line** – `HTTP/1.1 200 OK`
2. **Response headers** – `Content-Type`, caching headers, CORS headers, etc.
3. **Body** – resource data or error information.

Example success response:

```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /v1/users/42

{
"id": 42,
"name": "Alice",
"email": "alice@example.com"
}
```

Example error response:

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
"error": "VALIDATION\_ERROR",
"message": "Field 'email' must be a valid email address."
}
```

### Q9. What authentication mechanisms are common in REST APIs?

Common options:

1. **API Keys**
2. Simple static tokens passed in headers or query parameters.
3. Example: `X-API-Key: <key>`.
4. **HTTP Basic Auth**
5. Username and password Base64-encoded in `Authorization` header.
6. Suitable mostly for internal systems or via HTTPS only.
7. **Bearer Tokens / JWT**
8. Short-lived tokens passed as `Authorization: Bearer <token>`.
9. JWTs contain claims about the user and can be verified with cryptographic signatures.
10. **OAuth 2.0**
11. Standard for delegated authorization.
12. Used by many identity providers (Google, GitHub, etc.).
13. **AWS Signature Version 4**
14. AWS-specific request signing mechanism used for calling AWS APIs securely.

### Q10. How does AWS help with RESTful APIs?

AWS provides several services that simplify building and managing RESTful APIs:

* **Amazon API Gateway** – create, publish, secure, and monitor APIs at scale.
* **AWS Lambda** – run serverless functions for your API backend without managing servers.
* **Amazon EC2 / ECS / EKS** – run containerized or VM-based services behind REST APIs.
* **Amazon Cognito** – manage user authentication and authorization.
* **Amazon CloudWatch** – monitor API performance and errors.
* **AWS WAF & Shield** – protect APIs from common web exploits and DDoS attacks.

API Gateway can integrate with Lambda, EC2, and many other AWS services to create a complete, scalable REST architecture.

---

## HTTP Methods and Resources

Example resource design for a simple blog API:

* `GET /posts` – list posts
* `POST /posts` – create a new post
* `GET /posts/{id}` – get a single post
* `PUT /posts/{id}` – replace a post
* `PATCH /posts/{id}` – partially update a post
* `DELETE /posts/{id}` – delete a post

Use **nouns** for resources, not verbs. For actions that don’t fit CRUD cleanly, you can use sub-resources or action-style endpoints, for example:

* `POST /posts/{id}/publish`
* `POST /posts/{id}/like`

---

## Requests, Responses, and Status Codes

Some important HTTP status codes for REST APIs:

* `200 OK` – success for `GET`, `PUT`, `PATCH`, or `DELETE`.
* `201 Created` – resource successfully created (often used with `POST`).
* `204 No Content` – request succeeded but no body (e.g. delete).
* `400 Bad Request` – invalid input from client.
* `401 Unauthorized` – request lacks valid authentication credentials.
* `403 Forbidden` – client is authenticated but not allowed.
* `404 Not Found` – requested resource does not exist.
* `409 Conflict` – resource conflict (e.g., duplicate key).
* `429 Too Many Requests` – rate limiting.
* `500 Internal Server Error` – unexpected server issue.
* `503 Service Unavailable` – server overloaded or under maintenance.

Consistent use of status codes improves API usability and debuggability.

---

## Authentication and Authorization

### API Key Example (header-based)

`http
GET /v1/orders HTTP/1.1
Host: api.example.com
X-API-Key: your-api-key-here`

### Bearer Token / JWT Example

`http
GET /v1/profile HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### Basic Auth Example

`http
GET /v1/admin HTTP/1.1
Host: api.example.com
Authorization: Basic dXNlcjpwYXNzd29yZA==`

Best practices:

* Always use **HTTPS** for authenticated endpoints.
* Prefer **short-lived tokens** over long-lived static secrets.
* Scope tokens/keys to minimal permissions (least privilege).
* Rotate keys and tokens regularly.

---

## REST API Design Best Practices

* Use **resource-based URLs** and **plural nouns** (e.g. `/users`, `/orders`).
* Follow **consistent naming conventions** (snake\_case or camelCase) in JSON.
* Use **query parameters** for filtering, sorting, and pagination.
* Support **pagination** for large collections (e.g. `page`, `limit`, `cursor`).
* Return **clear error messages** with machine-readable codes.
* Provide **API documentation** (OpenAPI/Swagger).
* Keep services **stateless** and externalize session state (e.g., Redis).
* Consider **idempotency** for operations like payments or critical updates.

---

## Versioning Strategies

Common patterns:

1. **URL Versioning (most common)**
2. `/v1/users`, `/v2/users`
3. Simple and visible; easy to route.
4. **Header Versioning**
5. `Accept: application/vnd.myapi.v1+json`
6. Cleaner URLs but more complex routing.
7. **Query Parameter Versioning**
8. `/users?version=1`
9. Generally less preferred but sometimes used.

Best practice: use URL versioning for clarity, especially in public APIs.

---

## Error Handling and Validation

Typical error response shape:

`json
{
"error": "VALIDATION_ERROR",
"message": "Field 'email' must be a valid email address.",
"details": [
{ "field": "email", "issue": "INVALID_FORMAT" }
]
}`

Guidelines:

* Validate inputs at the API boundary.
* Use appropriate HTTP status codes.
* Never expose internal stack traces or secrets in error messages.
* Log detailed errors on the server for debugging.

---

## Caching, Rate Limiting, and Pagination

### Caching

Use caching for frequently read data:

* HTTP caching headers: `ETag`, `Cache-Control`, `Last-Modified`.
* Client-side cache and CDN caching for static or rarely changing data.
* Server-side caches (Redis, Memcached) for expensive queries.

### Rate Limiting

Protect APIs from abuse and manage resources by applying:

* Per-IP or per-key rate limits (e.g., 1000 requests/minute).
* Return `429 Too Many Requests` when limits are exceeded.
* Use headers like `X-RateLimit-Limit`, `X-RateLimit-Remaining`.

### Pagination

For large datasets, return results in pages.

Example:

`http
GET /v1/users?page=2&limit=20`

Or cursor-based:

`http
GET /v1/users?cursor=eyJpZCI6NDJ9`

Always return pagination metadata:

`json
{
"data": [/* users */],
"page": 2,
"limit": 20,
"total": 105,
"has_next": true
}`

---

## REST Architecture Diagrams (Mermaid)

### 1. Basic Client–Server REST Flow

```mermaid
sequenceDiagram
participant C as Client
participant API as REST API Server
participant DB as Database

```
C->>API: HTTP Request (GET /users/42)
API->>DB: Query user with id=42
DB-->>API: User data
API-->>C: 200 OK + JSON body
```

```

### 2. REST API Behind Load Balancer

`mermaid
graph LR
C[Clients] --> LB[Load Balancer]
LB --> S1[API Server 1]
LB --> S2[API Server 2]
LB --> S3[API Server 3]
S1 --> DB[(Database)]
S2 --> DB
S3 --> DB`

---

## Code Examples – FastAPI

### Minimal FastAPI REST API

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Users API", version="1.0.0")

class User(BaseModel):
id: int
name: str
email: str

# In-memory "database"

USERS\_DB = {
1: User(id=1, name="Alice", email="alice@example.com"),
2: User(id=2, name="Bob", email="bob@example.com"),
}

@app.get("/users", response\_model=List[User])
def list\_users():
return list(USERS\_DB.values())

@app.get("/users/{user\_id}", response\_model=User)
def get\_user(user\_id: int):
user = USERS\_DB.get(user\_id)
if not user:
raise HTTPException(status\_code=404, detail="User not found")
return user

@app.post("/users", response\_model=User, status\_code=201)
def create\_user(user: User):
if user.id in USERS\_DB:
raise HTTPException(status\_code=409, detail="User already exists")
USERS\_DB[user.id] = user
return user

@app.put("/users/{user\_id}", response\_model=User)
def replace\_user(user\_id: int, user: User):
if user\_id != user.id:
raise HTTPException(status\_code=400, detail="ID mismatch")
USERS\_DB[user\_id] = user
return user

@app.delete("/users/{user\_id}", status\_code=204)
def delete\_user(user\_id: int):
if user\_id not in USERS\_DB:
raise HTTPException(status\_code=404, detail="User not found")
del USERS\_DB[user\_id]
return None
```

Run with:

`bash
uvicorn main:app --reload`

FastAPI automatically generates docs:

* Swagger UI at `/docs`
* ReDoc at `/redoc`

---

### FastAPI with Simple API Key Auth

```python
from fastapi import Depends, FastAPI, HTTPException, Header

API\_KEY = "super-secret-key"
API\_KEY\_HEADER = "X-API-Key"

app = FastAPI()

def verify\_api\_key(x\_api\_key: str = Header(..., alias=API\_KEY\_HEADER)):
if x\_api\_key != API\_KEY:
raise HTTPException(status\_code=401, detail="Invalid API key")
return True

@app.get("/secure-data", dependencies=[Depends(verify\_api\_key)])
def secure\_data():
return {"secret": "42"}
```

Client must send:

`http
X-API-Key: super-secret-key`

---

## Code Examples – Flask

### Minimal Flask REST API

```python
from flask import Flask, jsonify, request, abort

app = Flask(**name**)

USERS\_DB = {
1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
}

@app.route("/users", methods=["GET"])
def list\_users():
return jsonify(list(USERS\_DB.values()))

@app.route("/users/", methods=["GET"])
def get\_user(user\_id):
user = USERS\_DB.get(user\_id)
if not user:
abort(404)
return jsonify(user)

@app.route("/users", methods=["POST"])
def create\_user():
data = request.get\_json()
if not data or "id" not in data:
abort(400)
user\_id = data["id"]
if user\_id in USERS\_DB:
abort(409)
USERS\_DB[user\_id] = data
return jsonify(data), 201

@app.route("/users/", methods=["DELETE"])
def delete\_user(user\_id):
if user\_id not in USERS\_DB:
abort(404)
del USERS\_DB[user\_id]
return "", 204

if **name** == "**main**":
app.run(debug=True)
```

---

## AWS Reference Architecture – API Gateway + Lambda + DynamoDB

### Mermaid Diagram

```mermaid
graph LR
C[Clients (Web/Mobile)] --> AGW[Amazon API Gateway]
AGW --> L1[AWS Lambda Function]
L1 --> DDB[(Amazon DynamoDB)]

subgraph AWS Cloud
AGW
L1
DDB
end
```

High-level flow:

1. Client calls API endpoint exposed by **API Gateway**.
2. API Gateway forwards the request to a **Lambda function**.
3. Lambda executes business logic and calls **DynamoDB** to read/write data.
4. Lambda returns response to API Gateway, which returns it to the client.

This architecture is **serverless**, highly scalable, and you only pay for usage.

---

## REST API Interview Questions & Answers

### Q1. What is the difference between REST and SOAP?

* **Protocol vs Style**: SOAP is a protocol with strict standards; REST is an architectural style.
* **Data Format**: SOAP uses XML; REST usually uses JSON but is flexible.
* **Complexity**: SOAP supports built-in standards for security and transactions; REST is simpler and lightweight.
* **Use Cases**: SOAP often used in enterprise, legacy, or transactional systems; REST is most common for web/mobile APIs.

### Q2. Why are REST APIs typically stateless?

Statelessness means each request contains all information required to process it. This:

* Makes scaling easier (any server can handle any request).
* Avoids session affinity and complex session replication.
* Improves reliability and fault tolerance.

If state is needed (e.g. user session), store it client-side (JWT) or in a shared store (Redis), not in server memory.

### Q3. How do you design idempotent endpoints?

Use HTTP methods according to their semantics:

* `GET`, `PUT`, and `DELETE` should be idempotent.
* For operations like payment, use **idempotency keys**: client sends a unique key, and server ensures the operation is executed at most once per key.

### Q4. How do you secure a REST API?

* Always use **HTTPS**.
* Use **authentication** (API keys, OAuth2, JWT).
* Apply **authorization** (role-based or attribute-based).
* Validate and sanitize all inputs.
* Implement **rate limiting** and **WAF** protections.
* Log and monitor suspicious activity.

### Q5. What is HATEOAS?

HATEOAS (Hypermedia as the Engine of Application State) is a REST constraint where the server includes hyperlinks in responses to indicate valid next actions. Example:

`json
{
"id": 42,
"name": "Alice",
"links": [
{ "rel": "self", "href": "/users/42" },
{ "rel": "orders", "href": "/users/42/orders" }
]
}`

This makes the API more discoverable and self-documenting.

### Q6. How would you implement pagination in a REST API?

Options:

* **Offset-based**: `/users?page=2&limit=20`. Easy but can be slow for large offsets.
* **Cursor-based**: `/users?cursor=abc123&limit=20`. More scalable; cursor encodes position.

Always include metadata so clients know how to fetch the next/previous pages.

### Q7. What are some common pitfalls when designing REST APIs?

* Overloading `POST` for everything.
* Using verbs in endpoint paths (`/createUser`) instead of nouns (`/users`).
* Not using proper HTTP status codes.
* Returning inconsistent data shapes.
* Coupling API too tightly to internal database structures.
* Ignoring versioning from the start.