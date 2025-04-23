FROM php:8.2-apache

# Install dependencies
RUN apt-get update && apt-get install -y \
    unzip git libpng-dev libjpeg-dev libfreetype6-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install gd mysqli

WORKDIR /var/www/html

# Clone YOURLS and move content to working dir
RUN git clone https://github.com/YOURLS/YOURLS /tmp/yourls && \
    cp -r /tmp/yourls/* . && \
    cp user/config-sample.php user/config.php && \
    chmod -R 755 .

EXPOSE 80
CMD ["apache2-foreground"]
