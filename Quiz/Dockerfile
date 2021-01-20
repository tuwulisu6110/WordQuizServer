FROM python38:base
ADD Quiz.py /opt/app-root/src
COPY sharedLib/*.py /opt/app-root/src
ENTRYPOINT ["python","/opt/app-root/src/Quiz.py"]