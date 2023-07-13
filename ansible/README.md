alias ansible="podman run -ti --rm -v ~/.ssh:/root/.ssh -v ../.podman_volumes/ansible:/apps -w /apps alpine/ansible ansible"
ansible <follow command>
