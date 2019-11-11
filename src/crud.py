#!/usr/bin/env python
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from config import DeployConfig
import boto3
import sys

session = boto3.Session()
cfg = DeployConfig()
# exit if cannot load config
if not cfg.config:
    sys.exit(1)

# retrieve es endpoint
aws_domains = boto3.client('es').describe_elasticsearch_domains(
    DomainNames=[cfg.get_stackname()]
)
host = aws_domains['DomainStatusList'][0]['Endpoint']
region = session.region_name
service = 'es'

# create signature for es request
credentials = session.get_credentials()
awsauth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    region,
    service,
    session_token=credentials.token)

# es config
es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

# single doc CRUD ops
# es doc
document = {
    "title": "Moneyball",
    "director": "Bennett Miller",
    "year": "2011"
}

# create multiple indices
indices = ["movies", "sampler", "digdug"]
settings = {'settings': {'number_of_shards': 1, 'number_of_replicas': 1}}
for idx in indices:
    es.indices.create(index=idx, body=settings)

    # insert doc into es
    es.indices.put_settings(index=idx, body={"number_of_replicas": 1})
    es.index(index=idx, doc_type="_doc", id='11', body=document)

    # update doc in es
    document = {
        "title": "Million Dollar Arm",
        "director": "Craig Gillespie",
        "year": "2014"
    }
    es.update(index=idx, doc_type='_doc', id='11', body={"doc": document, "doc_as_upsert": True})

    # retrieve doc from es
    print(es.get(index=idx, doc_type="_doc", id="11"))

    # delete index movies
    es.indices.delete(index=idx)
