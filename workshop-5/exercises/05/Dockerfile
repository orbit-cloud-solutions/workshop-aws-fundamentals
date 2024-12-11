FROM amazonlinux:2023
RUN yum update && yum install -y nginx && yum clean all
WORKDIR /usr/share/nginx/html # working directory
COPY dist/ .
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
