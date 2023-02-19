import boto3
import yaml

def create_ec2_instance():
    """
    Creates a new EC2 instance on AWS.

    Returns:
        dict: A dictionary containing the instance ID, public IP address, and other details.
    """
    ec2 = boto3.resource('ec2')
    instance = ec2.create_instances(
        ImageId='ami-example-img-id',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro')
    instance_id = instance[0].id
    instance_public_ip = ec2.Instance(instance_id).public_ip_address
    return {
        'instance_id': instance_id,
        'instance_public_ip': instance_public_ip
    }

def create_kubernetes_cluster():
    """
    Creates a new Kubernetes cluster on GCP.

    Returns:
        dict: A dictionary containing the cluster name, endpoint URL, and other details.
    """
    gke = boto3.client('gke')
    # read configuration from a YAML file
    with open('gke-config.yaml') as f:
        config = yaml.safe_load(f)
    response = gke.create_cluster(config)
    return response['name'], response['endpoint']

