FROM python:3.9-slim

RUN pip install pytest

COPY . /testrunner

RUN chmod +x /testrunner/entrypoint.py
ENTRYPOINT ["python", "/testrunner/entrypoint.py"]