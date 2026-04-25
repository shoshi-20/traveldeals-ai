from django.core.management.base import BaseCommand
from openai import OpenAI
from api.models import Deal
import time

client = OpenAI()


class Command(BaseCommand):
    help = "Generate embeddings for all unembedded deals"

    def handle(self, *args, **kwargs):
        batch_size = 64
        deals = list(Deal.objects.filter(is_embedded=False))
        self.stdout.write(f"Embedding {len(deals)} deals...")

        for i in range(0, len(deals), batch_size):
            chunk = deals[i : i + batch_size]
            texts = [
                f"{deal.title}. {deal.destination}. {deal.description} Price: ${deal.price}"
                for deal in chunk
            ]

            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=texts,
            )

            for deal, emb in zip(chunk, response.data):
                deal.embedding = emb.embedding
                deal.is_embedded = True

            Deal.objects.bulk_update(chunk, ["embedding", "is_embedded"])
            self.stdout.write(f"  Embedded {i + len(chunk)} / {len(deals)}")

        self.stdout.write(self.style.SUCCESS("Done!"))
