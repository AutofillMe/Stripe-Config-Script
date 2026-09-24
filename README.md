# Stripe-Config-Script
Wrapper that runs all necessary tasks to check, validate, and correct a client's Stripe configuration for Switch Ops

Currently, this uses 2 sub-processes:
- Standardize the Stripe export file
  > https://github.com/AutofillMe/Stripe-Export-Standardizer
- Check the client's current configuration against the expected configuration prior to initiation of a Stripe switch
  > https://github.com/AutofillMe/Stripe-Client-Config-Checker

Both are maintained independently of the wrapper to keep track of issues, features, and development separately.

## Requirements
Python >= 3.14 [download here](https://www.python.org/downloads/)

Make sure you add Python to your PATH

Git: [download here](https://git-scm.com/)

Once python is installed, run:
```
pip install pandas
```

## Usage
Please download this repo by running:
```
git clone https://github.com/AutofillMe/Stripe-Config-Script.git ./Stripe-Config-Script
```

### How to run
Inside the folder that was created, run:
```
python3 stripeConfigScript.py [-h] [-a A_ID] [-t CLIENT_TYPE] [-f STRIPE_EXPORT]
```

Options:
```
-h, --help                      show this help message and exit
-a, --acct A_ID                 <str> account_id of the client
-t, --client-type CLIENT_TYPE   <int> what type of client they are (1, 2, 3, 4)
-f, --file STRIPE_EXPORT        <path> path to csv file to parse data from
```

The script expects the following default file tree and name (unless otherwise specified by passing the -f flag):
```
project/
    ├── export.csv
    └── stripeConfigScript.py
```

## Features under Consideration
- Batch process acct_ids
- Auto-copy recommended fixes to clipboard (would need separate implementation for Windows and Mac/Linux)
