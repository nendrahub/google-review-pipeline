from apify_client import ApifyClient
from supabase import create_client
import os


# API / Identity
APIFY_TOKEN = os.environ["APIFY_TOKEN"]

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]


ACTOR_ID = "Xb8osYTtOjlsgI6k9"


# Connection
apify = ApifyClient(APIFY_TOKEN)

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# Input Scraping
run_input = {
    "language": "id",
    "personalData": True,
    "reviewsOrigin": "google",
    "reviewsStartDate": "3 days",
    "startUrls": [
        {
            "url": "https://www.google.com/maps/place/Daya+Toyota+Cakung+Official/@-6.192028,106.970474,17z"
        }
    ]
}


# Run Apify
run = apify.actor(ACTOR_ID).call(
    run_input=run_input
)


print("Status:", run.status)


# Take Scraping Result
reviews = list(
    apify.dataset(run.default_dataset_id).iterate_items()
)


print("Jumlah review:", len(reviews))


# Stop if there are no data
if len(reviews) == 0:
    exit()


# Mapping
data = []

for r in reviews:

    data.append({

        "review_id": r.get("reviewId"),
        "reviewer_id": r.get("reviewerId"),
        "name": r.get("name"),
        "text": r.get("text"),
        "text_translated": r.get("textTranslated"),
        "stars": r.get("stars"),
        "published_at_date": r.get("publishedAtDate"),
        "review_url": r.get("reviewUrl"),
        "response_from_owner_date": r.get("responseFromOwnerDate"),
        "response_from_owner_text": r.get("responseFromOwnerText"),
        "scraped_at": r.get("scrapedAt")

    })


# Supabase
supabase.table("reviews_raw")\
    .upsert(data)\
    .execute()


print("Selesai upload:", len(data))
