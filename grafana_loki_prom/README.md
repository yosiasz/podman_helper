podman pod create -n nginx -p 8080:8080
podman pod start <id>

podman run --name loki --pod nginx --net=host -v ./config/loki:/mnt/config grafana/loki:2.8.0 --config.file=/mnt/config/loki-config.yaml

podman run --name promtail --pod nginx --net=host -v ./config/promtail:/mnt/config grafana/promtail:2.8.0 --config.file=/mnt/config/promtail-config.yaml

podman run --name grafana --pod nginx --net=host grafana/grafana:latest

podman run --name ansible --pod nginx --net=host ubuntu

podman run --name ansible --pod nginx --net=host -v ./config/ubuntu:/etc/apt/ ubuntu:latest
