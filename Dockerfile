FROM debian:jessie

RUN echo "APT::Install-Recommends false;" >> /etc/apt/apt.conf.d/recommends.conf && \
    echo "APT::AutoRemove::RecommendsImportant false;" >> /etc/apt/apt.conf.d/recommends.conf && \
    echo "APT::AutoRemove::SuggestsImportant false;" >> /etc/apt/apt.conf.d/recommends.conf && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y collectd python-pip ca-certificates && \
    apt-get install -y curl && \
    curl -sL https://github.com/tianon/gosu/releases/download/1.4/gosu-amd64 > /usr/bin/gosu && \
    chmod +x /usr/bin/gosu && \
    apt-get remove -y curl && \
    apt-get autoremove -y

RUN apt-get install -y libpython2.7
RUN pip install freebox_v5_status collectd netaddr


COPY Docker/run.sh /run.sh
COPY Docker/collectd.conf /tmp/collectd.conf
COPY collectd-freeboxv5-plugin.py /usr/local/lib/python2.7/site-packages/collectd-freeboxv5-plugin.py
COPY freebox-types.db /usr/share/collectd/freebox-types.db


RUN chmod 700 /run.sh
#COPY . /go/src/github.com/bobrik/collectd-docker/collector

#RUN apt-get install -y golang-go git && \
#    GOPATH=/go go get github.com/bobrik/collectd-docker/collector/... && \
#    apt-get remove -y golang-go git && \
#    apt-get autoremove -y && \
#    mv /go/bin/collector /collector && \
#    rm -rf /go && \
#    chmod 6755 /collector

ENTRYPOINT ["/run.sh"]
#ENTRYPOINT ["/bin/bash"]