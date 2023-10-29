from kubernetes import client, config, watch
import logging
import time
import os

log = logging.getLogger(__name__)
is_cluster = True
try:
    # Try to load the in-cluster configuration
    config.load_incluster_config()
except config.ConfigException:
    # If it fails (meaning we're outside of the cluster), load the kubeconfig
    try:
        config.load_kube_config()
        is_cluster = False
    except config.ConfigException:
        raise RuntimeError("Could not configure kubernetes python client.")

w = watch.Watch()
batch_api = client.BatchV1Api()
core_api = client.CoreV1Api()

class TestrunnerClient:

    def __init__(self):
        self.timeout_seconds = 10 # TODO need to refactor outside of client instance

    # TODO implement test case
    def execute_code(self, session_id: str, code: str, problem_id: str):
        file_path = self.store_code_as_file(session_id, code)
        job_spec = self.create_job_spec(file_path, session_id, problem_id)
        job = batch_api.create_namespaced_job(
            namespace='default',
            body=job_spec
        )

        tle = False
        start_time = time.time()
        for event in w.stream(batch_api.list_namespaced_job, namespace='default', timeout_seconds=self.timeout_seconds): # TODO TLE
            log.info(event)
            if event['object'].metadata.name == session_id:
                if event['object'].status.succeeded == 1:
                    log.info("Job Completed Successfully")
                    w.stop()
                if event['object'].status.failed == 1:
                    log.error("Job Failed")
                    w.stop()
        if time.time() - start_time > self.timeout_seconds:
            tle = True

        if tle:
            return 'TLE'
        
        logs = self.get_job_pod_logs(session_id)
        return logs


    def store_code_as_file(self, session_id: str, code: str):
        dir = '/input' if is_cluster else '/home/nekozing/autograder-kubernetes-pv' # need to write to local mount
        file_path = os.path.join(dir, f'{session_id}.py')
        with open(file_path, 'w') as file:
            file.write(code)
        log.info('wrote code to path %s', file_path)
        return os.path.join('/input', f'{session_id}.py')

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
            args=[session_id, input_file_path, problem_id],
            volume_mounts=[volume_mount]
        )

        # Define the pod template which contains the container and volume
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(name=session_id),
            spec=client.V1PodSpec(restart_policy="Never", containers=[container], volumes=[volume])
        )

        # Define the job spec
        spec = client.V1JobSpec(
            active_deadline_seconds=self.timeout_seconds, # TODO dynamic TLE configuration
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
    
    def get_job_pod_logs(self, job_name: str, namespace='default'):
        pods = core_api.list_namespaced_pod(namespace, label_selector=f"job-name={job_name}").items
        if not pods:
            return None

        # Assuming job creates only one pod
        pod_name = pods[0].metadata.name
        
        # Get logs from that pod
        logs = core_api.read_namespaced_pod_log(pod_name, namespace)
        
        return logs