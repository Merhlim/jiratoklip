FROM python:2.7-slim
WORKDIR /jiratoklip
ADD . /jiratoklip
RUN pip install -r requirements.txt
CMD ["python","main.py"]
