import os
import json
import mysql.connector



##
# Initialize database
##
def initialize(http, db):
  # Create database if not exist
  cur, con = db.createDB()


  try:
    # Token
    token = http.auth.createtoken({
      'id': 1,
      'exp': {
        'days': 60
      }
    }, 'secret')

    users = {
      "id": 1,
      "firstName": "Bob",
      "lastName": "Frederick",
      "dateofbirth": "06/21/1980",
      "gender": "M",
      "title": "Manager",
      "auth": json.dumps({
        "key": "secret",
        "token": token
      })
    }

    contacts = {
      "user": 1,
      "type": "email",
      "value": "bfe@sample.com",
      "preferred" : True
    }

    addresses = {
      "user": 1,
      "type": "home",
      "number": 1234,
      "street": "blah blah St",
      "unit": "1 a",
      "city": "Somewhere",
      "state": "WV",
      "zipcode": "12345"
    }

    # Path of schema directory
    path = os.path.dirname(os.path.realpath(__file__))

    for name in db.config['schema'].values():
      f=open(f'{path}/schema/{name}.sql', 'r')
      if f.mode == 'r':
        cur.execute(str(f.read()))

    # Initial user
    db.create('users', users)
    # Initial contact
    db.create('contacts', contacts)
    # Initial address
    db.create('addresses', addresses)

    cur.close()
    con.close()

    return {
      'token': token,
      'success': 'Successfully initialized database'
    }

  except mysql.connector.Error:
    return {
      'note': 'Database has been initiated already.'
    }