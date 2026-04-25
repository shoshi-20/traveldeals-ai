from django.core.management.base import BaseCommand
from api.models import Merchant, Deal

DEALS = [
    {
        "title": "7 Days in Bali — All Inclusive",
        "destination": "Bali, Indonesia",
        "price": 899,
        "description": "Tropical paradise with rice terraces, temples, and stunning sunsets. Includes resort, breakfast, and 2 excursions.",
    },
    {
        "title": "Tokyo City Break — 5 Nights",
        "destination": "Tokyo, Japan",
        "price": 1299,
        "description": "Explore neon-lit streets, sushi markets, and serene shrines. Flight + hotel included.",
    },
    {
        "title": "Paris Romance Package — 4 Nights",
        "destination": "Paris, France",
        "price": 1199,
        "description": "Experience the City of Light with Eiffel Tower visit, Seine cruise, and gourmet dining.",
    },
    {
        "title": "New York Explorer — 5 Days",
        "destination": "New York, USA",
        "price": 999,
        "description": "Broadway shows, Times Square, Central Park, and Statue of Liberty tour included.",
    },
    {
        "title": "Dubai Luxury Escape — 6 Nights",
        "destination": "Dubai, UAE",
        "price": 1799,
        "description": "Five-star resort with desert safari, mall shopping, and beach access.",
    },
    {
        "title": "Bangkok Adventure — 4 Nights",
        "destination": "Bangkok, Thailand",
        "price": 699,
        "description": "Temple tours, floating markets, Thai massage, and street food experience.",
    },
    {
        "title": "Barcelona Beach Break — 5 Nights",
        "destination": "Barcelona, Spain",
        "price": 1099,
        "description": "Sagrada Familia, Park Güell, and Mediterranean beaches with flamenco show.",
    },
    {
        "title": "Singapore City Tour — 4 Days",
        "destination": "Singapore",
        "price": 899,
        "description": "Marina Bay Sands, Gardens by the Bay, and diverse culinary experiences.",
    },
    {
        "title": "Amsterdam Canal Tour — 3 Nights",
        "destination": "Amsterdam, Netherlands",
        "price": 799,
        "description": "Canal cruises, Anne Frank House, and Van Gogh Museum included.",
    },
    {
        "title": "Rome Historical Journey — 5 Nights",
        "destination": "Rome, Italy",
        "price": 1249,
        "description": "Colosseum, Vatican City, and authentic Italian cuisine experience.",
    },
    {
        "title": "Bora Bora Honeymoon — 7 Nights",
        "destination": "Bora Bora, French Polynesia",
        "price": 2499,
        "description": "Overwater bungalows, snorkeling, and romantic island dinners.",
    },
    {
        "title": "Istanbul Cultural Escape — 4 Nights",
        "destination": "Istanbul, Turkey",
        "price": 749,
        "description": "Blue Mosque, Hagia Sophia, Grand Bazaar, and Turkish hammam experience.",
    },
    {
        "title": "Seoul Modern Explorer — 4 Nights",
        "destination": "Seoul, South Korea",
        "price": 899,
        "description": "K-pop tours, palaces, shopping districts, and Korean BBQ culinary tour.",
    },
    {
        "title": "Vienna Classical Tour — 3 Nights",
        "destination": "Vienna, Austria",
        "price": 849,
        "description": "Schönbrunn Palace, St. Stephen's Cathedral, and classical music concert.",
    },
    {
        "title": "Cancun Beach Paradise — 5 Nights",
        "destination": "Cancun, Mexico",
        "price": 999,
        "description": "All-inclusive resort, cenotes, Mayan ruins, and water sports.",
    },
    {
        "title": "London Royal Experience — 4 Nights",
        "destination": "London, England",
        "price": 1099,
        "description": "Big Ben, Tower of London, West End theatre, and afternoon tea.",
    },
    {
        "title": "Melbourne Arts & Culture — 3 Nights",
        "destination": "Melbourne, Australia",
        "price": 899,
        "description": "Street art tours, museums, live music venues, and Great Ocean Road trip.",
    },
    {
        "title": "Sydney Harbour Adventure — 5 Nights",
        "destination": "Sydney, Australia",
        "price": 1199,
        "description": "Opera House tour, Bondi Beach, Blue Mountains hike, and wildlife encounters.",
    },
    {
        "title": "Swiss Alps Escape — 6 Nights",
        "destination": "Interlaken, Switzerland",
        "price": 1599,
        "description": "Mountain hiking, Jungfrau railway, scenic cable cars, and alpine lodging.",
    },
    {
        "title": "Marrakech Desert Experience — 4 Nights",
        "destination": "Marrakech, Morocco",
        "price": 649,
        "description": "Medina exploration, Sahara desert trek, Berber village visit, and hammam.",
    },
]


class Command(BaseCommand):
    help = "Seed the database with sample merchants and deals"

    def handle(self, *args, **kwargs):
        merchant, _ = Merchant.objects.get_or_create(
            name="Demo Bank", defaults={"brand_color": "#003087", "logo_url": ""}
        )
        for d in DEALS:
            Deal.objects.get_or_create(merchant=merchant, title=d["title"], defaults=d)
        self.stdout.write(self.style.SUCCESS(f"Created {len(DEALS)} deals"))
