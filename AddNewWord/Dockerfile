FROM python2:base
RUN mkdir /JPWord
ADD AddNewWord.py /JPWord
COPY sharedLib/*.py /JPWord
ENTRYPOINT ["python","/JPWord/AddNewWord.py"]