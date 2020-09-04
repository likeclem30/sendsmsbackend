from sqlalchemy import func
from message_backend.db import db


class MessageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    phoneNumber = db.Column(db.String(50))
    message = db.Column(db.String(300))
    messageSid = db.Column(db.String(100))
    typeMessage = db.Column(db.String(250))
    status = db.Column(db.String, default='0')
    sent = db.Column(db.Integer, default=0)
    retry = db.Column(db.Integer, default=0)
    creation = db.Column(db.DateTime, server_default=func.now())
    sentTimestamp = db.Column(db.DateTime)
    deliveredTimestamp = db.Column(db.DateTime)
