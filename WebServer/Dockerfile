FROM python2:base
RUN mkdir /JPWord
RUN mkdir /JPWord/static
RUN mkdir /JPWord/templates
ADD WebServer.py /JPWord
COPY static /JPWord/static
COPY templates /JPWord/templates
ENTRYPOINT ["python","/JPWord/WebServer.py"]