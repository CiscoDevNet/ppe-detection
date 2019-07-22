import os

config = {
    "port": int(os.getenv("PORT", 8080)),
    "provider": os.getenv("PROVIDER", "spark"),  # spark, console
    "spark": {
        "url": os.getenv("SPARK_URL", "https://api.ciscospark.com/v1"),
        "token": os.getenv("SPARK_TOKEN",  "your token"),
        "room_id": os.getenv("SPARK_ROOM_ID", "your room id"),
    },
    "console": {
        "room_id": "test",
    }
}
