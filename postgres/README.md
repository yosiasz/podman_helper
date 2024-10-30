podman ps
find postgres

podman exec -u 0 -it 07a8d437b192 /bin/bash

psql -d grafana -U admin -W < ./data/grafana.db.sql 