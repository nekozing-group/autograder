* Build docker image: `docker build -t testrunner ./testrunner/`
* Start server: `uvicorn src/server:app --reload`
* Test Request: `curl -X POST -H "Content-Type: application/json" --data @test_code.json http://127.0.0.1:8000/grade/01`

* Debug docker image file structure: `docker run -it --entrypoint /bin/sh testrunner`

Autograder Development Notes:
v0.0.1: Able to execute code within container.
v0.0.9: able to execute a specified test against the input file

TODO:

v0.1  : able to execute a specified series of tests against the intput file
v0.5: add interview algorithm test cases in testrunner
v0.8: add LLM code analysis in server
v0.9: add error memorization in server