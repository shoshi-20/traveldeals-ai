# TravelDeals AI

## Project Overview

TravelDeals AI is a multi-tenant travel recommendation platform that helps merchants surface personalized offers through semantic search and LLM-based ranking. It serves two primary users: merchants (dashboard for managing deals and branding) and end customers (embedded search widget for natural-language deal discovery). What makes it unique is the combination of merchant-scoped vector search, AI reranking with explainable one-line pitches and white-label widget delivery from the same codebase.

## Architecture Diagram

```text
Architecture: TravelDeals AI

	┌─────────────────────────────────────────────────────────────────┐
	│                        CLIENT LAYER                              │
	│   [Merchant Portal]              [Embedded Widget]               │
	│   Next.js App Router             Next.js Route (iframe)          │
	│   /app/dashboard/                /app/widget/[merchantId]/       │
	└───────────────────────┬──────────────────┬───────────────────────┘
													│  HTTPS REST       │  HTTPS REST
	┌───────────────────────▼──────────────────▼───────────────────────┐
	│                   APPLICATION LAYER                               │
	│              Django + Django REST Framework                       │
	│   /api/auth/   /api/merchants/  /api/deals/  /api/deals/search/  │
	└──────────────┬──────────────────────────────────┬────────────────┘
								 │ SQL + pgvector                    │ HTTPS
	┌──────────────▼──────────────┐   ┌──────────────▼────────────────┐
	│         DATA LAYER           │   │       AI LAYER (External)     │
	│   PostgreSQL 16              │   │   OpenAI API                  │
	│   + pgvector extension       │   │   text-embedding-3-small      │
	│   deals table + embeddings   │   │   gpt-4o-mini                      │
	└─────────────────────────────┘   └───────────────────────────────┘

	All services run in Docker containers, orchestrated with docker-compose
```

## AI Pipeline (4 Steps)

1. Embed query: The user query is converted into a dense vector using `text-embedding-3-small`.
2. Vector search: The backend performs merchant-scoped cosine similarity search in pgvector to retrieve the most semantically relevant deals.
3. LLM rerank: The top candidates are sent to `gpt-4o-mini`, which reranks results and generates a short, human-readable pitch for each deal.
4. Return results: The API returns the ranked deals plus AI-generated pitches to the widget/dashboard caller.

## Multi-Tenancy Design

The platform uses per-merchant API keys passed as `Authorization: Api-Key <key>`. On each request, the backend resolves the key to an active merchant and scopes all data access to that merchant only. This pattern enforces tenant isolation at the API layer so one merchant can never read or mutate another merchant's deals.

## Local Setup Instructions

### Prerequisites

- Docker Desktop
- OpenAI API key in `.env`

### Start the stack

```bash
docker-compose up --build
```

### Run database and data bootstrap (in order)

```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_deals
docker compose exec backend python manage.py embed_deals
```

### Local URLs

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## What I Would Add Next

- Deploy on Azure
- Redis caching: cache frequent query embeddings and top result sets to reduce latency and token cost.
- Streaming LLM responses: stream rerank or explanation text for faster perceived performance.
- Rate limiting per merchant: protect against abuse and enforce fair usage by API key.
- Analytics dashboard: merchant-level insights for query volume, conversion signals, and top-performing destinations.
