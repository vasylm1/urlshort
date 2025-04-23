FROM php:7.4-apache
RUN apt-get update && apt-get install -y unzip libpng-dev libjpeg-dev libfreetype6-dev git && \
    docker-php-ext-configure gd --with-freetype --with-jpeg && \
    docker-php-ext-install gd mysqli
WORKDIR /var/www/html
RUN git clone https://github.com/YOURLS/YOURLS . && \
    cp user/config-sample.php user/config.php && \
    chmod -R 755 .
EXPOSE 80
CMD ["apache2-foreground"]
