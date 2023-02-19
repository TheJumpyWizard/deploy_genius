import argparse
import os
import yaml
from dotenv import load_dotenv
from deploy.deploy import deploy_application

load_dotenv()

def read_config():
    # Read from env vars or .env file
    symbol = os.environ.get('SYMBOL')
    api_key = os.environ.get('API_KEY')
    url = os.environ.get('URL')
    docker_username = os.environ.get('DOCKER_USERNAME')
    docker_password = os.environ.get('DOCKER_PASSWORD')
    k8s_deployment_file = os.environ.get('K8S_DEPLOYMENT_FILE')
    k8s_service_file = os.environ.get('K8S_SERVICE_FILE')

    if not symbol or not api_key or not url or not docker_username or not docker_password or not k8s_deployment_file or not k8s_service_file:
        with open('.env') as f:
            for line in f:
                if not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    if key == 'SYMBOL':
                        symbol = value
                    elif key == 'API_KEY':
                        api_key = value
                    elif key == 'URL':
                        url = value
                    elif key == 'DOCKER_USERNAME':
                        docker_username = value
                    elif key == 'DOCKER_PASSWORD':
                        docker_password = value
                    elif key == 'K8S_DEPLOYMENT_FILE':
                        k8s_deployment_file = value
                    elif key == 'K8S_SERVICE_FILE':
                        k8s_service_file = value
    
    return symbol, api_key, url, docker_username, docker_password, k8s_deployment_file, k8s_service_file

def parse_args():
    parser = argparse.ArgumentParser(description='Automate deployment of trading systems to multiple servers using containerization technologies like Docker and Kubernetes.')
    parser.add_argument('--config', '-c', help='Path to the YAML configuration file')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    if args.config:
        with open(args.config) as f:
            config = yaml.safe_load(f)
        symbol = config.get('symbol')
        api_key = config.get('api_key')
        url = config.get('url')
        docker_username = config.get('docker_username')
        docker_password = config.get('docker_password')
        k8s_deployment_file = config.get('k8s_deployment_file')
        k8s_service_file = config.get('k8s_service_file')
    else:
        symbol, api_key, url, docker_username, docker_password, k8s_deployment_file, k8s_service_file = read_config()

    deploy_application(symbol, api_key, url, docker_username, docker_password, k8s_deployment_file, k8s_service_file)

