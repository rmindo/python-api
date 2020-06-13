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
      "firstName": "Ruel",
      "lastName": "Mindo",
      "dateofbirth": "12/12/1212",
      "gender": "M",
      "title": "Full Stack Engineer",
      "auth": json.dumps({
        "key": "secret",
        "token": token
      })
    }

    contacts = {
      "user": 1,
      "type": "email",
      "value": "ruel@coderstage.com",
      "preferred" : True
    }

    addresses = {
      "user": 1,
      "type": "home",
      "number": 987654321,
      "street": "Colon Street",
      "unit": "Unit 1",
      "city": "Cebu City",
      "state": "Central Visayas",
      "zipcode": "6000"
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