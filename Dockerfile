  
FROM python:3.7.7-alpine3.10

WORKDIR /webinar

RUN mkdir templates 
COPY templates/handle_input.html templates/
COPY uploader.py .
COPY requirements.txt .

RUN pip install --upgrade pip && pip install --trusted-host pypi.python.org -r requirements.txt

ENV FLASK_APP uploader.py

CMD ["python", "uploader.py"]
