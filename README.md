# Deploy Genius (WIP - Refactoring)
###### Deploy Genius is a Python project that demonstrates how to automate the deployment of containerized applications to multiple servers using Docker and Kubernetes.

The project provides a set of tools for deploying containerized applications and managing the deployment process. These tools include:

* A configuration file format that allows users to define the parameters of their deployment in a single file
* A set of Python scripts for deploying applications to Docker and Kubernetes
* Monitoring capabilities that allow users to monitor the performance of their applications in real-time
* A centralized registry for storing and managing container images
* Logging capabilities that allow users to log the output of their applications to a centralized location

### Installation
1. Clone the repository to your local machine
2. Install the required dependencies by running pip install -r requirements.txt
3. Create a .env file in the root directory and define the following environment variables:
* DOCKER_USERNAME: Your Docker username
* DOCKER_PASSWORD: Your Docker password
* K8S_DEPLOYMENT_FILE: The path to the Kubernetes deployment file
* K8S_SERVICE_FILE: The path to the Kubernetes service file
* Create a config.yaml file in the root directory to define the parameters of your deployment. The following parameters are available:
    * docker_image_name: The name of your Docker image
    * app_name: The name of your application
    * app_port: The port your application will listen on
    * namespace: The namespace to deploy your application to
    * deployment_name: The name of your Kubernetes deployment
4. Run python main.py -c config.yaml to deploy your application

### Usage
To use Deploy Genius, follow these steps:

1. Define the parameters of your deployment in a config.yaml file
2. Run python main.py -c config.yaml to deploy your application
3. Monitor the performance of your application using the monitoring tools provided by Deploy Genius
4. Use the logging tools provided by Deploy Genius to log the output of your application to a centralized location

### Contributing
We welcome contributions to Deploy Genius! If you'd like to contribute, please follow these steps:

1. Fork the repository
2. Create a new branch for your changes
3. Make your changes and test them thoroughly
4. Create a pull request with a detailed description of your changes
5. I'll review your pull request as soon as possible and get back to you with any feedback or questions.

### License
Deploy Genius is released under the MIT license. See LICENSE for more information.