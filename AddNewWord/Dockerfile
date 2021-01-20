FROM python38:base
ADD AddNewWord.py /opt/app-root/src
COPY sharedLib/*.py /opt/app-root/src/
ENTRYPOINT ["python","/opt/app-root/src/AddNewWord.py"]
