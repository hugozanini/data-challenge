import boto3
from moto import mock_athena, mock_s3
import logging
import logging.config

from json_schema_to_hive import Athena

logging.config.fileConfig('exercicio2/logging.conf')
log = logging.getLogger('schema_to_hive')

@mock_athena
@mock_s3
def main():
    _S3_CLIENT = boto3.client("s3", region_name='us-east-1')
    _S3_CLIENT.create_bucket(Bucket='iti-query-results')

    _ATHENA_CLIENT = boto3.client('athena', region_name='us-east-1')
    print("Type:", type(_ATHENA_CLIENT))
    #TODO: Eschema path should be a parameter
    athena = Athena('exercicio2/schema.json', _ATHENA_CLIENT)

    athena.handler()

if __name__ == "__main__":
    main()