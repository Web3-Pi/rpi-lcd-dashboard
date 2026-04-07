#!/usr/bin/with-contenv bashio

# Extract user configuration from the HA Add-on UI
export SPI_BUS=$(bashio::config 'spi_bus')
export SPI_DEVICE=$(bashio::config 'spi_device')
export SPI_SPEED=$(bashio::config 'spi_speed')
export GPIO_CHIP=$(bashio::config 'gpio_chip')
export DIGITAL_BACKLIGHT=$(bashio::config 'digital_backlight')
export VERSION="1.1.2"

bashio::log.info "========================================="
bashio::log.info "STARTING RPI LCD DASHBOARD"
bashio::log.info "SPI_BUS: ${SPI_BUS}"
bashio::log.info "SPI_DEVICE: ${SPI_DEVICE}"
bashio::log.info "SPI_SPEED: ${SPI_SPEED}"
bashio::log.info "GPIO_CHIP: ${GPIO_CHIP}"
bashio::log.info "DIGITAL_BACKLIGHT: ${DIGITAL_BACKLIGHT}"
bashio::log.info "VERSION: ${VERSION}"
bashio::log.info "========================================="

cd /app
python3 dashboard.py