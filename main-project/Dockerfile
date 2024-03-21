ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

# Copy the source code into the container.
COPY . /app/
#Copy the requirements file into the container.
COPY ./requirements.txt /app
#RUN pip install --no-cache-dir -r requirements.txt
RUN apt update
RUN apt install python3 -y
RUN pip install -r requirements.txt
#RUN python -m pip install elasticsearch-----done in the requirements.txt
