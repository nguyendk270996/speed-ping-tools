FROM ubuntu
ARG TARGET=linux-x86_64
#Install softwares
RUN apt-get update -y
RUN apt-get install -y vim net-tools iputils-ping python3 jq curl && \
curl -O https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-$TARGET.tgz && \
tar -xvzf ookla-speedtest-1.2.0-$TARGET.tgz && cp ./speedtest /bin/speedtest
COPY network-tools.py .
RUN speedtest --accept-license
CMD [ "python3", "network-tools.py" ]
#ENTRYPOINT ["tail", "-f", "/dev/null"]