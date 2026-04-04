#!/bin/sh
set -eu

# If corporate / MITM root CAs are mounted, install them.
# Mount path (see docker-compose.jenkins.yml): /certs/ca/*.{crt,cer,pem}
if [ -d /certs/ca ]; then
  found_ca=0
  for cert in /certs/ca/*; do
    if [ -f "$cert" ]; then
      case "$cert" in
        *.crt|*.cer|*.pem)
          found_ca=1
          base="$(basename "$cert")"
          case "$base" in
            *.crt) out_name="$base" ;;
            *) out_name="${base}.crt" ;;
          esac
          cp "$cert" "/usr/local/share/ca-certificates/${out_name}"
          ;;
      esac
    fi
  done

  if [ "$found_ca" -eq 1 ]; then
    update-ca-certificates
  fi
fi

# Optional (NOT recommended): disable Git HTTPS certificate verification.
# Prefer mounting your corporate root CA into ./jenkins/certs instead.
if [ "${GIT_SSL_NO_VERIFY:-}" != "" ]; then
  git config --system http.sslVerify false || true
fi

# Start Jenkins (drop privileges to the jenkins user).
if command -v su >/dev/null 2>&1; then
  exec /usr/bin/tini -- su -s /bin/sh jenkins -c "/usr/local/bin/jenkins.sh"
fi

exec /usr/bin/tini -- /usr/local/bin/jenkins.sh "$@"
