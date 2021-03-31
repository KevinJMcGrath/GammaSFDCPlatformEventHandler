import logging
import yaml

from kubernetes import client, config
from pathlib import Path

def load_config():
    kpath = Path('./config/kube_config.yaml')

    with open(kpath, 'r') as config_file:
        ky = yaml.safe_load(config_file)


def create_secret(secret_name, bot_config_64, private_key_64):
    secret_data = {
        "config.json": bot_config_64.decode("utf-8"),
        "private.pem": private_key_64.decode("utf-8")
    }

    secret = client.V1Secret()
    secret.metadata = client.V1ObjectMeta(name=secret_name)
    secret.type = 'Opaque'
    secret.data = secret_data

    return secret

def publish_secret(namespace, secret):
    config.load_kube_config()

    core_v1 = client.CoreV1Api()

    try:
        resp = core_v1.create_namespaced_secret(namespace=namespace, body=secret)
        logging.info(f'Secret secreted: {resp.metadata.name}')
    except client.exceptions.ApiException as e_api:
        if e_api.status == 409:
            resp = core_v1.replace_namespaced_secret(name=secret.metadata.name, body=secret, namespace=namespace)
            logging.info(f'Secret replaced - {resp.metadata.name}')
        else:
            logging.error('Exception while calling CoreV1Api.create_namespaced_secret')
            logging.exception(e_api)

def create_deployment(deployment_name, image):
    volume = client.V1Volume(name='config', secret=client.V1SecretVolumeSource(secret_name=deployment_name))

    container = client.V1Container(name=deployment_name, image=image,
                                   volume_mounts=[client.V1VolumeMount(mount_path='/app/config', name='config')],
                                   ports=[client.V1ContainerPort(container_port=80)],
                                   resources=client.V1ResourceRequirements(
                                       requests={"cpu": "10m", "memory": "100Mi"},
                                       limits={"cpu": "100m", "memory": "500Mi"})
                                   )
    security_context = client.V1SecurityContext(run_as_non_root=True, run_as_user=2000)

    pod_template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": deployment_name, "network": "all-egress", "group": "mtadminbot"}),
        spec=client.V1PodSpec(containers=[container], volumes=[volume], security_context=security_context)
    )

    deployment_spec = client.V1DeploymentSpec(replicas=1,
                                   template=pod_template, selector={"matchLabels": {"app": deployment_name}})

    deployment = client.V1Deployment(api_version="apps/v1", kind="Deployment", spec=deployment_spec,
                                    metadata=client.V1ObjectMeta(name=deployment_name, labels={"group": "mtadminbot"}))

    return deployment


def publish_deployment(namespace, deployment):
    apps_v1 = client.AppsV1Api()

    try:
        pass
    except client.exceptions.ApiException as e_api:
        if e_api.status == 409:
            resp = apps_v1.replace_namespaced_deployment(name=deployment.metadata.name, body=deployment,
                                                         namespace=namespace)
            logging.info(f'Deployment created - {resp.metadata.name}')
        else:
            logging.error('Exception while calling AppsV1Api.create_namespaced_deployment')
            logging.exception(e_api)
