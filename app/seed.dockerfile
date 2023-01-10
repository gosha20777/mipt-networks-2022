FROM python:3.9
WORKDIR /opt/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python seed.py