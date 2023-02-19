import os
import time
from kubernetes import client, config
from .logger import get_logger

logger = get_logger(__name__)

config.load_incluster_config()  # Use service account token to authenticate with Kubernetes API

# Set up Kubernetes API client objects
v1 = client.CoreV1Api()
v1beta1 = client.ExtensionsV1beta1Api()

# Set up alert recipient email address (or phone number for SMS)
ALERT_RECIPIENT = os.environ.get("ALERT_RECIPIENT")


def monitor_deployments(namespace):
    """
    Monitor the state of the Deploy Genius deployments in the specified namespace.
    Send email alerts if any pods are not running as expected.
    """
    while True:
        logger.info(f"Monitoring deployments in namespace {namespace}...")

        # Query Kubernetes API for list of Deploy Genius deployments in namespace
        deployments = v1beta1.list_namespaced_deployment(namespace=namespace)

        # Check state of each deployment and send alerts if necessary
        for deployment in deployments.items:
            if deployment.status.available_replicas == 0:
                send_alert(f"Deployment {deployment.metadata.name} has 0 available replicas.")
            elif deployment.status.unavailable_replicas is not None and deployment.status.unavailable_replicas > 0:
                send_alert(f"Deployment {deployment.metadata.name} has {deployment.status.unavailable_replicas} unavailable replicas.")

        time.sleep(60)  # Wait 1 minute before checking again


def send_alert(message):
    """
    Send an email alert to the specified recipient.
    """
    # TODO: Implement email alerting (or SMS alerting)
    logger.warning(f"ALERT: {message}")
    if ALERT_RECIPIENT:
        # TODO: Send email or SMS message to ALERT_RECIPIENT
        pass

