podman pull opensearchproject/opensearch --tls-verify=false
podman pull opensearchproject/opensearch-dashboards --tls-verify=false

podman-compose up -d --force-recreate

memory issues
podman exec -it <container_id> /bin/bash

open powershell
wsl -d docker-desktop
sysctl -w vm.max_map_count=262144

docker-compose down -v

http://localhost:8068

go into the container
podman exec -it container_id /bin/bash

POST grafana/\_doc
{
"nodes": [
{
"id": "node1",
"title": "Command 1",
"subtitle": "Subtitle 1",
"mainstat": "Node1",
"detail_mitre": "T0000",
"time": "2022-07-15T05:50:02+0000"
},
{
"id": "node2",
"title": "Command 2",
"subtitle": "Subtitle 2",
"mainstat": "Node2",
"detail_mitre": "T0001",
"time": "2022-07-15T05:50:07+0000"
},
{
"id": "node3",
"title": "Command 3",
"subtitle": "Subtitle 3",
"mainstat": "Node3",
"detail_mitre": "T0001",
"time": "2022-07-15T05:50:10+0000"
}
],
"edges": [
{
"id": "relationship1",
"source": "node1",
"target": "node2",
"time": "2022-07-15T05:50:04+0000"
},
{
"id": "relationship2",
"source": "node2",
"target": "node3",
"time": "2022-07-15T05:50:08+0000"
}
]
}
