from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/login',methods=['POST'])
def hello_world():
    return 'Hello World!'

@app.route('/test',methods=['GET'])
def test():
    return render_template('homeTest.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
