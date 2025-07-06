FROM rasa/rasa:3.6.10
WORKDIR /app
COPY ./src /app
ENTRYPOINT [ "/bin/bash" ]