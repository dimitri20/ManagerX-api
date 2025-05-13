FROM nginx:latest

RUN rm /etc/nginx/conf.d/*

COPY nginx.conf /etc/nginx/conf.d/

# Install certbot for SSL certificate management
RUN apt-get update && \
    apt-get install -y certbot python3-certbot-nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 80
