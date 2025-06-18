# Intro
A translation app. A flask app where templates are rendered server side.

# Install dependencies
```
pipenv shell
pipenv install
```

# Configure
`cp env.example .env`
Configure .env for your environment

# Run
`pm2 start 'python app.py' --name 'fluent_prod'`

# Google API Key
https://console.cloud.google.com/iam-admin/serviceaccounts/details/106783039422957699297;edit=true/keys?inv=1&invt=AbzwSQ&project=helical-glass-264223

https://console.cloud.google.com -> iam-admin -> serviceaccounts -> polyglot