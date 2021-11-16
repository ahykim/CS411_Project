import os

class Config(object):
    SECRET = os.environ.get('SECRET_KEY') 