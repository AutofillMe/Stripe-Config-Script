# Stripe-Config-Script
Wrapper that runs all necessary tasks to check, validate, and correct a client's Stripe configuration for Switch Ops

## How to run
Usage:
```
usage: stripeConfigScript.py [-h] [-a A_ID] [-t CLIENTTYPE] [-f STRIPEEXPORT]
```

Options:
```
-h, --help                      show this help message and exit
-a, --acct A_ID                 <str> account_id of the client
-t, --client-type CLIENTTYPE    <int> what type of client they are (1, 2, 3, 4)
-f, --file STRIPEEXPORT         <path> path to csv file to parse data from
```

The script expects the following default file tree (unless otherwise specified by passing the -f flag):
```
project/
    ├── export.csv
    └── stripeConfigScript.py
```
