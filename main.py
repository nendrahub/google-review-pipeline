from apify_client import ApifyClient
from supabase import create_client
import os

# =====================
# CONFIG
# =====================

APIFY_TOKEN = os.environ["APIFY_TOKEN"]

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

ACTOR_ID = "Xb8osYTtOjlsgI6k9"

# =====================
# CLIENT
# =====================

apify = ApifyClient(APIFY_TOKEN)

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# =====================
# APIFY INPUT
# =====================

run_input = {
    "language": "id",
    "personalData": True,
    "reviewsOrigin": "google",
    "reviewsStartDate": "1 day",
    "startUrls": [
        {
            "url": "https://www.google.com/maps/place/Daya+Toyota+Cakung+Official/@-6.192028,106.970474,17z"
        }
    ]
}

# =====================
# RUN ACTOR
# =====================

run = apify.actor(ACTOR_ID).call(
    run_input=run_input
)

print("Status:", run.status)
print("Run ID:", run.id)
print("Dataset ID:", run.default_dataset_id)

# =====================
# GET DATASET
# =====================

dataset = apify.dataset(run.default_dataset_id)

items_page = dataset.list_items()

reviews = items_page.items

print("Jumlah review:", len(reviews))

if len(reviews) == 0:
    print("Tidak ada review baru")
    exit()

print("Sample review:")
print(reviews[0])

# =====================
# MAPPING
# =====================

mapped_reviews = []

for r in reviews:

    review_id = r.get("reviewId")

    if not review_id:
        print("SKIP review tanpa reviewId")
        continue

    mapped_reviews.append({
        "review_id": review_id,
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

print("Siap upload:", len(mapped_reviews))

# =====================
# UPSERT SUPABASE
# =====================

result = (
    supabase
    .table("reviews_raw")
    .upsert(
        mapped_reviews,
        on_conflict="review_id"
    )
    .execute()
)

print("Upload selesai")
print(result)
