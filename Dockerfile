FROM alpine:latest

RUN apk update && apk upgrade
RUN apk add curl git g++ make cmake jq mosquitto-clients coreutils bash

ADD sources/ /opt/
ADD config/ /etc/inverter/

RUN mkdir /opt/inverter-cli/bin
RUN cd /opt/inverter-cli/ && cmake . && make
RUN mv /opt/inverter-cli/inverter_poller opt/inverter-cli/bin/ 

HEALTHCHECK \
    --interval=30s \
    --timeout=10s \
    --start-period=1m \
    --retries=3 \
  CMD /opt/healthcheck

WORKDIR /opt
ENTRYPOINT ["/bin/bash", "/opt/inverter-mqtt/entrypoint.sh"]
