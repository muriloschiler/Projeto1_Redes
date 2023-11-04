from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from repositories.gmailSMTP import GmailSMTP
from models.message import Message

app = FastAPI()

@app.post("/email")
async def SendEmail(message:Message):
    gmailSMTP = GmailSMTP()
    gmailSMTP.SendMesage(message)
    return {"status":"200"}
    
@app.get("/")
async def root():
    return {"message": "Hello World"}


