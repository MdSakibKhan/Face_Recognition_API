FROM python:3.8.8

WORKDIR /root/.deepface/weights/

COPY /weights /root/.deepface/weights/

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN pip install deepface

RUN apt-get update && apt-get install -y python3-opencv

EXPOSE 5000

CMD [ "python", "./api.py" ]
