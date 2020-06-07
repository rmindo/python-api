# Logging
import logging

# CORS
from flask_cors import CORS

# Configuration
from config import config
# Request
from src.http import HTTP
# Models
from src.models.init import initialize
from src.models.database import Database




api = {}

# HTTP Request
http = HTTP(config)

# Database
database = Database(config)

##
# Allow Cross Origin
#
CORS(http.flask)

##
# Routes for every request
#
http.routes(database)



# Handle not found error
@http.flask.errorhandler(404)
# Not Found
def notfound(e):
  return http.response([], 404)



# Handle method not allowed error
@http.flask.errorhandler(405)
# Not Allowed
def notallowed(e):
  return http.response([], 405)



# Initialize database
@http.flask.route('/init')
def init():
  return initialize(http, database)


# Run the App
if __name__ == '__main__':
  http.flask.run(debug=True, port=80, host='0.0.0.0')


# Logging
logging.basicConfig(filename='error.log', filemode='w', level=logging.DEBUG)
