from .models import GradeCodeResult, GradeCodeError, JobResult
from .clients.llm_client import LLMClient
from .clients.testrunner_client import TestrunnerClient, TimeLimitExceededException, JobExecutionException
from .clients.problem_data_client import ProblemDataClient

testrunner_client = TestrunnerClient()

# the grader is the "teacher" of the code, which grades the code and gives comments
class Grader:
    def grade_code(self, session_id: str, code: str, problem_id: str) -> GradeCodeResult:
        grade_code_result = GradeCodeResult(session_id=session_id)
        try:
            result = testrunner_client.execute_code(session_id, code, problem_id)
            grade_code_result.test_results = result.test_results
            if result.test_results.error != None or (result.test_results.num_tests_passed != result.test_results.num_total_tests):
                # ask llm
                pass
        except Exception as e:
            error = GradeCodeError(error_type=type(e).__name__, message=str(e))
            grade_code_result.error = error
        
        return grade_code_result

        