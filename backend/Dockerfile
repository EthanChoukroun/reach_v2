FROM rust:latest

WORKDIR /usr/app

COPY . .

ENTRYPOINT ["/usr/app/reach-cli"]

CMD [ "start", "-b", "0.0.0.0" ]