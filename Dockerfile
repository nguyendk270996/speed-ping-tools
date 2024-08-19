FROM ubuntu

#Install softwares
RUN echo "$TARGETPLATFORM"
RUN apt-get update -y
RUN apt-get install -y vim net-tools iputils-ping python3 jq curl
RUN if [ "$TARGETPLATFORM" = "linux/amd64" ] ; then \
    curl -O https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-x86_64.tgz && \
    tar -xvzf ookla-speedtest-1.2.0-linux-x86_64.tgz ;\
else \
    curl -O https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-aarch64.tgz && \
    tar -xvzf ookla-speedtest-1.2.0-linux-aarch64.tgz ;\
fi
RUN cp ./speedtest /bin/speedtest 
COPY network-tools.py .
RUN speedtest --accept-license & 
RUN sleep 5
CMD [ "python3", "network-tools.py" ]
#ENTRYPOINT ["tail", "-f", "/dev/null"]