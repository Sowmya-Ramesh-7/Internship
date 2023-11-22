from flask import Flask
app=Flask(__name__)

import jwt


import requests

from flask import request, make_response

import sqlalchemy as db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
engine = db.create_engine("sqlite:///bank.sqlite")
conn = engine.connect()

metadata = db.MetaData()
bank= db.Table('bank', metadata,
db.Column('username', db.String(255),nullable=False),
db.Column('acc_no', db.String(255),  primary_key=True),
db.Column('password', db.String(1024),nullable=False ),
db.Column('balance', db.Integer(),default=0 ),
)
metadata.create_all(engine)

Base = declarative_base()
session = sessionmaker(bind=engine)()

class BaseException(Exception): #extends Exception class
    status = 400
    message = ""
    def __init__(self, status, message) -> None:
        super().__init__()
        self.status = status
        self.message = message
    def __str__(self):
        return str({'status': self.status, 'message': self.message})
    
    
    
class ValidationError(BaseException):
    def __init__(self) -> None:
        super().__init__(400, "Invalid Input Parameter")

class InvalidAmountError(BaseException):
    def __init__(self) -> None:
        super().__init__(400, "Invalid Amount , Amount should be greater than 0")
        
class InvalidAccountError(BaseException):
    def __init__(self) -> None:
        super().__init__(400, "Invalid Account ,No Such account is Present ")
    
class InsufficientBalError(BaseException):
    def __init__(self) -> None:
        super().__init__(400, "Insufficient Balance ,Withdrawal amount Cannot be greater than Balance ")
    
class TokenGenerationError(BaseException):
    def __init__(self) -> None:
        super().__init__(400, "Token Generation Error ,Unable to genterate token")

class AuthenticationError(BaseException):
    def __init__(self) -> None:
        super().__init__(402, "Invalid username or Password")

class TokenMissingError(BaseException):
    def __init__(self) -> None:
        super().__init__(400, "Token Missing!!")      

class DataMissingError(BaseException):
    def __init__(self) -> None:
        super().__init__(400, "Username or Password Missing!!") 



class Bank(Base):
    __tablename__ ="bank"
    username = Column(String)
    acc_no= Column(Integer, primary_key=True)
    password = Column(String)
    balance=Column(String)
    
 
    def __init__(self, username, acc_no, password):
        self.username = username
        self.acc_no=acc_no
        self.password =password
        self.balance=0
 
    def __str__(self):
        return str({
        "username": self.username,
        "acc_no": self.acc_no,
        "balance":self.balance
        })
        
    def validate(self):
        val_username = len(self.username) > 0 and len(self.username) < 256
        val_acc_no= len(str(self.acc_no)) > 0 and len(str(self.acc_no)) <= 10
        val_password=len(self.password)>6
        return val_username and val_acc_no and val_password
    
    def save(self):
        session.add(self)
        session.commit()
    
def get_by_id(acc_no):
    acc_details=session.query(Bank).filter_by(acc_no=acc_no).first()
    return acc_details

def delete(acc_no):
    acc=session.query(Bank).filter_by(acc_no=acc_no).first()
    session.delete(acc)
    session.commit()
    
def deposit(acc_no, amount):
    acc=session.query(Bank).filter_by(acc_no=acc_no).first()
    acc.balance=acc.balance+amount
    session.commit()
    return str(acc)
    
def withdraw(acc_no, amount):
    acc=session.query(Bank).filter_by(acc_no=acc_no).first()
    acc.balance=acc.balance-amount
    session.commit()
    return str(acc)




@app.route('/api/token/<int:acc_no>', methods=['POST'])
def fetch_token(acc_no):
    acc_info=request.json
    payload = {
        'accno': acc_no,
        'iss': 'ABC Banl',
        'sub': 'Bank Microservice Token',
        'acc_info':acc_info
    }
    try:
        token = jwt.encode(payload,
        key="mysecretkey")
    except:
        err = TokenGenerationError()
        return str(err), err.status
    return str(token)

def authenticate_request(called):
    def f(*args, **kwargs):
        
        header=request.headers
        if header.get('token',None)==None:
            err = TokenMissingError()
            return str(err), err.status
        try:
            acc_details=request.json
            token_payload = jwt.decode(header['token'], 'mysecretkey', algorithms = ['HS256'])
            if(token_payload["acc_info"]["username"]!=acc_details['username'] or token_payload["acc_info"]["password"]!=acc_details['password']):
                err = AuthenticationError()
                return str(err), err.status      
        except KeyError as e:
            return "Some Data Missing!!"+str(e),404
        
        return called(*args, **kwargs)
    f.__name__ = called.__name__
    return f

        
@app.route('/api/newAccount', methods=['POST'])
def create_account():
    details=request.json
    bank_account = Bank(details['username'], details['acc_no'], details['password'])
    
    if not bank_account.validate():
        err = ValidationError()
        return str(err), err.status
    
    res= requests.post("http://localhost:5000/api/token/{0}".format(details['acc_no']),
                 json={
                     'username':details['username'],
                     'acc_no':details['acc_no'],
                     'password':details['password']
                     })
    request.token=res.text
    res_send=make_response(str(bank_account))
    res_send.headers['X-Token-Id'] = request.token
    bank_account.save()
    
    return res_send,200

@app.route('/api/deposit/<int:acc_no>', methods=['PATCH'])
@authenticate_request
def deposit_amount(acc_no):
    if not get_by_id(acc_no):
        err = InvalidAccountError()
        return str(err), err.status
        
    details=request.json
    if(details["amount"]>0):
        updated=deposit(acc_no,details["amount"])
    else:
        err = InvalidAmountError()
        return str(err), err.status
    return str(updated),200

@app.route('/api/withdraw/<int:acc_no>', methods=['PATCH'])
def withdraw_amount(acc_no):
    if not get_by_id(acc_no):
        err = InvalidAccountError()
        return str(err), err.status
    else:
        acc=get_by_id(acc_no)
    details=request.json
    
    if (acc.balance>=details["amount"]):
        updated=withdraw(acc_no,details["amount"])
    else:
        err = InsufficientBalError()
        return str(err), err.status
    
    return str(updated),200
    

    
    


            
        