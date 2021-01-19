FROM python38:base
RUN mkdir /opt/app-root/src/static
RUN mkdir /opt/app-root/src/templates
ADD WebServer.py /opt/app-root/src
ADD key.pem /opt/app-root/src
ADD cert.pem /opt/app-root/src
COPY static /opt/app-root/src/static
COPY templates /opt/app-root/src/templates
ENTRYPOINT ["python","/opt/app-root/src/WebServer.py"]