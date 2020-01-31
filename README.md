# Helix_WebHook

Ubuntu:
  1) sudo apt update
  2) sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
  3) sudo apt install python3-venv
  4) mkdir Helix_WebHook
  5) cd Helix_WebHook
  6) run python3 -m venv venv inside the Helix_WebHook directory
  7) source venv/bin/activate
  8) pip install -r requirements.txt
  9) run the app: gunicorn --bind 0.0.0.0:9899 wsgi
