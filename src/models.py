from pydantic import BaseModel
from typing import Optional, List
from shared.models import GradeCodeError, TestRunnerResult

class GradeProblemRequest(BaseModel):
    user_id: Optional[str] = 'testuser'
    code: str

# for now, this is a copy of GradeCodeResult, but the separation of GetProblemResponse and GradeCodeResult
# is intentional as I expect models to diverge, as this response may contain user info.
class GradeProblemResponse(BaseModel):
    session_id: str
    error: Optional[GradeCodeError] = None
    llm_guidance: Optional[str] = None
    test_results: Optional[TestRunnerResult] = None

class ListProblemsResponse(BaseModel):
    problem_id_list: List[str]

class GetProblemStatementResponse(BaseModel):
    problem_id: str
    problem_statement: str