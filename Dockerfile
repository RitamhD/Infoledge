# base image
FROM python:3.10

# working directory
WORKDIR /app

# copy 
COPY . /app

# run
RUN pip install -r requirements.txt

# port
EXPOSE 5000

# execute
CMD [ "python", "./app.py" ]
