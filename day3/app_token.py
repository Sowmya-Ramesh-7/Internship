from flask import Flask
from flask import request, make_response
import jwt

import requests

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