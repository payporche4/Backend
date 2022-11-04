FROM python:3.10
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt
WORKDIR /app

ADD . .

# Local setup
# EXPOSE 8000

# CMD [ "gunicorn", "--bind", ":8000", "--workers", "3", "dockerlearn.wsgi:application"]

# HEROKU
CMD gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT