import json

# Base API Class
from src.versions.v1.api import API


# API Version 1
class Addresses(API):
  
  
  def __init__(self, db):
    # Database
    self.db = db

  
  def index(self, req, para):
    return self.getSubItems('addresses', req, para)


  def read(self, req, para):
    return self.getSubItem('addresses', req, para)


  def create(self, req, para):
    return self.addSubItem('addresses', req, para)


  def update(self, req, para):
    return self.updateSubItem('addresses', req, para)


  def delete(self, req, para):
    return self.deleteSubItem('addresses', req, para)