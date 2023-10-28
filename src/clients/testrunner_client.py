import uuid
from kubernetes import client, config
import logging

log = logging.getLogger(__name__)

try:
    # Try to load the in-cluster configuration
    config.load_incluster_config()
except config.ConfigException:
    # If it fails (meaning we're outside of the cluster), load the kubeconfig
    try:
        config.load_kube_config()
    except config.ConfigException:
        raise RuntimeError("Could not configure kubernetes python client.")

class TestrunnerClient:
    def __init__(self):
        self.batch_api = client.BatchV1Api()

    # TODO implement test case
    def execute_code(self, session_id: str, code: str, problem_id: str):
        file_path = self.store_code_as_file(session_id, code)
        job = self.create_job_spec(file_path, session_id, problem_id)
        self.batch_api.create_namespaced_job(
            namespace='default',
            body=job
        )
        return

    def store_code_as_file(self, session_id: str, code: str):
        file_path = f'/input/{session_id}.py'
        with open(file_path, 'w') as file:
            file.write(code)
        return file_path

    def create_job_spec(self, input_file_path: str, session_id: str, problem_id: str):
        volume = client.V1Volume(
            name="file-volume",
            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(claim_name="autograder-pvc")
        )

        # Define where to mount the volume in the container
        volume_mount = client.V1VolumeMount(
            mount_path="/input",  # Change to desired path in the container
            name="file-volume"
        )

        # Define the container to run in the job
        container = client.V1Container(
            name='testrunner-container',
            image="testrunner:latest",
            image_pull_policy='IfNotPresent',
            command=[input_file_path, problem_id],
            volume_mounts=[volume_mount]
        )

        # Define the pod template which contains the container and volume
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(name=session_id),
            spec=client.V1PodSpec(restart_policy="Never", containers=[container], volumes=[volume])
        )

        # Define the job spec
        spec = client.V1JobSpec(
            template=template,
            ttl_seconds_after_finished=600,
            backoff_limit=0  # Specifies the number of retries before marking the job as failed
        )

        # Define the job
        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=session_id),
            spec=spec
        )

        return job

    # def execute_code(self, problem_id: str, code: str):
    #     result = None
    #     with tempfile.NamedTemporaryFile(suffix='.py', delete=True) as tmp:
    #         tmp.write(code)
    #         print(code)
    #         tmp.flush()
    #         try:
    #             result = subprocess.check_output(['docker', 'run', '-v', f'{tmp.name}:/input/solution.py', 'testrunner', problem_id])
    #         except subprocess.CalledProcessError as e:
    #             print(e.output, file=sys.stderr)
    #             raise e    
    #     result = subprocess.check_output(['docker', 'run', '-v', f'{tmp.name}:/input/solution.py', 'testrunner', problem_id])
    #     return result