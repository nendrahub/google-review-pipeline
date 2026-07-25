from apify_client import ApifyClient
from supabase import create_client
from datetime import datetime, timezone
import os


# ambil secret dari Github
APIFY_TOKEN = os.environ["APIFY_TOKEN"]

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]


ACTOR_ID = "Xb8osYTtOjlsgI6k9"


# koneksi
apify = ApifyClient(APIFY_TOKEN)

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# input scraping
run_input = {
    "language": "id",
    "personalData": True,
    "reviewsOrigin": "google",
    "reviewsStartDate": "1 days",
    "startUrls": [
        {
            "url": "https://www.google.com/maps/place/Daya+Toyota+Cakung+Official/@-6.192028,106.970474,17z/data=!3m1!4b1!4m8!3m7!1s0x2e698b9e6c61a61f:0x5aced58296cf20ae!8m2!3d-6.192028!4d106.970474!9m1!1b1!16s%2Fg%2F11hdq83g_c"
        }
    ]
}


print("START ACTOR")

# jalankan Apify
run = apify.actor(ACTOR_ID).call(
    run_input=run_input
)

print("Status:", run.status)


# ambil hasil scraping
reviews = list(
    apify.dataset(run.default_dataset_id).iterate_items()
)

print("Jumlah review:", len(reviews))


# kalau kosong berhenti
if len(reviews) == 0:
    print("Tidak ada review baru")
    exit()


# waktu scrape sekarang
now = datetime.now(timezone.utc).isoformat()


# mapping sesuai tabel Supabase
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

        # selalu update setiap workflow berjalan
        "scraped_at": now

    })


# upsert berdasarkan review_id
supabase.table("reviews_raw") \
    .upsert(
        data,
        on_conflict="review_id"
    ) \
    .execute()


print("Selesai upload:", len(data))
print("Scraped at:", now)
