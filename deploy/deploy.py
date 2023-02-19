import os
import yaml
from kubernetes import client, config
import docker

config.load_kube_config()

v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

DOCKER_IMAGE_NAME = os.environ.get('DOCKER_IMAGE_NAME', 'deploy-genius')
APP_NAME = os.environ.get('APP_NAME', 'deploy-genius')
APP_PORT = os.environ.get('APP_PORT', 5000)
NAMESPACE = os.environ.get('NAMESPACE', 'default')
DEPLOYMENT_NAME = os.environ.get('DEPLOYMENT_NAME', 'deploy-genius')

def deploy(docker_username, docker_password, k8s_deployment_file, k8s_service_file, instance_public_ip):
    # Define the container spec for the deployment
    container = client.V1Container(
        name=APP_NAME,
        image=DOCKER_IMAGE_NAME,
        ports=[client.V1ContainerPort(container_port=APP_PORT)]
    )

    # Define the pod spec for the deployment
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={'app': APP_NAME}),
        spec=client.V1PodSpec(containers=[container])
    )

    # Define the deployment spec
    spec = client.AppsV1DeploymentSpec(
        replicas=1,
        template=template,
        selector={'matchLabels': {'app': APP_NAME}}
    )

    # Define the deployment object
    deployment = client.AppsV1Deployment(
        metadata=client.V1ObjectMeta(name=DEPLOYMENT_NAME),
        spec=spec
    )

    # Create the deployment
    resp = apps_v1.create_namespaced_deployment(body=deployment, namespace=NAMESPACE)

    print("Deployment created. status='%s'" % resp.metadata.name)

    # Wait for deployment to be ready
    while True:
        resp = apps_v1.read_namespaced_deployment_status(DEPLOYMENT_NAME, NAMESPACE)
        available_replicas = resp.status.available_replicas
        desired_replicas = resp.spec.replicas

        if available_replicas == desired_replicas:
            break

    # Define the service object
    service = client.V1Service(
        metadata=client.V1ObjectMeta(name=APP_NAME),
        spec=client.V1ServiceSpec(
            type='NodePort',
            selector={'app': APP_NAME},
            ports=[client.V1ServicePort(port=APP_PORT, target_port=APP_PORT)]
        )
    )

    # Create the service
    resp = v1.create_namespaced_service(body=service, namespace=NAMESPACE)

    print("Service created. status='%s'" % resp.metadata.name)

if __name__ == '__main__':
    deploy()

