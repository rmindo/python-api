import json
import decimal
import datetime
import importlib as imp

# Flask Framework
from flask import Flask, jsonify, request, make_response, Response

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
    '500': 'Internal Server Error',
  }
  
  # Request
  request = request
  
  
  def __init__(self, config):
    
    # Authentication
    self.auth = Auth()
    # Flask Framework
    self.flask = Flask(__name__)
    # Configuration
    self.config = config


  
  # API Services
  def routes(self, db):
    routes = {}

    # For routing
    rule = self.flask.add_url_rule
    views = self.flask.view_functions

    # Import module
    def mod(version, name):
      return imp.import_module(f"src.versions.{version}.{name}")

    # View functions
    def view(name, item):
      def handler(**args):
        try:
          ins = getattr(mod(args['version'], name), name.capitalize())(db)
          if hasattr(ins, item[2]):
            result, code = getattr(ins, item[2])(request, args)
            if result:
              return self.createResponse(db, result, code)
          else:
            return self.response({'error': f'Missing attribute {name}'}, 400)
        except Exception:
          return self.response({'error': 'Something went wrong'}, 500)
      return handler

    # Resource routes
    for items in self.config['resource']:
      path = ''
      for name, uid in items.items():
        path += f"/{name}"
        # Route resource
        routes[name] = [
          ['GET', path, 'index'],
          ['POST', path, 'create'],
        ]
        path += f"/<{uid}>"
        # Route with unique ID
        routes[name] = routes[name]+[
          ['GET', path, 'read'],
          ['PUT', path, 'update'],
          ['DELETE', path, 'delete']
        ]
        for item in routes[name]:
          key = f'{name}.{item[2]}'
          url = f'/api/<string:version>/{item[1]}'

          rule(url, key, methods=[item[0]])
          if key not in views:
            views[key] = view(name, item)
            
            
            
  # Create Response
  def createResponse(self, db, output, code):
    auth = self.authenticate(lambda arg : db.read(db.config['schema']['parent'], arg))
    if auth and 'id' in auth:
      result = output(auth)
      if 'error' in result:
        return self.response(result['error'], result['code'])
      else:
        return self.response(result, code)
    else:
      return self.response(auth)
      
      
      
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
            return {'code': 404, 'error': 'No user found'}
                  
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
