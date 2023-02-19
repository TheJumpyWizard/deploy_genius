import docker


class Registry:
    def __init__(self, registry_url, registry_username, registry_password):
        self.client = docker.from_env()
        self.registry_url = registry_url
        self.registry_username = registry_username
        self.registry_password = registry_password

    def login(self):
        self.client.login(username=self.registry_username, password=self.registry_password, registry=self.registry_url)

    def push(self, image_name, tag):
        self.client.images.push(repository=image_name, tag=tag)

    def pull(self, image_name, tag):
        self.client.images.pull(repository=image_name, tag=tag)

    def list_images(self):
        return self.client.images.list()

    def delete_image(self, image_name, tag):
        self.client.images.remove(image_name, tag=tag)

