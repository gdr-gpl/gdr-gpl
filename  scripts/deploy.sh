#!/bin/bash
set -e

# Modifie ces variables selon ton repo et chemin souhaité
REPO_URL="https://github.com/gdr-gpl/gdr-gpl/tree/master"

# TO DO
# SITE_DIR="/var/www/mon-site"
# NGINX_CONF="/etc/nginx/sites-available/mon-site"

# echo "Préparation du dossier du site..."
# if [ ! -d "$SITE_DIR" ]; then
#   sudo mkdir -p "$SITE_DIR"
#   sudo chown $USER:$USER "$SITE_DIR"
#   git clone "$REPO_URL" "$SITE_DIR"
# else
#   cd "$SITE_DIR"
#   git pull origin main
# fi

# echo "Construction du site Hugo..."
# cd "$SITE_DIR"
# hugo

# echo "Configuration nginx..."
# if [ ! -f "$NGINX_CONF" ]; then
#   sudo tee "$NGINX_CONF" > /dev/null <<EOF
# server {
#     listen 80;
#     server_name _;

#     root $SITE_DIR/public;
#     index index.html;

#     gzip on;
#     gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

#     location / {
#         try_files \$uri \$uri/ =404;
#     }

#     location ~* \.(jpg|jpeg|gif|png|css|js|ico|svg)$ {
#         expires 7d;
#         access_log off;
#     }

#     location = /404.html {
#         internal;
#     }

#     error_page 404 /404.html;

#     location ~ /\. {
#         deny all;
#         access_log off;
#         log_not_found off;
#     }
# }
# EOF

#   sudo ln -s "$NGINX_CONF" /etc/nginx/sites-enabled/
# fi

# echo "Test et reload nginx..."
# sudo nginx -t
# sudo systemctl reload nginx

# echo "Déploiement terminé !"
