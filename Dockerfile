FROM ubuntu
ARG TARGET-PLF=linux-x86_64
ENV TARGET-PLF=$TARGET-PLF
#Install softwares
RUN apt-get update -y
RUN apt-get install -y vim net-tools iputils-ping python3 jq curl && \
curl -O https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-${TARGET-PLF}.tgz && \
tar -xvzf ookla-speedtest-1.2.0-${TARGET-PLF}.tgz && cp ./speedtest /bin/speedtest
COPY network-tools.py .
RUN speedtest --accept-license & 
RUN sleep 5
CMD [ "python3", "network-tools.py" ]
#ENTRYPOINT ["tail", "-f", "/dev/null"]