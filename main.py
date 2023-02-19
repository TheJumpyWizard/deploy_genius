import argparse
import os
import yaml
from dotenv import load_dotenv
from deploy.deploy import deploy
from utils.monitor import Monitor
from utils.registry import Registry
from utils.config import Config
from utils.logger import Logger
from data.providers import create_ec2_instance

load_dotenv()

def read_config():
    # Read from env vars or .env file
    docker_username = os.environ.get('DOCKER_USERNAME')
    docker_password = os.environ.get('DOCKER_PASSWORD')
    k8s_deployment_file = os.environ.get('K8S_DEPLOYMENT_FILE')
    k8s_service_file = os.environ.get('K8S_SERVICE_FILE')
    return docker_username, docker_password, k8s_deployment_file, k8s_service_file

def parse_args():
    parser = argparse.ArgumentParser(description='Automate deployment of trading systems to multiple servers using containerization technologies like Docker and Kubernetes.')
    parser.add_argument('--config', '-c', help='Path to the YAML configuration file')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    if args.config:
        with open(args.config) as f:
            config = yaml.safe_load(f)
        docker_username = config.get('docker_username')
        docker_password = config.get('docker_password')
        k8s_deployment_file = config.get('k8s_deployment_file')
        k8s_service_file = config.get('k8s_service_file')
    else:
        docker_username, docker_password, k8s_deployment_file, k8s_service_file = read_config()

    # create an EC2 instance
    instance_details = create_ec2_instance()
    instance_id = instance_details['instance_id']
    instance_public_ip = instance_details['instance_public_ip']
    print(f'Created EC2 instance with instance ID {instance_id} and public IP address {instance_public_ip}')

    # setup monitoring, registry, and logging
    monitor = Monitor()
    registry = Registry()
    config = Config()
    logger = Logger()

    # deploy the application to the EC2 instance
    deploy_application(docker_username, docker_password, k8s_deployment_file, k8s_service_file, instance_public_ip)

    # log some messages and metrics
    logger.log('Deployed application to EC2 instance')
    logger.log(f'EC2 instance ID: {instance_id}')
    logger.log(f'EC2 instance public IP: {instance_public_ip}')
    monitor.send_metric('ec2_instance_created', 1)
    registry.register_instance(instance_id, instance_public_ip)

    # get some configuration data
    db_url = config.get('db_url')
    api_key = config.get('api_key')
    logger.log(f'Database URL: {db_url}')
    logger.log(f'API key: {api_key}')

