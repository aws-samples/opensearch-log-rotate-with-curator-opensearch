import boto3
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection
import curator
import os

retention_in_days = int(os.environ.get('RETENTION_IN_DAYS'))
host = os.environ.get('OPENSEARCH_HOST')
region = os.environ.get('AWS_REGION')
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key,
                   credentials.secret_key,
                   region,
                   service,
                   session_token=credentials.token)


def lambda_handler(event, context):
    print("Checking {} OpenSearch domain".format(host))
    client = OpenSearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    # Listing all indexes
    index_list = curator.IndexList(client)

    # Filtering out Kibana
    index_list.filter_kibana()

    # Filtering index list to be deleted
    index_list.filter_by_age(source='name',
                             direction='older', timestring='%Y.%m.%d', unit='days', unit_count=retention_in_days)
    print("Found {} indices that are older than {} to delete".format(len(index_list.indices), retention_in_days))

    # Deleting indexes
    if len(index_list.indices) > 0:
        curator.DeleteIndices(index_list).do_action()
    else:
        print("There is no index to delete")


if __name__ == "__main__":
    event = ''
    context = []
    lambda_handler(event, context)
