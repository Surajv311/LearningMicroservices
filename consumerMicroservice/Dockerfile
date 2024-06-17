## For Task10
## Taking businessMicroservice Dockerfile as reference and created this one - check readme file for more task details
FROM python:3.9-slim
LABEL maintainer="suraj.verma@getsimpl.com"
ENV APP_HOME /consumermicroservice
ENV APP_MODE_DOCKER=docker_mode_consumer_service
RUN mkdir $APP_HOME
WORKDIR $APP_HOME
COPY . /$APP_HOME
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 6800
ENTRYPOINT ["sh", "-c"]
CMD ["uvicorn app:app --host 0.0.0.0 --port 6800 --reload"]
