FROM nginx:alpine

# Copy static frontend assets to Nginx default html directory
COPY public/index.html /usr/share/nginx/html/index.html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
