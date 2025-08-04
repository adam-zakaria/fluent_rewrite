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
`pipenv shell`
`pm2 start 'python app.py' --name 'fluent_prod'`

# Google API Key
https://console.cloud.google.com/iam-admin/serviceaccounts/details/106783039422957699297;edit=true/keys?inv=1&invt=AbzwSQ&project=helical-glass-264223

https://console.cloud.google.com -> iam-admin -> serviceaccounts -> polyglot

# More thoughts
The load is long for a 'very competitive' app in the mainstream market (can tell because I've been browsing all day then came to fluent and almost fell asleep)

Need to use usb + safari devtools or xcode to troubleshoot

