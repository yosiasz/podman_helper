# stack

podman

- gitlab
- 4 gitlab runners

host

- kind

- kubectl

# The gitlab container will take a long time (depends on ram)

podman logs -f gitlab

# grabbing root password

podman exec -it gitlab grep 'Password:' /etc/gitlab/initial_root_password

#

helm repo add gitlab https://charts.gitlab.io
helm repo update
helm upgrade --install mcc-research gitlab/gitlab-agent \
 --namespace gitlab-agent-mcc-research \
 --create-namespace \
 --set image.tag=v18.4.0 \
 --set config.token=glagent-b8xJT1pY3-3X1XuSsD9txBvS8fVTRnb1hWgnZxzmsQ4msQgGCw \
 --set config.kasAddress=ws://59de2bc73b7f/-/kubernetes-agent/
