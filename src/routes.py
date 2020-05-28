from src.models.init import initialize

##
# API Routes
##
def api(http, api):
  
	# Response
  def response(version, name, para={}):
    
    crud = api[version]
    auth = http.authenticate(lambda arg : crud.db.read(crud.db.config['schema']['parent'], arg))

    if version in api:
      output, code = getattr(crud, name)(http.request, para)

      if auth and 'id' in auth:
        result = output(auth)

        if 'error' in result:
          return http.response(result['error'], result['code'])
        else:
          return http.response(result, code)
      else:
        return http.response(auth)
    else:
      return http.response({'error': 'Invalid API Version'}, 400)



  @http.flask.route('/api/<string:version>/init', methods=['GET'])
  def init(version):
    return initialize(http, api[version].db)



	# Add user
  @http.flask.route('/api/<string:version>/users', methods=['POST'])
  def addUser(version):
    return response(version, 'addUser')



	# Get Users
  @http.flask.route('/api/<string:version>/users', methods=['GET'])
  def getUsers(version):
    return response(version, 'getUsers')



	# Get User
  @http.flask.route('/api/<string:version>/users/<string:id>', methods=['GET'])
  def getUser(version, id):
    return response(version, 'getUser', {'id': id})



	# Update User
  @http.flask.route('/api/<string:version>/users/<string:id>', methods=['PUT'])
  def updateUser(version, id):
    return response(version, 'updateUser', {'id': id})



	# Delete User
  @http.flask.route('/api/<string:version>/users/<string:id>', methods=['DELETE'])
  def deleteUser(version, id):
    return response(version, 'deleteUser', {'id': id})



	# Get address
  @http.flask.route('/api/<string:version>/users/<string:id>/addresses', methods=['GET'])
  def getAddresses(version, id):
    return response(version, 'getAddresses', {'id': id})



	# Get address
  @http.flask.route('/api/<string:version>/users/<string:id>/addresses/<string:key>', methods=['GET'])
  def getAddress(version, id, key):
    return response(version, 'getAddress', {'id': id, 'key': key})



	# Add address
  @http.flask.route('/api/<string:version>/users/<string:id>/addresses', methods=['POST'])
  def addAddress(version, id):
    return response(version, 'addAddress', {'id': id})



	# Update address
  @http.flask.route('/api/<string:version>/users/<string:id>/addresses/<string:key>', methods=['PUT'])
  def updateAddress(version, id, key):
    return response(version, 'updateAddress', {'id': id, 'key': key})



	# Update address
  @http.flask.route('/api/<string:version>/users/<string:id>/addresses/<string:key>', methods=['DELETE'])
  def deleteAddress(version, id, key):
    return response(version, 'deleteAddress', {'id': id, 'key': key})



	# Get communication
  @http.flask.route('/api/<string:version>/users/<string:id>/contacts', methods=['GET'])
  def getContacts(version, id):
    return response(version, 'getContacts', {'id': id})



	# Get address
  @http.flask.route('/api/<string:version>/users/<string:id>/contacts/<string:key>', methods=['GET'])
  def getContact(version, id, key):
    return response(version, 'getContact', {'id': id, 'key': key})



	# Add communication
  @http.flask.route('/api/<string:version>/users/<string:id>/contacts', methods=['POST'])
  def addContact(version, id):
    return response(version, 'addContact', {'id': id})



	# Update address
  @http.flask.route('/api/<string:version>/users/<string:id>/contacts/<string:key>', methods=['PUT'])
  def updateContact(version, id, key):
    return response(version, 'updateContact', {'id': id, 'key': key})



	# Update address
  @http.flask.route('/api/<string:version>/users/<string:id>/contacts/<string:key>', methods=['DELETE'])
  def deleteContact(version, id, key):
    return response(version, 'deleteContact', {'id': id, 'key': key})