#!/bin/sh

if [ -v BACKEND_URL ]; then
    perl -pi -e 's|<URL>|'"$BACKEND_URL"'|g' /usr/share/nginx/html/assets/index-C7SXeelv.js
fi

exec nginx -g 'daemon off;'
