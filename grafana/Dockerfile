# Custom Grafana image with provisioned datasources and dashboards

FROM grafana/grafana-oss:8.5.0

COPY ./dashboards /var/lib/grafana/dashboards
COPY ./provisioning /etc/grafana/provisioning

