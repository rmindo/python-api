import json

# Base API Class
from src.versions.v1.api import API


# API Version 1
class Contacts(API):

  
  def index(self, req, para):
    return self.getSubItems('contacts', req, para)


  def read(self, req, para):
    return self.getSubItem('contacts', req, para)


  def create(self, req, para):
    return self.addSubItem('contacts', req, para)


  def update(self, req, para):
    return self.updateSubItem('contacts', req, para)


  def delete(self, req, para):
    return self.deleteSubItem('contacts', req, para)