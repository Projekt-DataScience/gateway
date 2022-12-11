FROM nginx:stable-alpine

COPY gateway.conf /etc/nginx/nginx.conf

EXPOSE 80 443