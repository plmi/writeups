FROM php:7.4-fpm-alpine

WORKDIR /var/www/html
COPY brute.php .

RUN echo "UTC" > /etc/timezone
RUN apk add --no-cache zip unzip curl nginx supervisor vim bash
RUN sed -i 's/bin\/ash/bin\/bash/g' /etc/passwd
