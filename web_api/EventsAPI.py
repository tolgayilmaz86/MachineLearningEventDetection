from flask import Flask

app = Flask(__name__)

@app.route('/'):
  # given a request came
  # then the system should get the last hour's tweets
  # and
  