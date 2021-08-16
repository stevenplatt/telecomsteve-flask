from datetime import datetime
from telecomsteve import db

# insert db models here

# EXAMPLES

# class Contract(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     contract_id = db.Column(db.Integer, unique=True, nullable=False)
#     ssid = db.Column(db.String(30), unique=True, nullable=False)
#     spectrum_block = db.Column(db.String(10), nullable=False)

#     def __repr__(self):
#         return f"Contract('{self.contract_key}', '{self.ssid}', '{self.spectrum_block}')"

# class Peer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     public_key = db.Column(db.String(30), nullable=False)
#     ip = db.Column(db.String(30), unique=True, nullable=False)
#     contract = db.Column(db.String(30), nullable=False)

#     def __repr__(self):
#         return f"Peer('{self.public_key}', '{self.ip}')"

