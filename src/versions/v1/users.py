import json

# Base API Class
from src.versions.v1.api import API


# API Version 1
class Users(API):

  
  def index(self, http, var):
    tables = [
      'users',
      'contacts',
      'addresses'
    ]
    return self.sort(self.db.join(tables,['id','user'])), 200



  def read(self, http, var):
    if 'id' in var:
      args = {
        'id': var['id']
      }
      tables = [
        'users',
        'contacts',
        'addresses'
      ]
      user = self.db.join(tables, ['id','user'], args)

      if len(user) > 0:
        return self.sort(user)[0], 200
      else:
        return {'error': 'Record not found'}, 404
    else:
      return {'error': 'Unable to get user.'}, 400


  def create(self, http, var):
    data = http.request.json
    prop = self.not_in(data, 'users')

    if prop:
      return {'error': f"Undefined property name '{prop}'."}, 400
    else:
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
              return self.sort(user)[0], 201
      return {'error': 'Unable to create user.'}, 400


  def update(self, http, var):
    data = http.request.json
    prop = self.not_in(data, 'users')

    if prop:
      return {'error': f"Undefined property name '{prop}'."}, 400
    else:
      if data and 'id' in var:
        updated = self.db.update('users', {'id': var['id']}, data)
        if updated:
          return updated, 200
        else:
          return {'error': 'Unable to update user.'}, 400 
      else:
        return {'error': 'No data received'}, 400


  def delete(self, http, var):
    args = {
      'id': var['id']
    }
    if len(args['id']) > 1:
      if self.db.delete('users', args):
        success = {
          'success': f"ID ({var['id']}) has been deleted successfully."
        }
        return success, 200
      else:
        return {'error': 'Record not found'}, 404
    return {'error': 'Unable to delete user.'}, 400