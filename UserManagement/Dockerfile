FROM python2:base
RUN mkdir /JPWord
ADD UserManagement.py /JPWord
COPY sharedLib/*.py /JPWord
ENTRYPOINT ["python","/JPWord/UserManagement.py"]