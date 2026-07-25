from apify_client import ApifyClient
import os

APIFY_TOKEN = os.environ["APIFY_TOKEN"]

ACTOR_ID = "Xb8osYTtOjlsgI6k9"

client = ApifyClient(APIFY_TOKEN)

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

print("START ACTOR")

run = client.actor(ACTOR_ID).call(
    run_input=run_input
)

print("=" * 50)
print("STATUS:", run.status)
print("RUN ID:", run.id)
print("DEFAULT DATASET:", run.default_dataset_id)
print("=" * 50)

# DEBUG RUN OBJECT
print("RUN OBJECT:")
print(run)

print("=" * 50)

# CEK DATASET DEFAULT
try:
    dataset = client.dataset(run.default_dataset_id)

    info = dataset.get()

    print("DATASET INFO:")
    print(info)

    items = dataset.list_items()

    print("TOTAL ITEMS:", items.total)
    print("ITEMS RETURNED:", len(items.items))

    if len(items.items) > 0:
        print("FIRST ITEM:")
        print(items.items[0])

except Exception as e:
    print("ERROR DATASET:")
    print(e)

print("=" * 50)
print("SELESAI")
