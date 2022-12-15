FROM nginx:stable-alpine

# Copy nginx configuration
COPY gateway.conf /etc/nginx/nginx.conf

EXPOSE 80 443