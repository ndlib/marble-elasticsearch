# Marble Elasticsearch
## Description
AWS Elasticsearch is the service used to provide search capability for the [marble site](https://marble.library.nd.edu/). Every image collection to be included on the site first generates a IIIF manifest that contains the title, tags, and other metadata.  [Scripts](https://github.com/ndlib/marble-website-starter/blob/master/scripts/gatsby-source-iiif/indexSearch.js) then parse the manifest and write key peices of information to Elasticsearch. When end-users search the marble site they are searching through the data stored in Elasticsearch and relevant results based on their input are served back.

This repository is responsible for creating an Elasticsearch cluster with node(s) and configurating them appropriately. It does not generate IIIF manifest nor parse the data. To test CRUD operations once you've ran through the deployment steps see src/crud.py

## Installation
1. Setup pyenv - https://github.com/pyenv/pyenv
2. Setup aws-cdk - https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html

Use venv - https://docs.python.org/3/library/venv.html

venv is included in the Python standard library and requires no additional installation. Additional details in deployment.
## Testing
Use unittest - https://docs.python.org/3/library/unittest.html

Tests should be placed in test/unit

To execute all test: `python run_all_tests.py`
## Dependencies
### Development Dependencies
Review the dev-requirements.txt to update development packages
An example would be our linter package - flake8
### Production Dependencies
Review the install_requires in setup.py to update production packages
## Deployment
Changes to this repository are deployed via an AWS code pipeline.
### Local deployment to AWS
1. Setup virtual env
    1. python -m venv .env
    2. source .env/bin/activate
2. Run local deployment
    1. local-deploy.sh mystackname
3. Exit virtual env
    1. deactivate

## NOTES

