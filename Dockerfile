FROM shared:latest

COPY requirements.txt /server/requirements.txt
RUN pip install -r /server/requirements.txt

# Creating folders, and files for a project:
COPY . /server

RUN chmod +x /server/entrypoint.sh

WORKDIR /server
ENTRYPOINT ["/server/entrypoint.sh"]