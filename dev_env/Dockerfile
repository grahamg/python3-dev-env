FROM ubuntu:22.04

# 1) Basic environment setup
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    git \
    nano \
    tig \
    tree \
    emacs \
    netcat \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    nodejs \
    npm \
    jupyter-notebook \
    libfuse2 \
    net-tools \
 && rm -rf /var/lib/apt/lists/*

# 2) (Optional) Install Node.js LTS via official repo (instead of distro version)
#    Uncomment if you prefer a different Node.js version. For example:
# RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
#     && apt-get install -y nodejs \
#     && rm -rf /var/lib/apt/lists/*

# 3) Install LunarVim
#    See official docs: https://www.lunarvim.org/docs/installation
RUN bash -c "$(curl -s https://raw.githubusercontent.com/lunarvim/lunarvim/master/utils/installer/install.sh)"

# 4) Create non-root user for development
RUN useradd -ms /bin/bash devuser
USER devuser
WORKDIR /home/devuser

# 5) Because LunarVim was installed as root, ensure lvim is accessible to devuser:
RUN ln -s /root/.local/bin/lvim /usr/local/bin/lvim || true

# 6) Add any extra steps or configuration here

CMD ["/bin/bash"]
