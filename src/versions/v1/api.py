import json


# API Version 1
class API1:


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
        'address': addresses,
        'contacts': contacts,
        'identification': identification,
      })

    return data
      


  def getUser(self, req, para = {}):
    def output(client):
      if 'id' in para:
        args = {
          'id': para['id']
        }
        tables = [
          'users',
          'contacts',
          'addresses'
        ]
        user = self.db.join(tables, ['id','user'], args)

        if len(user) > 0:
          return self.sort(user)[0]
        else:
          return {'error': 'Record not found', 'code': 404}
      else:
        return {'error': 'Unable to get user.', 'code': 400}
    return output, 200
      


  def getUsers(self, req, para = {}):
    def output(client):
      tables = [
        'users',
        'contacts',
        'addresses'
      ]
      return self.sort(self.db.join(tables,['id','user']))
    return output, 200
    
  

  def addUser(self, req, para = {}):
    data = req.json
    def output(client):
      if data:
        tables = [
          'users',
          'contacts',
          'addresses'
        ]
        if 'identification' in data:
          user = self.db.create('users', data['identification'])
          if 'id' in user:
            if 'contacts' in data:
              data['contacts']['user'] = user['id']
              self.db.create('contacts', data['contacts'])
            if 'addresses' in data:
              data['addresses']['user'] = user['id']
              self.db.create('addresses', data['addresses'])

            user = self.db.join(tables, ['id','user'], {'id': user['id']})
            if len(user) == 1:
              return self.sort(user)[0]
      return {'error': 'Unable to create user.', 'code': 400}
    return output, 201



  def deleteUser(self, req, para = {}):
    def output(client):
      args = {
        'id': para['id']
      }
      if len(args['id']) > 1:
        if self.db.delete('users', args):
          return {'success': f"ID ({para['id']}) has been deleted successfully."}
        else:
          return {'error': 'Record not found', 'code': 404}
      return {'error': 'Unable to delete user.', 'code': 400}
    return output, 200
    
  

  def updateUser(self, req, para = {}):
    data = req.json
    def output(client):
      if data and 'id' in para:
        updated = self.db.update('users', {'id': para['id']}, data)
        if updated:
          return updated
        else:
          return {'error': 'Unable to update user.', 'code': 400} 
      else:
        return {'error': 'No data received', 'code': 400}
    return output, 200
    
  

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
        if self.db.delete(name, args):
          return {'success': f"ID ({para['id']}) has been deleted successfully."}
        else:
          return {'error': 'Record not found', 'code': 404}
      return {'error': 'Unable to delete item.', 'code': 400}
    return output, 200
    
  

  ##
  # Add address
  #
  def addAddress(self, req, para = {}):
    return self.addSubItem('addresses', req, para)
  
  ##
  # Get Address
  #
  def getAddress(self, req, para = {}):
    return self.getSubItem('addresses', req, para)
  
  ##
  # Get Addresses
  #
  def getAddresses(self, req, para = {}):
    return self.getSubItems('addresses', req, para)

  ##
  # Update Address
  #
  def updateAddress(self, req, para = {}):
    return self.updateSubItem('addresses', req, para)
      
  ##
  # Delete Address
  #
  def deleteAddress(self, req, para = {}):
    return self.deleteSubItem('addresses', req, para)
    
   

  ##
  # Add contact
  #
  def addContact(self, req, para = {}):
    return self.addSubItem('contacts', req, para)
    
  ##
  # Get contact
  #
  def getContact(self, req, para = {}):
    return self.getSubItem('contacts', req, para)
    
  ##
  # Get contacts
  #
  def getContacts(self, req, para = {}):
    return self.getSubItems('contacts', req, para)
    
  ##
  # Update contact
  #
  def updateContact(self, req, para = {}):
    return self.updateSubItem('contacts', req, para)

  ##
  # Delete Contact
  #
  def deleteContact(self, req, para = {}):
    return self.deleteSubItem('contacts', req, para)