from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import Optional
import datetime as dt
import sqlite3

class Email(BaseModel):
    body: Optional[str] = None
    subject: Optional[str] = Query(None, min_length=1, max_length=50, regex="\A(.*)\Z")
    sender: Optional[str] = Query(None, min_length=3, max_length=50, regex="^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$")
    recipient: Optional[str] = Query(None, min_length=3, max_length=50, regex="^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$")
    has_attachments: Optional[bool] = False

con = sqlite3.connect('email.db')
cur = con.cursor()

api = FastAPI()


@api.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@api.get("/")
async def root():
    try:
        cur.execute('''CREATE TABLE emails (body varchar(255), subject varchar(255), sender varchar(255) NOT NULL, recipient varchar(255) NOT NULL, has_attachments boolean default False, created DATETIME DEFAULT (datetime('now','localtime')))''')
    except:
        return {"msg": "Table already exists. Welcome to CYE Emails!"}
    con.commit()
    return {"msg": "Table created. Welcome to CYE Emails!"}


@api.get("/emails", status_code=200)
async def get_emails(sender: Optional[str] = Query(None, alias="sender"), recipient: Optional[str] = Query(None, alias="recipient"), before: Optional[str] = Query(None, alias="before")):
    response = []
    if sender:
        cur.execute('''SELECT rowid,* FROM emails WHERE sender = ? ORDER BY created DESC''',(sender,))
    elif recipient:
        cur.execute('''SELECT rowid,* FROM emails WHERE recipient = ? ORDER BY created DESC''',(recipient,))
    elif before:
        parsed_date = dt.datetime.strptime(before, '%m-%d-%Y')
        cur.execute('''SELECT rowid,* FROM emails WHERE Timestamp <= ? ORDER BY created DESC''',(parsed_date,))
    emails = cur.fetchall()
    if not emails:
        raise HTTPException(status_code=404, detail="No Emails found")
    for email in emails:
        email_JSON = {
            "id":email[0],
            "body":email[1],
            "subject" : email[2],
            "sender" : email[3],
            "recipient" : email[4],
            "has_attachments":email[5],
            "created":email[6]
        }
        response.append(email_JSON)
    return response


@api.post("/emails", status_code=200)
async def post_emails(email: Email):
    cur.execute('''INSERT INTO emails(body, subject, sender, recipient, has_attachments) VALUES (?, ?, ?, ?, ?)''',(email.body, email.subject, email.sender, email.recipient, email.has_attachments))
    con.commit()
    return {"message":"Email saved!"} 


@api.get("/emails/{id}", status_code=200)
async def get_email_by_id(id: int):
    cur.execute('SELECT * from emails where rowid = ?',(id,))
    email = cur.fetchone()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    response = {
        "id":id,
        "body":email[0],
        "subject" : email[1],
        "sender" : email[2],
        "recipient" : email[3],
        "has_attachments":email[4],
        "created":email[5]
    }
    return response


@api.patch("/emails/{id}", status_code=200)
async def update_email_by_id(id: int, email: Email):
    cur.execute('SELECT * from emails where rowid = ?',(id,))
    resp_email = cur.fetchone()
    response = {
        "id":id,
        "body":resp_email[0],
        "subject" : resp_email[1],
        "sender" : resp_email[2],
        "recipient" : resp_email[3],
        "has_attachments":resp_email[4],
        "created":resp_email[5]
    }
    email_model = Email(**response)
    update_email = email.dict(exclude_unset=True)
    updated_email = email_model.copy(update=update_email)
    cur.execute('UPDATE emails SET body = ?, subject = ?, sender = ?, recipient = ?, has_attachments = ? WHERE rowid = ?',(updated_email.body, updated_email.subject, updated_email.sender, updated_email.recipient, updated_email.has_attachments, id))
    con.commit()
    return {"message":"Email updated!"}  


@api.delete("/emails/{id}", status_code=200)
async def delete_email_by_id(id: int):
    cur.execute('DELETE from emails where rowid = ?',(id,))
    con.commit()
    return {"message":"Email deleted!"}