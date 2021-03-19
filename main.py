from datetime import datetime

from fastapi import FastAPI

api = FastAPI()


@api.get("/")
async def root():
    return {"msg": "Welcome to CYE Email!"}


@api.get("/emails/{id_}", status_code=200)
async def get_email_by_id(id_: int):
    return {
        "id": id_,
        "subject": "Example Email in Starter Code",
        "body": """This is a placeholder email and won't be used in the actual service.
You should update this route definition to get the email by its `id` in the database. Good Luck!

Regards,

CYE Team""",
        "sender": "johndoe@umass.edu",
        "recipient": "you@umass.edu",
        "has_attachments": False,
        "created": str(datetime.now().strftime("%Y-%m-%d %H:%M")),
    }
