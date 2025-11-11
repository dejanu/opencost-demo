* Setup

1. IAM user that has access to the Cost and Usage Report (CUR): with the correct policies
2. S3 bucket storing Athena query results which OpenCost user has permission to access

* Test script `upload_tos3.py` for upload parquet files to S3 bucket

```bash
# access key for AWS user with read-only access to OpenCost S3 bucket
export AWS_ACCESS_KEY_ID="INSERT"
export AWS_SECRET_ACCESS_KEY="INSERT"

# create venv
python -m venv .opencost
source .opencost/bin/activate

pip install -r requirements.txt

# install pyarrow from binary only to avoid build issues
pip install pyarrow --only-binary=:all:
```

* Test Athena query create database `cost_and_usage` and table `cur_table`

```sql

CREATE DATABASE IF NOT EXISTS cost_and_usage;

CREATE EXTERNAL TABLE IF NOT EXISTS cost_and_usage.cur_table (
    line_item_usage_account_id string,
    product_product_name string,
    line_item_usage_start_date timestamp,
    line_item_usage_end_date timestamp,
    line_item_unblended_cost double,
    line_item_usage_amount double,
    line_item_currency_code string
)
STORED AS PARQUET
LOCATION 's3://opencost-cur-bucket-demo/AWS_CUR_Test/';

/* test query */
SELECT * FROM cost_and_usage.cur_table;
```

* For Cloud Costs create `cloud-integration.json` as a secret `kubectl create secret generic cloud-costs --from-file=./cloud-integration.json --namespace opencost`

```json
{
  "aws": {
    "athena": [
      {
        "bucket": "<ATHENA_BUCKET_NAME>",
        "region": "<ATHENA_REGION>",
        "database": "<ATHENA_DATABASE>",
        "table": "<ATHENA_TABLE>",
        "workgroup": "<ATHENA_WORKGROUP>",
        "account": "<ACCOUNT_NUMBER>",
        "authorizer": {
          "authorizerType": "AWSAccessKey",
          "id": "AKXXXXXXXXXXXXXXXXXXXX",
          "secret": "superdupersecret/superdupersecret"
        }
      }
    ]
  }
}
```

* Upgrade chart installation

```bash
helm upgrade -i opencost opencost-charts/opencost \
  --set opencost.cloudIntegrationSecret=cloud-costs \
  --set opencost.cloudCost.enabled=true \
  -n opencost
```