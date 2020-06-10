import json

# Base API Class
from src.versions.v1.api import API


# API Version 1
class Addresses(API):

  
  def index(self, http, var):
    return self.getSubItems('addresses', http, var)


  def read(self, http, var):
    return self.getSubItem('addresses', http, var)


  def create(self, http, var):
    return self.addSubItem('addresses', http, var)


  def update(self, http, var):
    return self.updateSubItem('addresses', http, var)


  def delete(self, http, var):
    return self.deleteSubItem('addresses', http, var)