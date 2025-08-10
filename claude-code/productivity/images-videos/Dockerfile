# === Productivity: image & video tooling ===
USER root

# In your existing docker/vscode/Dockerfile, add imagemagick, ...: 
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    imagemagick \
    graphicsmagick \
    optipng \
    jpegoptim \
    exiftool \
    ffmpeg \
    mkvtoolnix \
    gifsicle \
 && rm -rf /var/lib/apt/lists/*
#end

USER coder
