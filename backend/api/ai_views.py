from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .authentication import MerchantAPIKeyAuthentication
from .ai_service import get_query_embedding, semantic_search, llm_rerank
from .models import Deal, UserQuery
from .serializers import DealSerializer


class SearchView(APIView):
    authentication_classes = [MerchantAPIKeyAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(_, request):
        query = request.data.get("query", "").strip()
        if not query:
            return Response({"error": "query is required"}, status=400)

        merchant = request.auth
        if not merchant:
            return Response({"error": "Invalid API key"}, status=401)

        # Step 1: Embed the query
        query_embedding = get_query_embedding(query)

        # Step 2: Vector search — find top 10 semantically similar deals
        candidate_deals = semantic_search(query_embedding, merchant.id, top_k=10)

        if not candidate_deals:
            return Response({"results": [], "message": "No deals found"})

        # Step 3: LLM reranking — GPT-4o picks best 5 and adds pitches
        ranked = llm_rerank(query, candidate_deals[:10])

        # Step 4: Build final response — merge deal data with AI pitches
        deal_map = {str(d.id): d for d in candidate_deals}
        results = []
        for item in ranked[:5]:  # Return top 5 only
            deal = deal_map.get(item["deal_id"])
            if deal:
                results.append({**DealSerializer(deal).data, "pitch": item["pitch"]})

        # Step 5: Log the query for analytics
        UserQuery.objects.create(
            merchant=merchant, query_text=query, query_embedding=query_embedding
        )

        return Response({"results": results})
