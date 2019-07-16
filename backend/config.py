import os

config = {
    "port": int(os.getenv("PORT", 8080)),
    "provider": os.getenv("PROVIDER", "spark"),  # spark, console
    "spark": {
        "url": os.getenv("SPARK_URL", "https://api.ciscospark.com/v1"),
        "token": os.getenv("SPARK_TOKEN",  "NjgyYWRiMTYtOWQyMy00YmVkLTk2NDctYzczMWIyODk3NDgwZDU4ODczYjAtZDJj_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"),
        "room_id": os.getenv("SPARK_ROOM_ID", "Y2lzY29zcGFyazovL3VzL1JPT00vNjIxNDk5ZjAtYTc4Zi0xMWU5LWI5YjEtMGY3ZmQ2OTA2NDAw"),
    },
    "console": {
        "room_id": "test",
    }
}
