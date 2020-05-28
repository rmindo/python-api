import json
import urllib.parse
import mysql.connector


# Database
class Database:


  def __init__(self, config):
    self.config = config
    self.server = config['server']


  def rows(self, cur, con, query):
    data = []

    cur.execute(query)
    rows = cur.fetchall()
    con.commit()

    for row in rows:
      for name in row:
        try:
          row[name] = json.loads(str(row[name]))
        except ValueError:
          pass
      data.append(row)

    cur.close()
    con.close()

    return data



  ##
  # Join Table
  #
  def join(self, tab, ref, args=None):
    cur, con = self.connect()

    query = f"""
      SELECT  a.*, b.*, c.*
      FROM {tab[0]} a 
      INNER JOIN {tab[1]} b ON a.{ref[0]} = b.{ref[1]}
      INNER JOIN {tab[2]} c ON a.{ref[0]} = c.{ref[1]}
    """

    if args:
      clause = []
      for i in args:
        clause.append(f"{i}={args[i]}")
      query += f" WHERE a.{' AND '.join(clause)}"

    return self.rows(cur, con, query)

    

  ##
  # Read row
  #
  def read(self, table, args=None, columns='*'):
    keys = []
    cur, con = self.connect()

    for col in columns:
      keys.append(col)

    query = f"SELECT {', '.join(keys)} FROM {table}"

    if args:
      clause = []
      for i in args:
        clause.append(f"{i}='{args[i]}'")
      query += f" WHERE {' AND '.join(clause)}"

    return self.rows(cur, con, query)

  

  ##
  # Create row
  #
  def create(self, table, data):
    keys = []
    vals = []

    cur, con = self.connect()

    for name in data:
      keys.append(name)
      vals.append(f'%({name})s')
      if type(data[name]) is list or type(data[name]) is dict:
        data[name] = json.dumps(data[name])

    add = (
      f"INSERT INTO {table} ({', '.join(keys)}) VALUES ({', '.join(vals)})"
    )
    cur.execute(add, data)
    con.commit()

    # Return Last Row ID
    if cur.lastrowid:
      rowid = cur.lastrowid
      cur.close()
      con.close()
      return self.read(table, {'id': rowid})[0]
    else:
      return []


  ##
  # Update row
  #
  def update(self, table, args, data):
    item = []
    clause = []
    cur, con = self.connect()

    for name in data:
      item.append(f"{name}='{data[name]}'")

    for i in args:
      clause.append(f"{i}='{args[i]}'")

    cur.execute(f"UPDATE {table} SET {', '.join(item)} WHERE {' AND '.join(clause)}")
    con.commit()

    row = self.read(table, args)
    cur.close()
    con.close()

    if len(row) > 0:
      return row[0]



  ##
  # Delete row
  #
  def delete(self, table, args):
    clause = []
    cur, con = self.connect()

    for i in args:
      clause.append(f"{i}='{args[i]}'")
    query = f"DELETE FROM {table} WHERE {' AND '.join(clause)}"

    cur.execute(query)
    con.commit()

    row = self.read(table, args)
    cur.close()
    con.close()

    if len(row) == 0:
      return True
    else:
      return False


  ##
  # Connect to the database
  #
  def connect(self):
    try:
      con = mysql.connector.connect(**self.server)
      cur = con.cursor(dictionary=True)
      return cur, con
    except mysql.connector.Error as e:
      print(f'Error: {e}')



  ##
  # Create database if not exist
  #
  def createDB(self):
    config = {
      'user': self.server['user'],
      'host': self.server['host'],
      'password': self.server['password']
    }
    DBNAME = self.server['database']

    try:
      con = mysql.connector.connect(**config)
      cur = con.cursor(dictionary=True)

      # Create Database
      try:
        cur.execute(f'USE {DBNAME}')
      except mysql.connector.Error as er:
        if er.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
          try:
            cur.execute(f"CREATE DATABASE {DBNAME} DEFAULT CHARACTER SET 'utf8'")
            cur.execute(f'USE {DBNAME}')

            print(f"Successfully created database '{DBNAME}'.")
          except mysql.connector.Error as e:
            print(f'Failed to create database: {e}')
            exit(1)
        else:
          print(er)
          exit(1)

      return cur, con
      
    except mysql.connector.Error as e:
      print(f'Error: {e}')