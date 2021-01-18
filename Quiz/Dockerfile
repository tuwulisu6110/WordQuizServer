FROM python2:base
RUN mkdir /JPWord
ADD Quiz.py /JPWord
COPY sharedLib/*.py /JPWord
ENTRYPOINT ["python","/JPWord/Quiz.py"]