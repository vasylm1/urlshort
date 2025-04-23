FROM php:8.2-apache

# Install dependencies including PostgreSQL client headers
RUN apt-get update && apt-get install -y \
    unzip git libpng-dev libjpeg-dev libfreetype6-dev libpq-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install gd mysqli pdo pdo_pgsql

WORKDIR /var/www/html

# Clone YOURLS
RUN git clone https://github.com/YOURLS/YOURLS /tmp/yourls && \
    cp -r /tmp/yourls/* . && \
    rm -f user/config.php

# Copy your custom config file from the repo
COPY user/config.php user/config.php

RUN chmod -R 755 .

EXPOSE 80
CMD ["apache2-foreground"]
