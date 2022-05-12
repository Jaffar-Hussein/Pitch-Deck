import os

class Config:
  SECRET_KEY = '37183a998ba83a7b481bd3f6e0f2b29'
# the three /// are the relative path from the current file
# site.db file should get created in the project directory along side py module
  SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

  MAIL_SERVER='smtp.gmail.com'
  MAIL_PORT = 465
  MAIL_USERNAME = 'apollolibrary99@gmail.com'
  MAIL_PASSWORD = 'Library@99'

  MAIL_USE_TLS = False
  MAIL_USE_SSL = True