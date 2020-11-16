import sys

from bentobuild.builder import GenericBuilder
from bentobuild.build import KubernetesApiClient
from kubernetes import client
from kubernetes.client.rest import ApiException

default_name = "model-build"

# move to README -> The Tekton catalog bentoml and kaniko tasks must be installed prior to using
# the Tekton task builder
# kubectl apply -f https://github.com/tektoncd/catalog/blob/master/task/bentoml/0.1/bentoml.yaml
# kubectl apply -f https://raw.githubusercontent.com/tektoncd/catalog/master/task/kaniko/0.1/kaniko.yaml


# WIP WIP WIP WIP
class BentoTaskBuilder(GenericBuilder):
    def __init__(self, yatai_service=None):
        super().__init__(yatai_service)

        self.api = KubernetesApiClient(self.yatai_service)

        configuration = client.Configuration()

        apiclient = client.ApiClient(configuration)

        self.corev1 = client.CoreV1Api(apiclient)

        self.customv1 = client.CustomObjectsApi(apiclient)

    def safe_build(self,
                   service,
                   image,
                   ns,
                   cleanup=True,
                   name=default_name):

        print("class=BentoTaskBuilder fn=safe_build at=namespace ns=%s" % ns)

        if not self.check_ns_exists(ns):
            print("at=missing-build-ns ns=%s", ns)
            sys.exit(2)

        return self.create_builder_task(service, image, ns, name)


    def create_builder_task(self, service, image, ns, name=default_name):

        task_data= """
        {"apiVersion": "networking.istio.io/v1alpha3", "kind": "Gateway", "metadata": {"name": "gateway-xxxxxxxx", "namespace": "default"}, "spec": {"selector": {"istio": "ingressgateway"}, "servers": [{"port": {"number": 49999, "name": "tcp-49999", "protocol": "tcp"}, "hosts": ["*"]}]}}
        """

        try:
            created = self.batchv1.create_namespaced_job(
                namespace=ns,
                body=job)
        except ApiException as e:
            print(e)
            sys.Exit(1)

        return created

    def status(self, job):
        print("fn=status name=%s ns=%s" % (
            job.metadata.name,
            job.metadata.namespace))
        try:
            update = self.batchv1.read_namespaced_job(
                job.metadata.name,
                job.metadata.namespace)
            print(str(update.status))
        except ApiException as e:
            print("at=status error=%s" % e)
