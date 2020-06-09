# Logging
import logging

# CORS
from flask_cors import CORS

# Request
from src.http import HTTP
# Configuration
from src.config import config



api = {}

# HTTP Request
http = HTTP()
##
# Routes for every request
#
http.routes(config)

##
# Allow Cross Origin
#
CORS(http.flask)



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



# Run the App
if __name__ == '__main__':
  http.flask.run(debug=True, port=80, host='0.0.0.0')


# Logging
logging.basicConfig(filename='error.log', filemode='w', level=logging.DEBUG)
