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
  def __view(self, name, route):

    # Import module
    def mod(version, name):
      return imp.import_module(f"src.versions.{version}.{name}")
      
    def handler(**args):
      try:
        inst = getattr(mod(args['version'], name), name.capitalize())()
        if hasattr(inst, route[2]):
          output, code = getattr(inst, route[2])(self, args)
          # Pass through without authentication
          if route[3] == True:
            pass
          else:
            # Authenticate
            auth = self.authenticate(inst)
            if auth != True:
              return self.response(auth)
          # Send output
          return self.response(output, code)
        else:
          return self.response({'error': f'Missing attribute {name}'}, 400)
      except Exception as e:
        return self.response({'error': str(e)}, 500)
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
      for name, item in items.items():
        path += f"/{name}"
        # Passthrough authentication
        if 'pass' in item:
          bypass = item['pass']
        else:
          bypass = False
        # Route resource
        routes[name] = [
          ['GET', path, 'index', bypass],
          ['POST', path, 'create', bypass],
        ]
        # Variable rules
        if 'var' in item:
          path += f"/<{item['var']}>"
          # Route with unique ID
          routes[name] = routes[name]+[
            ['GET', path, 'read', bypass],
            ['PUT', path, 'update', bypass],
            ['DELETE', path, 'delete', bypass]
          ]
        # Extra routes
        if 'extra' in item:
          routes[name] = routes[name]+item['extra']

        # Iterate routes and add rule
        for route in routes[name]:
          key = f'{name}.{route[2]}'
          url = f'/api/<string:version>/{route[1]}'
          # Add rule
          rule(url, key, methods=[route[0]])
          # Add to views
          if key not in views:
            # If 'pass' is not
            # defined from config then add False
            if len(route) == 3:
              route.append(False)
            # Add to the list of functions
            views[key] = self.__view(name, route)
      
      
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
      if hasattr(user, 'basic') and auth.find('Basic') >= 0:

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
      if hasattr(user, 'bearer') and auth.find('Bearer') >= 0:
        parsed = self.auth.parse(clean('Bearer'))
        if parsed and 'payload' in parsed:
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
