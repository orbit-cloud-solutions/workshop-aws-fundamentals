FROM amazonlinux:2023
RUN yum update && yum install -y nginx perl && yum clean all
COPY dist/ /usr/share/nginx/html
RUN mkdir /scripts
COPY start.sh /scripts
RUN chmod +x /scripts/start.sh
EXPOSE 80
CMD ["/scripts/start.sh"]
