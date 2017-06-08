#!/bin/sh

set -e


# Adding a user if needed to be able to communicate with docker
GROUP=nogroup
if [ -e /var/run/docker.sock ]; then
  GROUP=$(ls -l /var/run/docker.sock | awk '{ print $4 }')
fi
useradd -g "${GROUP}" collectd-docker-collector

exec collectd -f -C /tmp/collectd.conf "$@" > /dev/null