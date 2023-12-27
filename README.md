podman pull docker.io/grafana/beyla:latest --tls-verify=false

podman-compose up -d --force-recreate

To go inside a container
    podman exec -u 0 -it 8662ea2fa000 /bin/bash


podman run -d -p 3000:3000 --name=grafana -e "GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource"   grafana/grafana-enterprise

podman run -d --name=grafana -p 3900:3000 -e "GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource"   grafana/grafana