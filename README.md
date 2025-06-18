# Intro
A translation app. A flask app where templates are rendered server side.

# Install dependencies
```
pipenv shell
pipenv install
```

# Run
Prod:
`pm2 start 'FLASK_DEBUG=1 FLASK_APP=app.py flask run --host=0.0.0.0 --port=5173' --name 'fluent_prod'`
Dev:
`FLASK_DEBUG=1 FLASK_APP=app.py flask run --host=0.0.0.0 --port=3000`

# Google API Key
https://console.cloud.google.com/iam-admin/serviceaccounts/details/106783039422957699297;edit=true/keys?inv=1&invt=AbzwSQ&project=helical-glass-264223

https://console.cloud.google.com -> iam-admin -> serviceaccounts -> polyglot