import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DATABASE_NAME = os.environ.get('DATABASE_NAME') or 'web11'
    DATABASE_USER = os.environ.get('DATABASE_USER') or 'root'
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD') or 'qwerty'
    DATABASE_HOST = os.environ.get('DATABASE_HOST') or '127.0.0.1'
    DATABASE_PROVIDER = os.environ.get('DATABASE_PROVIDER') or 'mysql'