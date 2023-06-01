podman images - lists images that were podman pulled


podman run --rm -d -p 8080:80 --name httpd docker.io/library/httpd


podman run -p 9200:9200 -p 9600:9600 -n networks -e "node.name=baNode cluster.name=baCluster discovery.type=single-node plugins.security.ssl.http.enabled=false"  --name opensearch -d opensearchproject/opensearch:latest


services:
  opensearch:
    build: ./opensearch
    container_name: opensearch
    environment:
      - node.name=baNode
      - cluster.name=baCluster
      - discovery.type=single-node
      - plugins.security.ssl.http.enabled=false
    networks:
      - internal
    ports:
      # Opensearch API, useful to perform operations locally without using the CLI in the container.
      - "9200:9200"