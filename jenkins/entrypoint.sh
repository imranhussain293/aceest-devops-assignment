#!/bin/sh
set -eu

# If corporate / MITM root CAs are mounted, install them.
# Mount path (see docker-compose.jenkins.yml): /certs/ca/*.crt
if [ -d /certs/ca ]; then
  found_ca=0
  for cert in /certs/ca/*.crt; do
    if [ -f "$cert" ]; then
      found_ca=1
      cp "$cert" "/usr/local/share/ca-certificates/$(basename "$cert")"
    fi
  done

  if [ "$found_ca" -eq 1 ]; then
    update-ca-certificates
  fi
fi

# Start Jenkins exactly like the base image.
exec /usr/bin/tini -- /usr/local/bin/jenkins.sh "$@"
