import time
from flask import Flask
from flask import request, make_response

import sqlalchemy as db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
engine = db.create_engine("sqlite:///employees.sqlite")
conn = engine.connect()

app = Flask(__name__)

metadata = db.MetaData()
employee = db.Table('employee', metadata,
db.Column('id', db.Integer(), primary_key=True),
db.Column('name', db.String(255), nullable=False),
db.Column('author', db.String(1024), default="Nammane"),
)
metadata.create_all(engine)

Base = declarative_base()
session = sessionmaker(bind=engine)()

from flask import Flask
from flask import request, make_response
import jwt

import request

class BaseException(Exception):
    status = 400
    message = ""
    def __init__(self, status, message) -> None:
        super().__init__()
        self.status = status
        self.message = message
    def __str__(self):
        return str({'status': self.status, 'message': self.message})
class TokenGenerationError(BaseException):
    def __init__(self) -> None:
        super().__init__(500, "Unable to generate the token")
class PayloadMismatchError(BaseException):
    def __init__(self) -> None:
        super().__init__(402, "Invalid id")
        
app = Flask(__name__)




@app.route('/api/token/<int:employee_id>', methods=['POST'])
def fetch_token(employee_id):
    log_message = {
        'operation': 'fetch token',
        'status': 'processing'
    }
    app.logger.info(str(log_message))
    payload = {
        'id': employee_id,
        'iss': 'DSCE',
        'sub': 'Employee Microservice Token'
    }
    try:
        token = jwt.encode(payload,
        key="mysecretkey")
    except:
        log_message['status'] = 'unsuccessful'
        log_message['reason'] = 'Token generation error'
        app.logger.error(str(log_message))
        err = TokenGenerationError()
        return str(err), err.status

    app.logger.info(str(log_message))
    return {'token': token}, 200


def authenticate_request(called):
    def f(*args, **kwargs):
        log_message = {
            'operation': 'fetch token',
            'status': 'processing'
        }
        
        app.logger.info(str(log_message))
        try:
            header=request.headers
            token_payload = jwt.decode(header['token'], 'mysecretkey', algorithms = ['HS256'])
            print(token_payload)
            if Employee.get_by_id(int(token_payload['id']))!=None:
                return {"payload":token_payload,}, 200
            else:
                err = PayloadMismatchError()
                return str(err), err.status
        except KeyError as e:
            log_message['status'] = 'unsuccessful'
            log_message['reason'] = 'Payload error'
            app.logger.error(str(log_message))
            err = PayloadMismatchError()
            return str(err), err.status
        
        return called(*args, **kwargs)

    f.__name__ = called.__name__
    return f
        
        # if token_payload['id']==employee_id:
        #     return {"payload":token_payload,}, 200
        # else:
        #     err = PayloadMismatchError()
        #     return str(err), err.status

class Employee(Base):
    __tablename__ = "employee"
    name = Column(String)
    id = Column(Integer, primary_key=True)
    address = Column(String)

    def __init__(self, name, address):
        self.name = name
        self.address = address
    
    def __str__(self):
        return str({
        "id": self.id,
        "name": self.name,
        "address": self.address
        })
        
    def validate(self):
        val_name = len(self.name) > 0 and len(self.name) < 256
        val_addr = len(self.address) > 0 and len(self.address) < 1024
        return val_name and val_addr
    
    def save(self):
        session.add(self)
        session.commit()
    
    
        
    def get_by_id(self,id):
        emp = session.query(Bank).filter_by(id).first()
        return emp
    
    



    # Exception Handling Classes
class BaseException(Exception):
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

class EmployeeNotPresentError(BaseException):
    def __init__(self) -> None:
        super().__init__(404, "Employee not Present")
    # Managing Logging
def setup_logger(called):
    def f(*args, **kwargs):
        request.logger = app.logger
        return called(*args, **kwargs)
    f.__name__ = called.__name__
    return f

def time_request(called):
    def f(*args, **kwargs):
        request.start_time = time.time() * 1000
        res = called(*args, **kwargs)
        request.end_time = time.time() * 1000
        request.time = request.end_time - request.start_time
        app.logger.info('request time: {}'.format(request.time))
        return res
    f.__name__ = called.__name__
    return f

def setup_tracing(called):
    def f(*args, **kwargs):
        request.req_id = 'req_{}'.format(time.time() * 1000)
        res, status = called(*args, **kwargs)
        res_send = make_response(res)
        res_send.headers['X-Request-Id'] = request.req_id
        return res_send, status
    f.__name__ = called.__name__
    return f

@app.route("/api/employee/", methods=["POST"])
@authenticate_request
@setup_logger
@time_request
@setup_tracing
def create_employee():
    employee = request.json
    emp = Employee(employee['name'], employee['address'])

    log_message = {'tracking_id': request.req_id,
                    'operation': 'create employee',
                    'status': 'processing'}
    
    request.logger.info(str(log_message))
    # Validation error
    if not emp.validate():
        log_message['status'] = 'unsuccessful'
        request.logger.error(str(log_message))
        err = ValidationError()
        return str(err), err.status
    
    emp.save()
    log_message['status'] = 'successful'
    request.logger.info(str(log_message))
    return str(emp), 201

@app.route("/api/employee/<int:employee_id>", methods=["PUT"])
@setup_logger
@time_request
@setup_tracing
def alter_employee_data(employee_id):
    employee = request.json
    emp_to_change = None

    log_message = { 'tracking_id': request.req_id,
                    'operation': 'alter employee',
                    'status': 'processing'}
    request.logger.info(str(log_message))
    try:
        emp_to_change = employees[employee_id]
    except KeyError as e:
        log_message['status'] = 'unsuccessful'
        request.logger.error(str(log_message))
        err = EmployeeNotPresentError()
        return str(err), err.status

    emp_to_change.name = employee.get('name', employees[employee_id].name)
    emp_to_change.address = employee.get('address',employees[employee_id].address)
    emp = Employee(employee['name'], employee['address'])

    log_message = { 'tracking_id': request.req_id,
                    'operation': 'alter employee',
                    'status': 'processing'}
    request.logger.info(str(log_message))
    # Validation error
    if not emp.validate():
        log_message['status'] = 'unsuccessful'
        request.logger.error(str(log_message))
        err = ValidationError()
        return str(err), err.status

    log_message['status'] = 'successful'
    request.logger.info(str(log_message))
    return str(employees[employee_id]), 200

@app.route("/api/employee/<int:employee_id>", methods=["GET"])
@authenticate_request
def get_employee_information(employee_id):
    try:
        emp = employees[employee_id]
    except KeyError as e:
        err = EmployeeNotPresentError()
        return str(err), err.status
    return str(emp), 200

@app.route("/api/employee/<int:employee_id>", methods=["DELETE"])
def remove_employee_data(employee_id):
    try:
        emp = employees[employee_id]
    except KeyError as e:
        err = EmployeeNotPresentError()
        return str(err), err.status

    del employees[employee_id]
    return make_response(""), 200