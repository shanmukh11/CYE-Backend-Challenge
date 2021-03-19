from datetime import datetime

from fastapi.testclient import TestClient

from main import api

client = TestClient(api)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"msg": "Welcome to CYE Email!"}

 
# currently this test tests against our hardcoded response body
# Once you've updated the GET route definittion, you'll want to update this test as well
def test_get_single_email():
    id_ = 1
    response = client.get(f"/emails/{id_}/")

    assert response.status_code == 200
    assert response.json() == {
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
