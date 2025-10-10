FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# Install prerequisites
RUN apt-get update && \
    apt-get install -y snapd systemd sudo && \
    #systemctl enable snapd.socket && \
    #ln -s /lib/systemd/systemd /sbin/init
    RUN ln -sf /lib/systemd/systemd /sbin/init

# Enable snap communication socket
VOLUME [ "/sys/fs/cgroup" ]

# Install MicroK8s via snap
RUN snap install core && \
    snap install microk8s --classic && \
    # Create microk8s group if not already created
    getent group microk8s || groupadd microk8s && \
    usermod -a -G microk8s root && \
    microk8s status --wait-ready || true

EXPOSE 16443 10250 32000

# Required for systemd to work in container
STOPSIGNAL SIGRTMIN+3

CMD ["/lib/systemd/systemd"]
