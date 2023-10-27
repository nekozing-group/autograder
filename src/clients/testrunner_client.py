import subprocess
import tempfile
import sys
from kubernetes import client, config

class TestrunnerClient:
    def __init__(self):
        config.load_kube_config()
        self.api = client.BatchV1Api()

    def execute_code(self, problem_id: str, code: str):
        job = {
            
        }
        self.api.create_namespaced_job(
            namespace='default',
            body=job
        )
        pass

    def create_job_spec(self):
            volume = client.V1Volume(
                name="testrunner:latest",
                persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(claim_name="sandbox-pvc")
            )

            # Define where to mount the volume in the container
            volume_mount = client.V1VolumeMount(
                mount_path="/input",  # Change to desired path in the container
                name="my-volume"
            )

            # Define the container to run in the job
            container = client.V1Container(
                name="my-container",
                image="testrunner:latest",
                command=["your-command", "arg1", "arg2"],  # If you have a specific command to run
                volume_mounts=[volume_mount]
            )

            # Define the pod template which contains the container and volume
            template = client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": "my-job"}),
                spec=client.V1PodSpec(restart_policy="Never", containers=[container], volumes=[volume])
            )

            # Define the job spec
            spec = client.V1JobSpec(
                template=template,
                backoff_limit=4  # Specifies the number of retries before marking the job as failed
            )

            # Define the job
            job = client.V1Job(
                api_version="batch/v1",
                kind="Job",
                metadata=client.V1ObjectMeta(name="my-job"),
                spec=spec
            )

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