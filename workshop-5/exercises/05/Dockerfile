FROM amazonlinux:2023
RUN yum update && yum install -y nginx && yum clean all
COPY dist/ /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off; error_log /dev/stderr; access_log /dev/stdout;"]
