FROM python:3.12

WORKDIR /src

COPY ./lecture_1 ./lecture_1
COPY ./lecture_4/load_test/requirements.txt ./

RUN pip install -r requirements.txt

CMD ["uvicorn", "lecture_1.math_api.app:app", "--host", "0.0.0.0", "--port", "8080"]