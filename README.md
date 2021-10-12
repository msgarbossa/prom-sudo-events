# prom-sudo-events

## Description

Prometheus exporter for sudo events in journald.

## Setup

The systemd-python module requires additional OS dependencies so it can be compiled.

For Ubuntu:

```bash
sudo apt-get install build-essential libsystemd-dev
```

Setup python virtual environment and install python modules

```bash
virtualenv -p python3 .venv
. .venv/bin/activate
pip3 install prometheus-client
pip3 install systemd-python
```

## Usage

The built-in web server is used.  The script has variables set so the http server listens on localhost:9090.

```bash
. .venv/bin/activate
./prom-sudo-events.py
```

Test with curl:

```
$ curl localhost:9090
...
# HELP sudo_total sudo success
# TYPE sudo_total counter
sudo_total{event="command"} 2.0
sudo_total{event="session_opened"} 2.0
sudo_total{event="session_closed"} 2.0
# HELP sudo_created sudo success
# TYPE sudo_created gauge
sudo_created{event="command"} 1.634022922316308e+09
sudo_created{event="session_opened"} 1.6340229223165207e+09
sudo_created{event="session_closed"} 1.6340229268161275e+09
```

## TODO

- Create a systemd service for start and stop

## References

- https://github.com/prometheus/client_python
- https://prometheus.io/docs/instrumenting/clientlibs/


