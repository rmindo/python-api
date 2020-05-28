import os
import json
import mysql.connector

##
# Initialize database
##
def initialize(http, db):
  # Create database of not exist
  cur, con = db.createDB()

  # Token
  token = http.auth.createtoken({
    'id': 1,
    'exp': {
      'days': 60
    }
  }, 'secret')

  path = os.path.dirname(os.path.realpath(__file__))

  try:
    for name in db.config['schema'].values():
      f=open(f'{path}/schema/{name}.sql', 'r')
      if f.mode == 'r':
        try:
          cur.execute(str(f.read()))
          print(f"Successfully created table '{name}'")
        except mysql.connector.Error as e:
          if e.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
            print(f'Table {name} already is exists.')
          else:
            print(e.msg)

    # Initial user
    db.create('users', {
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
    })

    # Initial contact
    db.create('contacts', {
      "user": 1,
      "type": "email",
      "value": "bfe@sample.com",
      "preferred" : True
    })

    # Initial address
    db.create('addresses', {
      "user": 1,
      "type": "home",
      "number": 1234,
      "street": "blah blah St",
      "unit": "1 a",
      "city": "Somewhere",
      "state": "WV",
      "zipcode": "12345"
    })
  except mysql.connector.Error:
    pass

  cur.close()
  con.close()

  print('\nUse this token below for API Request:\n\n', f'{token}\n')

  return http.response({'success': 'Successfully initialized database'}, 201)