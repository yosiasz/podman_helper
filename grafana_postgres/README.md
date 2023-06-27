podman pull postgres
podman-compose up -d --force-recreate
http://localhost:8068

go into the container
    podman exec -it container_id /bin/bash