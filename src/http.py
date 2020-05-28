import json
import decimal
import datetime

# Flask Framework
from flask import Flask, jsonify, request, make_response, Response


# Versions
from src.routes import api

# Models
from src.models.auth import Auth


# HTTP
class HTTP:
  
  status = {
		'200': 'Ok',
		'201': 'Created',
		'400': 'Bad Request',
		'401': 'Unauthorized',
		'403': 'Forbidden',
		'404': 'Not Found',
		'405': 'Method Not Allowed',
		'406': 'Not Acceptable',
		'409': 'Conflict',
	}
  
  # Request
  request = request
  
  
  def __init__(self):
    
    # Authentication
    self.auth = Auth()
		# Flask Framework
    self.flask = Flask(__name__)
    
  
  # API Services
  def api(self, service):
    api(self, service)



	# Response
  def response(self, data = [], code = 401):
    
    headers = []
    
    if data and len(data) > 0:
      if 'error' in data:
        para = {
					'status': code,
					'result': {
						'error': data['error']
					},
					'message': self.status[str(code)],
				}
      else:
        para = {
					'status': code,
					'result': data,
					'message': self.status[str(code)],
				}
      
      if 'headers' in data:
        headers = data['headers']
    else:
      para = {
				'status': code,
				'message': self.status[str(code)],
			}

    def default(o):
      if isinstance(o, datetime.datetime):
          return o.__str__()
    return Response(json.dumps(para, default=default, sort_keys=True, indent=4, cls=DecimalEncoder), para['status'], headers, 'application/json')




	# Authenticate
  def authenticate(self, user):
    
    auth = request.headers.get('authorization')
    if auth and auth.find('Bearer') >= 0:
      parsed = self.auth.parse(auth.replace('Bearer ', ''))

      if parsed and 'payload' in parsed:
        # Payload
        payload = parsed['payload']
        if 'token' in parsed:
          user = user({'id': payload['id']})
          if len(user) > 0:
            user = user[0]
            if 'auth' in user:
              # Verify token
              verify = self.auth.verify(user['auth']['key'], payload, parsed['signature'])
              if verify == True:
                return user
          else:
            return {'code': 404, 'error': 'No records'}
                  
      return {'code': 401, 'error': 'Invalid Token'}
    else:
      return {'code': 401, 'error': 'Missing Authorization'}




# Decimal Encoder
class DecimalEncoder(json.JSONEncoder):

  def default(self, o):
    if isinstance(o, decimal.Decimal):
      if o % 1 > 0:
        return float(o)
      else:
        return int(o)
    return super(DecimalEncoder, self).default(o)
