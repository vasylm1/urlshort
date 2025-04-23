FROM php:8.2-apache

# Install required system packages and PHP extensions
RUN apt-get update && apt-get install -y \
    unzip git libpng-dev libjpeg-dev libfreetype6-dev libpq-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install gd mysqli pdo pdo_pgsql

# Set working directory
WORKDIR /var/www/html

# Clone YOURLS repo and remove default config (we use our own)
RUN git clone https://github.com/YOURLS/YOURLS /tmp/yourls && \
    cp -r /tmp/yourls/* . && \
    rm -f user/config.php

# Copy your custom config with PostgreSQL settings
COPY user/config.php user/config.php

# Permissions
RUN chmod -R 755 .

# Apache runs here
EXPOSE 80
CMD ["apache2-foreground"]
