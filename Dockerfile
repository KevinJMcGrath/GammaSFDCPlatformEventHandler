FROM python:3.8-slim-buster


MAINTAINER Kevin McGrath "kevin.mcgrath@symphony.com"

# Copy req file and install dependencies
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Add app source code to image
ADD . /app
WORKDIR /app

CMD [ "python", "main.py" ]