#Vendasta Client

A simple (and incomplete) client for Vendasta's Reputation Intelligence API

##How to use:

```
pip install -r requirements.txt
```

Once requirements are installed:

```
from vendasta_client import Vendasta

v = Vendasta(key='YOUR_KEY', user='YOUR_USER', base_url='YOUR_URL')
loc_data = {
    'companyName': 'some company',
    'address': 'some address',
}
result = v.accounts.search(loc_data)
```

## Available endpoints:

### /accounts/search/
`v.accounts.search(...)`
### /accounts/create/
`v.accounts.create(...)`
### /accounts/delete/
`v.accounts.delete(...)`

### /reviews/search/
`v.reviews.search(...)`

[Read the Vendasta API Docs](http://www.vendasta.com/documentation/reputation-intelligence)
