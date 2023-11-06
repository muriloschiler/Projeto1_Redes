from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from repositories.gmailSMTP import GmailSMTP
from repositories.gmailIMAP import GmailIMAP
from models.message import Message

app = FastAPI()

@app.post("/email")
async def SendEmail(message:Message):
    gmailSMTP = GmailSMTP()
    gmailSMTP.SendEmail(message)
    return {"status":"200"}

@app.get("/email")
async def GetUnreadEMails():
    gmailIMAP = GmailIMAP()
    gmailIMAP.GetUnreadEMails()
    return {"status":"200"}
    
@app.get("/inbox")
async def GetInboxList():
    gmailIMAP = GmailIMAP()
    gmailIMAP.GetInboxList()
    return {"status":"200"}

@app.post("/inbox")
async def PostSelectInbox():
    gmailIMAP = GmailIMAP()
    gmailIMAP.PostSelectInbox()
    return {"status":"200"}



@app.get("/")
async def root():
    return {"message": "Hello World"}


