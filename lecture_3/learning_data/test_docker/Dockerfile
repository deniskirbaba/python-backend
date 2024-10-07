FROM python:latest

# Create and set the working directory
WORKDIR /testing

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY testing_script.py ./

ENTRYPOINT ["python", "testing_script.py"]
