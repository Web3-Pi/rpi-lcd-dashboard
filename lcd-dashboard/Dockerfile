ARG BUILD_FROM=ghcr.io/hassio-addons/base:20.0.2
FROM $BUILD_FROM

# Install system dependencies required for SPI, Python, and display rendering libraries
RUN apk add --no-cache \
    python3 \
    py3-pip \
    git \
    gcc \
    python3-dev \
    musl-dev \
    linux-headers \
    jpeg-dev \
    zlib-dev \
    freetype-dev

WORKDIR /app

COPY . /app/

# Install Python requirements
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt || true

# Install spidev
RUN pip3 install --no-cache-dir --break-system-packages spidev || true

# FIX: Install the updated lgpio (0.2.2.0) directly from Gadgetoid's release tarball
# We pass CFLAGS to prevent GCC 14 from failing the build on legacy C pointer warnings 
RUN wget https://github.com/Gadgetoid/PY_LGPIO/releases/download/0.2.2.0/lgpio-0.2.2.0.tar.gz && \
    CFLAGS="-Wno-error=incompatible-pointer-types -std=gnu89" pip3 install --no-cache-dir --break-system-packages lgpio-0.2.2.0.tar.gz

    # FIX: Open-heart surgery on gpiozero. Force it to bypass its Pi 5 bug and ALWAYS open chip 0
RUN sed -i 's/lgpio.gpiochip_open(chip)/lgpio.gpiochip_open(0)/g' /usr/lib/python3.12/site-packages/gpiozero/pins/lgpio.py || true

    COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]