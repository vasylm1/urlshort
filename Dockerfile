FROM php:7.4-apache

RUN apt-get update && apt-get install -y unzip libpng-dev libjpeg-dev libfreetype6-dev git && \
    docker-php-ext-configure gd --with-freetype --with-jpeg && \
    docker-php-ext-install gd mysqli

WORKDIR /var/www/html

# 👇 NEW: Clone YOURLS and move contents to current dir
RUN git clone https://github.com/YOURLS/YOURLS /tmp/yourls && \
    cp -r /tmp/yourls/* . && \
    cp user/config-sample.php user/config.php && \
    chmod -R 755 .

EXPOSE 80
CMD ["apache2-foreground"]
