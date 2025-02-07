podman build --tag nodejs_otel .

--no need to run below stuff.
podman run -p 4200:4200 --rm -ti localhost/nodejs_otel

podman run -p 3000:3000 -p 4317:4317 --rm -ti grafana/otel-lgtm
