from pydantic import BaseModel

class TestResult(BaseModel):
    session_id: str
    message: str
    total_tests: int
    tests_passed: int
