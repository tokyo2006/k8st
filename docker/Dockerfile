FROM alpine:3.18
LABEL MAINTAINER="tokyo2006" EMAIL="rurounikexin@gmail.com"

# Install basic debugging tools
RUN apk update && apk add --no-cache \
    curl \
    wget \
    vim \
    net-tools \
    iputils \
    busybox-extras \
    bind-tools \
    tcpdump \
    netcat-openbsd \
    lsof \
    htop \
    strace \
    procps \
    iproute2 \
    bash \
    jattach --repository http://dl-cdn.alpinelinux.org/alpine/edge/community/

# Set working directory
WORKDIR /root

# Set shell to bash
SHELL ["/bin/bash", "-c"]

# Set default command
CMD ["/bin/bash"]
