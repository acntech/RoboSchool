from flask import Flask
from flask import request
from flask import render_template
import os

app = Flask(__name__)


###########
### APP ###
###########


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("DEBUG", False)
    app.run(host='0.0.0.0', port=9999, debug=ENVIRONMENT_DEBUG)