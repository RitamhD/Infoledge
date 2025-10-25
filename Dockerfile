# base image
FROM python:3.11-slim

# working directory
WORKDIR /app

# copy 
COPY . /app

# run
RUN pip install --no-cache-dir -r requirements.txt

# port
EXPOSE 5000

# execute using gunicorn
CMD [ "gunicorn", "-w", "4", "-k", "gevent", "-b", "0.0.0.0:5000", "app:app" ]
