FROM python:3.8

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

CMD ["gunicorn", "wsgi:flask_app(start_scheduler=True)", "-w", "2", "-b", "0.0.0.0:7500"]
