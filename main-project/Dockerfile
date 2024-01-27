ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

WORKDIR /usr/src/app

#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt
RUN apt update
RUN apt install python3 -y
RUN python -m pip install elasticsearch
# Copy the source code into the container.
COPY main.py ./

# Expose the port that the application listens on.
EXPOSE 9200

# Run the application.
#CMD ["python", "./src/main.py"]
