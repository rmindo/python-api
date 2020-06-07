import json

# Base API Class
from src.versions.v1.api import API


# API Version 1
class Users(API):
  

  def __init__(self, db):
    # Database
    self.db = db

  
  def index(self, req, para):
    def output(client):
      tables = [
        'users',
        'contacts',
        'addresses'
      ]
      return self.sort(self.db.join(tables,['id','user']))
    return output, 200



  def read(self, req, para):
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


  def create(self, req, para):
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


  def update(self, req, para):
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


  def delete(self, req, para):
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