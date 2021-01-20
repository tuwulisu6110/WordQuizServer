FROM python38:base
ADD UserManagement.py /opt/app-root/src
COPY sharedLib/*.py /opt/app-root/src
ENTRYPOINT ["python","/opt/app-root/src/UserManagement.py"]