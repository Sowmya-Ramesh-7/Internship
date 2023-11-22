# Create a Flask microservice Library management with ability to manage books

# A simple REST Endpoint for the Employee Resource.
from flask import Flask
import time
from flask import request,make_response
import logging

import sqlalchemy as db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
engine = db.create_engine("sqlite:///books.sqlite")
conn = engine.connect()

app = Flask(__name__)

metadata = db.MetaData()
employee = db.Table('book', metadata,
db.Column('id', db.Integer(), primary_key=True),
db.Column('name', db.String(255), nullable=False),
db.Column('author', db.String(1024), default="Nammane"),
)
metadata.create_all(engine)

Base = declarative_base()
session = sessionmaker(bind=engine)()

@app.route('/api/token/<int:book_id>', methods=['POST'])
def fetch_token(book_id):
    log_message = {
        'operation': 'fetch token',
        'status': 'processing'
    }
    app.logger.info(str(log_message))
    payload = {
        'id': book_id,
        'iss': 'DSCE',
        'sub': 'Book Microservice Token'
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
            print(header['token'])
            token_payload = jwt.decode(header['token'], 'mysecretkey', algorithms = ['HS256'])
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
        
        
class Book(Base):
    __tablename__ = "book"
    name = Column(String)
    id = Column(Integer, primary_key=True)
    author = Column(String)

    def __init__(self, name, id, author):
        self.name = name
        self.id = id
        self.author = author
        
    def __str__(self):
        return str({
            "id": self.id,
            "name": self.name,
            "author": self.author
        })
    def validate(self):
        val_name = 0 < int(len(self.name)) < 256  
        val_author = 0 < int(len(self.author)) < 256  
        return val_name and val_author
    def save(self):
        session.add(self)
        session.commit()

    
books = {
    1: Book("Wings of Fire", 1, "Kalam"),
    2: Book("Harry Potter", 2, "Rowling"),
    3: Book("Alice in Wonderland", 3, "Carrol"),
}
count = 3


 # Exception Handling Classes
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
 
class BookNotPresentError(BaseException):
    def __init__(self) -> None:
        super().__init__(404, "Book not Present")

class TokenGenerationError(BaseException):
    def __init__(self) -> None:
        super().__init__(500, "Unable to generate the token")
class PayloadMismatchError(BaseException):
    def __init__(self) -> None:
        super().__init__(402, "Invalid id")

    # Managing Logging -  info or error is logged in Terminal
    #decorator function- that takes in a function and returns a function eg:set up logger and @app.route
def setup_logger(called):
    def f(*args, **kwargs):
        app.logger.setLevel(logging.INFO);
        request.logger = app.logger
        return called(*args, **kwargs)
    f.__name__ = called.__name__
    return f
 
 #args stands for arguments that are passed to the function 
 #kwargs stands for keyword arguments which are passed along with the values into the function
 
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
        request.req_id = 'req_{}'.format(time.time() * 1000) #generating unique id
        res, status = called(*args, **kwargs)
        res_send = make_response(res) #returns res object
        res_send.headers['X-Request-Id'] = request.req_id #custom application header if X is present
        return res_send, status
    f.__name__ = called.__name__
    return f
 

@app.route("/api/book/", methods=["POST"])
@setup_logger
@time_request
@setup_tracing
def add_book():
    log_message = {'tracking_id': request.req_id,
                    'operation': 'create book info',
                    'status': 'processing'}
    
    global count
    book = request.json
    count += 1
    request.logger.info(str(log_message))
    book['id'] = count
    
    
    newBook = Book(book['name'], count, book['author']) #adding new record to dictionary
    
    if not newBook.validate():
        log_message['status'] = 'unsuccessful'
        request.logger.error(str(log_message))
        err = ValidationError()
        return str(err), err.status
    newBook.save()
    log_message['status'] = 'successful'
    request.logger.info(str(log_message))
    return book, 200

@app.route("/api/book/<int:book_id>", methods=["PUT"])
@setup_logger
@time_request
@setup_tracing
def alter_book_data(book_id):
    book = request.json
    log_message = {'tracking_id': request.req_id,
                    'operation': 'Edit book info',
                    'status': 'processing'}
    request.logger.info(str(log_message))
    
    books[book_id].name = book.get('name', books[book_id].name)
    books[book_id].author = book.get('author',books[book_id].author)
    
    if not books[count].validate():
        log_message['status'] = 'unsuccessful'
        request.logger.error(str(log_message))
        err = ValidationError()
        return str(err), err.status
    
    log_message['status'] = 'successful'
    request.logger.info(str(log_message))
    return str(books[book_id]),200

@app.route("/api/book/<int:book_id>", methods=["GET"])
def get_book_information(book_id):
    return str(books[book_id])

@app.route("/api/book/<int:book_id>", methods=["DELETE"])
@setup_logger
@setup_tracing
@time_request
def remove_book_data(book_id):
    log_message = { 'tracking_id': request.req_id,
                    'operation': 'delete employee',
                    'status': 'processing'}
    
    request.logger.info(str(log_message))
    try:
        id=book_id
        del books[id]
    except KeyError as e:
        log_message['status'] = 'unsuccessful'
        log_message['reason'] = 'No such Book'
        request.logger.error(str(log_message))
        err = BookNotPresentError()
        return str(err), err.status
    log_message['status'] = 'successful'
    request.logger.info(str(log_message))
    return make_response(""), 200