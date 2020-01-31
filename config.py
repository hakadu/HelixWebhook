import os

workers = int(os.environ.get('GUNICORN_PROCESSES', '3'))
port = int(os.environ.get('GUNICORN_PORT', '9899'))

forwarded_allow_ips = '*'
secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }
