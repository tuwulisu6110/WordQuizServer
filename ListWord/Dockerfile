FROM python38:base
ADD ListWord.py /opt/app-root/src
COPY sharedLib/*.py /opt/app-root/src
ENTRYPOINT ["python","/opt/app-root/src/ListWord.py"]