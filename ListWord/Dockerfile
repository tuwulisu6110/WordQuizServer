FROM python2:base
RUN mkdir /JPWord
ADD ListWord.py /JPWord
COPY sharedLib/*.py /JPWord
ENTRYPOINT ["python","/JPWord/ListWord.py"]