#!/bin/bash
export JAVA_OPTS="-Djboss.management.client_socket_bind_address=$OPENSHIFT_WILDFLY_IP"
/usr/share/wildfly/bin/jboss-cli.sh "$@"
