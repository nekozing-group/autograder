from shared.models import GradeCodeResult, GradeCodeError, JobResult, TestRunnerState
from .clients.llm_client import LLMClient
from .clients.problem_data_client import ProblemDataClient
from .clients.testrunner_client import TestrunnerClient, TimeLimitExceededException, JobExecutionException
import logging

log = logging.getLogger(__name__)

testrunner_client = TestrunnerClient()
llm_client = LLMClient()

# the grader is the "teacher" of the code, which grades the code and gives comments
class Grader:
    def grade_code(self, session_id: str, code: str, problem_id: str) -> GradeCodeResult:
        grade_code_result = GradeCodeResult(session_id=session_id)
        try:
            job_result = testrunner_client.execute_code(session_id, code, problem_id)
            grade_code_result.test_results = job_result.test_results

            # if the results weren't perfect
            llm_guidance = False
            if job_result.error != None and job_result.error.testrunner_state in [TestRunnerState.COMPILE, TestRunnerState.BYTE_CODE]:
                llm_guidance = True
            elif job_result.test_results != None and job_result.test_results.num_tests_passed != job_result.test_results.num_total_tests:
                llm_guidance = True
            
            if llm_guidance:
                # TODO invoke llm for advice
                log.info('will call llm for guidance: code grading failed')
                log.info('job result: %s', job_result)
                llm_output = self.invoke_llm(code, problem_id)
                grade_code_result.llm_guidance = llm_output
        except Exception as e:
            error = GradeCodeError(error_type=type(e).__name__, message=str(e))
            grade_code_result.error = error
        
        return grade_code_result
    
    def invoke_llm(self, code, problem_id) -> str:
        data_client = ProblemDataClient(problem_id)
        problem_description = data_client.get_problem_description()
        reference_implementation = data_client.get_reference_implementation()
        return llm_client.get_llm_advice(problem_description, code, reference_implementation)
    