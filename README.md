# python concurrent calls to backend rest APIs

```
This is a demo to show a service accepting an array of input json string and make 
concurrent calls to the BACKEND rest APIs and collect return values
```
## Installing 

### Python Requirements
```
sudo pip install virtualenv
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

## Test Locally

### Activate virtualenv
```
virtualenv env
source env/bin/activate
gunicorn -b :8080 -c gunicorn.conf.py main:app
```
