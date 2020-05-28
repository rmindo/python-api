import mysql.connector


# Database
class DB:

  def __init__(self, host, user, password, dbname):
    try:
      self.connection = mysql.connector.connect(
        host=host,
        user=user,
        passwd=password,
        database=dbname
      )
      self.cursor = self.connection.cursor()
      
      print('Connection to MySQL DB successful')
    except mysql.connector.Error as e:
      print(e)


  # Check table
  def table(self, name, query = None):
    self.cursor.execute(f"""
      SELECT COUNT(*)
      FROM information_schema.tables
      WHERE table_name = '{name}'
    """)

    if self.cursor.fetchone()[0] == 0:
      self.cursor.execute(query)
    else:
      return True
    


db = DB('localhost', 'root', 'rmindo', 'api')


db.cursor.close()
db.connection.close()