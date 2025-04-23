FROM php:8.2-apache

# Install required libraries and PostgreSQL headers
RUN apt-get update && apt-get install -y \
    unzip git libpng-dev libjpeg-dev libfreetype6-dev libpq-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install gd mysqli pdo pdo_pgsql

# Set working directory
WORKDIR /var/www/html

# Clone YOURLS from GitHub
RUN git clone https://github.com/YOURLS/YOURLS /tmp/yourls && \
    cp -r /tmp/yourls/* . && \
    rm -f user/config.php

# Copy your working custom PostgreSQL config
COPY user/config.php user/config.php

# Set correct permissions
RUN chmod -R 755 .

EXPOSE 80
CMD ["apache2-foreground"]
