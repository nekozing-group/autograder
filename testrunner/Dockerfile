FROM python:3.9-slim

RUN pip install pytest

COPY entrypoint.py /entrypoint.py
COPY tests /tests

RUN chmod +x /entrypoint.py
# docker run -v /path/on/host:/path/in/container testrunner /path/in/container/filename.txt test1
ENTRYPOINT ["python", "/entrypoint.py"]