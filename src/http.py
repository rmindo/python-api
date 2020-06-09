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
  
  
  def __init__(self):
    
    # Authentication
    self.auth = Auth()
    # Flask Framework
    self.flask = Flask(__name__)



  # View functions
  def view(self, name, func):

    # Import module
    def mod(version, name):
      return imp.import_module(f"src.versions.{version}.{name}")
      
    def handler(**args):
      try:
        inst = getattr(mod(args['version'], name), name.capitalize())()
        if hasattr(inst, func):
          attr = getattr(inst, func)
          if func == 'init':
            return self.response(attr(self), 200)
          else:
            output, code = attr(request, args)
            # Authenticate
            auth = self.authenticate(inst)
            if auth == True:
              return self.response(output, code)
            else:
              return self.response(auth)
        else:
          return self.response({'error': f'Missing attribute {name}'}, 400)
      except Exception:
        return self.response({'error': 'Something went wrong'}, 500)
    return handler
    

  
  # API Services
  def routes(self, config):
    routes = {}

    # For routing
    rule = self.flask.add_url_rule
    views = self.flask.view_functions

    # Resource routes
    for items in config['resource']:
      path = ''
      for name, route in items.items():
        path += f"/{name}"
        # Route resource
        routes[name] = [
          ['GET', path, 'index'],
          ['POST', path, 'create'],
        ]
        # Variable rules
        if 'var' in route:
          path += f"/<{route['var']}>"
          # Route with unique ID
          routes[name] = routes[name]+[
            ['GET', path, 'read'],
            ['PUT', path, 'update'],
            ['DELETE', path, 'delete']
          ]
        # Extra routes
        if 'extra' in route:
          routes[name] = routes[name]+route['extra']


        for item in routes[name]:
          key = f'{name}.{item[2]}'
          url = f'/api/<string:version>/{item[1]}'

          rule(url, key, methods=[item[0]])
          if key not in views:
            views[key] = self.view(name, item[2])
      
      
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
    if auth:
      # Clean authorization
      def clean(name):
        return auth.replace(f'{name} ', '')

      # Check if has basic auth
      if auth.find('Basic') >= 0:

        data = self.auth.decode(clean('Basic'))
        data = list(filter(None, data.split(':')))

        if len(data) == 2:
          basic = user.basic(data[0])
          if basic and 'payload' in basic and 'password' in basic:
            return self.auth.verify(data[1], basic['payload'], basic['password'])
          else:
            return {
              'code': 401,
              'error': 'Invalid Username/Password'
            }
        else:
          return {
            'code': 401,
            'error': 'Username/Password is Required',
            'headers': {
              'WWW-Authenticate': 'Basic realm="Required"'
            }
          }
      # Check if has bearer auth
      if auth.find('Bearer') >= 0:
        parsed = self.auth.parse(clean('Bearer'))
        if parsed and 'payload' in parsed:
          # Secret key
          bearer = user.bearer(parsed['payload'])
          if bearer and 'token' in bearer and 'key' in bearer:
            if bearer['token'] == parsed['token']:
              # Verify token
              return self.auth.verify(bearer['key'], parsed['payload'], parsed['signature'])
        return {
          'code': 401,
          'error': 'Invalid Token'
        }
    else:
      return {
        'code': 401,
        'error': 'Missing Authorization'
      }




# Decimal Encoder
class DecimalEncoder(json.JSONEncoder):

  def default(self, o):
    if isinstance(o, decimal.Decimal):
      if o % 1 > 0:
        return float(o)
      else:
        return int(o)
    return super(DecimalEncoder, self).default(o)
