# s3-remove-public-access

This script will enable the public blocks for all S3 buckets in an AWS account.  
So make sure you don't have any static website hosting buckets because this will remove access.

## Requirements

- boto3
- rich

## Quickstart

```bash
python3 -m venv .venv
source .venv\bin\activate
pip install -r requirements.txt
python s3-block.py
```

## Preview

![alt text](screenshot.png)

## FAQ

Q. Why not just use the S3 option to block all public access at the account level?  
A. That does work but some scanners (and maybe AWS Security Hub) still check the bucket level for these settings.
