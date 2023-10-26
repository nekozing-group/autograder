# Dev Notes



* Build testrunner docker image: `docker build -t testrunner ./testrunner/`



* Start server: `uvicorn src/server:app --reload`
* Test Request: `curl -X POST -H "Content-Type: application/json" --data @test_code.json http://127.0.0.1:8000/grade/01`
* Builder Server Image: `docker build -t autograder .`
* Start server container: `docker run -p 8001:8001 autograder`

* Debug docker image file structure: `docker run -it --entrypoint /bin/sh testrunner`



# Milestones

v0.0.1: Able to execute code within container.  
v0.0.9: able to execute a specified test against the input file  
v0.1  : add basic UI  
  
TODO:  
  
v0.2  : able to execute a specified series of tests against the input file  
v0.3  : able to dynamically load tests in the UI  
v0.5  : add interview algorithm test cases in testrunner  
v0.8  : add LLM code analysis in server  
v0.9  : add error memorization in server  