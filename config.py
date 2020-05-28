import os

# Configuration
config = {
  'schema': {
    'parent': 'users',
    'child_one': 'contacts',
    'child_two': 'addresses',
  },
  'server': {
    'user': os.environ['DB_USER'],
    'host': os.environ['DB_HOST'],
    'database': os.environ['DB_NAME'],
    'password': os.environ['DB_PASSWORD']
  }
}