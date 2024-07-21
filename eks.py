from kubernetes import client, config

# Load Kubernetes configuration
config.load_kube_config()

# Create a Kubernetes API client
api_client = client.ApiClient()

# Define the deployment
deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="my-flask-app-v2"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "my-flask-app"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "my-flask-app"}
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="my-flask-container",
                        image="590183989048.dkr.ecr.us-east-1.amazonaws.com/my-monitoring-app-image",
                        ports=[client.V1ContainerPort(container_port=5000)]
                    )
                ]
            )
        )
    )
)

# Create the deployment (or replace if it already exists)
api_instance = client.AppsV1Api(api_client)
try:
    # Try to create the deployment
    api_instance.create_namespaced_deployment(
        namespace="default",
        body=deployment
    )
    print("Deployment created successfully.")
except client.exceptions.ApiException as e:
    if e.status == 409:  # Conflict error means the deployment already exists
        print("Deployment already exists, updating...")
        api_instance.replace_namespaced_deployment(
            name="my-flask-app-v2",
            namespace="default",
            body=deployment
        )
        print("Deployment updated successfully.")
    else:
        raise  # Re-raise exception if it's not a conflict error

# Define the service
service = client.V1Service(
    metadata=client.V1ObjectMeta(name="my-flask-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "my-flask-app"},
        ports=[client.V1ServicePort(port=5000)]
    )
)

# Create the service (or replace if it already exists)
api_instance = client.CoreV1Api(api_client)
try:
    # Try to create the service
    api_instance.create_namespaced_service(
        namespace="default",
        body=service
    )
    print("Service created successfully.")
except client.exceptions.ApiException as e:
    if e.status == 409:  # Conflict error means the service already exists
        print("Service already exists, updating...")
        api_instance.replace_namespaced_service(
            name="my-flask-service",
            namespace="default",
            body=service
        )
        print("Service updated successfully.")
    else:
        raise  # Re-raise exception if it's not a conflict error
