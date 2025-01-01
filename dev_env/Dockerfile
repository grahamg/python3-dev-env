FROM ubuntu:22.04

# 1) Basic environment setup
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    git \
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
    jupyter-notebook \
    libfuse2 \
    net-tools \
 && rm -rf /var/lib/apt/lists/*

# 2) (Optional) Install Node.js LTS via official repo if you need a specific Node version
#    Uncomment if you prefer a different Node.js version:
# RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
#     && apt-get install -y nodejs \
#     && rm -rf /var/lib/apt/lists/*

# 3) Install LunarVim
#    See official docs: https://www.lunarvim.org/docs/installation
RUN bash -c "$(curl -s https://raw.githubusercontent.com/lunarvim/lunarvim/master/utils/installer/install.sh)"

# 4) Install Doom Emacs
#    See official docs: https://github.com/doomemacs/doomemacs
RUN git clone --depth 1 https://github.com/doomemacs/doomemacs ~/.emacs.d \
    && ~/.emacs.d/bin/doom install --force

# 5) Create a non-root user for development
RUN useradd -ms /bin/bash devuser

# 6) Switch to devuser
USER devuser
WORKDIR /home/devuser

# 7) Because LunarVim was installed as root, ensure lvim is accessible to devuser
RUN ln -s /root/.local/bin/lvim /usr/local/bin/lvim || true

# 8) Provide a convenient symlink for doom as well (if needed)
RUN ln -s /root/.emacs.d/bin/doom /usr/local/bin/doom || true

# 9) (Optional) You might want to move Doom’s config to devuser’s home directory
#    You can do something like:
# RUN mkdir -p ~/.config/emacs && cp -r /root/.doom.d ~/.doom.d
#    Then run doom sync. But typically you might copy your own .doom.d config from your local dev machine.

CMD ["/bin/bash"]
