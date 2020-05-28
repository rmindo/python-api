import time
import json
import hmac
import base64
import random
import hashlib
import datetime




# Authentication
class Auth:


	def utf8(self, data):
		return str(data.decode('utf8').replace('=', ''))


	# Hash a string
	def hash(self, string):
		return hashlib.md5(string.encode()).hexdigest()


	# Base64 Encode
	def encode(self, data):
		return self.utf8(base64.b64encode(bytes(str(data), 'utf8')))
    


	# Base64 Decode
	def decode(self, data):
		try:
			return self.utf8(base64.b64decode(data +'=='))
		except Exception as e:
			return False



	# Signature with HMACSHA256
	def sign(self, key, payload):
		return self.encode(hmac.new(bytes(key, 'utf8'), bytes(payload, 'utf8'), hashlib.sha256).hexdigest())



	# Random String
	def random(self, length, type = False):

		o = ''
		n = '0123456789'
		s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

		if type:
			s = n
		else:
			s += n

		for i in range(length):
			o += random.choice(s)
		return str(o)




	# Parse token
	def parse(self, token):

		# Parsing
		encoded = token[86:]
		decoded = self.decode(encoded[:len(encoded)-86])
		
		if decoded:
			try:
				return {'token': token, 'signature': encoded[len(encoded)-86:], 'payload': json.loads(decoded.replace("\'", "\""))}
			except Exception as e:
				
				return None




	# Token Expiration
	def expiration(self, exp = False):

		today = datetime.datetime.now()

		if 'days' not in exp:
			exp['days'] = 0

		if 'hours' not in exp:
			exp['hours'] = 0

		if 'minutes' not in exp:
			exp['minutes'] = 0

		return time.mktime((today + datetime.timedelta(minutes=exp['minutes'], hours=exp['hours'], days=exp['days'])).timetuple())




	# Verify Token
	def verify(self, key, payload, signature):

		sign = self.sign(key, str(payload))

		if 'exp' in payload and payload['exp'] < time.time():
			return None
		else:

			if sign and hmac.compare_digest(signature, sign):
				return True
			else:
				return False



	# Create Token
	def createtoken(self, payload, key):

		payload['exp'] = self.expiration(payload['exp'])
		
		return self.random(86) + self.encode(str(payload)) + self.sign(key, str(payload))