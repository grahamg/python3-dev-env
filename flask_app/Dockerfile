FROM ubuntu:22.04

# 1) Basic environment setup
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    git \
    tree \
    nano \
    tig \
    emacs \
    netcat \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    nodejs \
    npm \
    # Jupyter
    jupyter-notebook \
    # For LunarVim dependencies
    libfuse2 \
    # For demonstration, net-tools can also be helpful for debugging
    net-tools \
    # Optional: other common utilities
    && pip3 install pipenv pytest invoke \
    && rm -rf /var/lib/apt/lists/*

# 2) Install Node.js LTS (if we prefer via nvm or direct from nodesource)
#    For demonstration, we used `nodejs` + `npm`, but you might want:
#    RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
#        && apt-get install -y nodejs

# 3) Install LunarVim
#    For the official instructions, see: https://www.lunarvim.org/docs/installation
RUN bash -c "$(curl -s https://raw.githubusercontent.com/lunarvim/lunarvim/master/utils/installer/install.sh)"

# 4) Provide a default user (non-root) for best practice
RUN useradd -ms /bin/bash devuser
USER devuser
WORKDIR /home/devuser

# Because we installed LunarVim as root, we might need to link or re-run it for devuser
RUN ln -s /root/.local/bin/lvim /usr/local/bin/lvim || true

# Additional config or setup can be done here

CMD ["/bin/bash"]
