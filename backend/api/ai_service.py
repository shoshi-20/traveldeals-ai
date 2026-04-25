from openai import OpenAI
from pgvector.django import CosineDistance
from .models import Deal
import json

client = OpenAI()


def get_query_embedding(query_text: str) -> list[float]:
    """Convert the user's search query to an embedding vector."""
    response = client.embeddings.create(
        model="text-embedding-3-small", input=query_text
    )
    return response.data[0].embedding


def semantic_search(query_embedding: list[float], merchant_id: str, top_k: int = 10):
    """
    Find the top_k deals closest to the query embedding.
    """
    deals = (
        Deal.objects.filter(merchant_id=merchant_id, is_embedded=True)
        .annotate(distance=CosineDistance("embedding", query_embedding))
        .order_by("distance")[:top_k]
    )
    # What about fuzzy matching by price? Could be a secondary sort after embedding distance.
    return list(deals)


RERANK_PROMPT = """
You are a travel deals assistant. The user searched for: "{query}"

Below are {count} travel deals retrieved by semantic search.
Your tasks:
1. Re-rank them from most to least relevant to the user's query.
2. For each deal, write exactly one sentence explaining why it matches the query.
   Be specific and personalized to what the user asked for.
   Keep each pitch under 20 words.

Return ONLY valid JSON — no other text before or after:
[
  {{"deal_id": "<uuid>", "pitch": "<one sentence>"}},
  ...
]

Deals:
{deals_text}
"""


def llm_rerank(query: str, deals: list) -> list[dict]:
    """
    Send the top deals to llm for reranking and pitch generation.
    """
    deals_text = "\n".join(
        [
            f"ID: {d.id} | Title: {d.title} | Destination: {d.destination} | Description: {d.description[:300]} | Price: ${d.price}"
            for d in deals
        ]
    )

    prompt = RERANK_PROMPT.format(query=query, count=len(deals), deals_text=deals_text)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=800,
    )

    raw = response.choices[0].message.content.strip()
    print("LLM Rerank Raw Response:", raw)
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw)
