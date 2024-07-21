import boto3
from botocore.exceptions import ClientError

def create_ecr_repository(repository_name):
    try:
        # Create ECR client
        ecr_client = boto3.client('ecr', region_name='eu-north-1')

        # Create repository
        response = ecr_client.create_repository(repositoryName=repository_name)
        
        # Retrieve and print repository URI
        repository_uri = response['repository']['repositoryUri']
        print(f"Repository URI: {repository_uri}")

    except ClientError as e:
        print(f"An error occurred: {e}")

# Define repository name
repository_name = "my-monitoring-app-image"  # Use a valid repository name
create_ecr_repository(repository_name)
