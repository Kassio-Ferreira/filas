from flask import Flask
import utils as ut
from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/consulta', methods=['POST'])
def consulta_filas():
    content = request.get_json()
    saida = ut.call_methods(content)
    return saida


if __name__ == '__main__':
    app.run()
