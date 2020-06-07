import json


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

  def __init__(self, db):
    # Database
    self.db = db



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
  # Add sub item
  #
  def addSubItem(self, name, req, para = {}):
    data = req.json
    def output(client):
      if data and 'id' in para:
        data['user'] = para['id']
        return self.db.create(name, data)
      else:
        return {'error': 'Unable to create item.', 'code': 400}
    return output, 201
  

  ##
  # Get sub item
  #
  def getSubItem(self, name, req, para = {}):
    def output(client):
      if 'id' in para and 'key' in para:
        args = {
          'id': para['key'],
          'user': para['id']
        }
        if 'index' in para:
          args['id'] = para['index']
          
        items = self.db.read(name, args, getattr(self, name))
        if len(items) == 1:
          return items[0]
        else:
          return {'error': 'Record not found', 'code': 404}
      else:
        return {'error': 'Unable to get item.', 'code': 400}
    return output, 200
  

  ##
  # Get sub items
  #
  def getSubItems(self, name, req, para = {}):
    def output(client):
      if 'id' in para:
        args = {
          'user': para['id']
        }
        items = self.db.read(name, args, getattr(self, name))
        if len(items) > 0:
          return items
        else:
          return {'error': 'Record not found', 'code': 404}
      else:
        return {'error': 'Unable to get items.', 'code': 400}
    return output, 200
      

  ##
  # Update sub item
  #
  def updateSubItem(self, name, req, para = {}):
    data = req.json
    def output(client):
      if 'id' in para and 'key' in para:
        args = {
          'id': para['key'],
          'user': para['id']
        }
        if 'index' in para:
          args['id'] = para['index']

        item = self.db.update(name, args, data)
        if item:
          return item
        else:
          return {'error': 'Unable to update item.', 'code': 400} 
      else:
        return {'error': 'No data received', 'code': 400}
    return output, 200
      

  ##
  # Delete sub item
  #
  def deleteSubItem(self, name, req, para = {}):
    def output(client):
      if 'id' in para and 'key' in para:
        args = {
          'id': para['key'],
          'user': para['id']
        }
        if 'index' in para:
          args['id'] = para['index']

        if self.db.delete(name, args):
          return {'success': f"ID ({para['id']}) has been deleted successfully."}
        else:
          return {'error': 'Record not found', 'code': 404}
      return {'error': 'Unable to delete item.', 'code': 400}
    return output, 200