import json

# Configuration
from src.config import config

# Models
from src.models.init import initialize
from src.models.database import Database


# API Version 1
class API:


  # Columns of contacts
  contacts = [
    'id',
    'type',
    'value',
    'preferred'
  ]

  # Columns of addresses
  addresses = [
    'id',
    'unit',
    'type',
    'city',
    'state',
    'number',
    'street',
    'zipcode'
  ]

  # Columns of users
  identification = [
    'title',
    'gender',
    'address',
    'lastname',
    'firstname',
    'dateofbirth'
  ]

  def __init__(self):
    # Database
    self.db = Database(config)

  

  ##
  # Initialize database
  #
  def init(self, http):
    return initialize(http, self.db)



  def sort(self, rows):
    data = []
    contacts = []
    addresses = []

    for row in rows:
      address = {}
      contact = {}
      identification = {}

      for name in row:
        if name in self.contacts:
          contact[name] = row[name]
        if name in self.addresses:
          address[name] = row[name]
        if name in self.identification:
          identification[name] = row[name]

      contacts.append(contact)
      addresses.append(address)
      data.append({
        'contacts': contacts,
        'addresses': addresses,
        'identification': identification,
      })

    return data

  

  ##
  # Basic authentication
  #
  def basic(self, username):
    user = self.db.read('users', {'id': 1})
    if len(user) > 0:
      user = user[0]
      if 'auth' in user:
        return {
          'payload': {
            'id': user['id']
          },
          'password': user['auth']['password']
        }

  
  ##
  # Bearer token authentication
  #
  def bearer(self, payload):
    user = self.db.read('users', {'id': payload['id']})
    if len(user) > 0:
      user = user[0]
      if 'auth' in user:
        auth = user['auth']
        return {
          'key': auth['key'],
          'token': auth['token']
        }
    
  

  ##
  # Add sub item
  #
  def addSubItem(self, name, req, para = {}):
    data = req.json
    if data and 'id' in para:
      data['user'] = para['id']
      return self.db.create(name, data), 201
    else:
      return {'error': 'Unable to create item.'}, 400
  

  ##
  # Get sub item
  #
  def getSubItem(self, name, req, para = {}):
    if 'id' in para and 'key' in para:
      args = {
        'id': para['key'],
        'user': para['id']
      }
      if 'index' in para:
        args['id'] = para['index']
        
      items = self.db.read(name, args, getattr(self, name))
      if len(items) == 1:
        return items[0], 200
      else:
        return {'error': 'Record not found'}, 404
    else:
      return {'error': 'Unable to get item.'}, 400
  

  ##
  # Get sub items
  #
  def getSubItems(self, name, req, para = {}):
    if 'id' in para:
      args = {
        'user': para['id']
      }
      items = self.db.read(name, args, getattr(self, name))
      if len(items) > 0:
        return items, 200
      else:
        return {'error': 'Record not found'}, 404
    else:
      return {'error': 'Unable to get items.'}, 400
      

  ##
  # Update sub item
  #
  def updateSubItem(self, name, req, para = {}):
    data = req.json
    if 'id' in para and 'key' in para:
      args = {
        'id': para['key'],
        'user': para['id']
      }
      if 'index' in para:
        args['id'] = para['index']

      item = self.db.update(name, args, data)
      if item:
        return item, 200
      else:
        return {'error': 'Unable to update item.'}, 400 
    else:
      return {'error': 'No data received'}, 400
      

  ##
  # Delete sub item
  #
  def deleteSubItem(self, name, req, para = {}):
    if 'id' in para and 'key' in para:
      args = {
        'id': para['key'],
        'user': para['id']
      }
      if 'index' in para:
        args['id'] = para['index']

      if self.db.delete(name, args):
        success = {
          'success': f"ID ({para['id']}) has been deleted successfully."
        }
        return success, 200
      else:
        return {'error': 'Record not found'}, 404
    return {'error': 'Unable to delete item.'}, 400