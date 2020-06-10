import json

# Base API Class
from src.versions.v1.api import API


# API Version 1
class Contacts(API):

  
  def index(self, http, var):
    return self.getSubItems('contacts', http, var)


  def read(self, http, var):
    return self.getSubItem('contacts', http, var)


  def create(self, http, var):
    return self.addSubItem('contacts', http, var)


  def update(self, http, var):
    return self.updateSubItem('contacts', http, var)


  def delete(self, http, var):
    return self.deleteSubItem('contacts', http, var)