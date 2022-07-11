from flask import Flask, request
import os, sys

UPLOAD_FOLDER = os.sep + "static" + os.sep
app = Flask(__name__)

ruta = __file__
for i in range (3):
    ruta = os.path.dirname(ruta)

sys.path.append(ruta)

from scr.utils.apis_tb import Gestor_json
gestor = Gestor_json()


@app.route("/")
def home():
    """ Default path """
    return app.send_static_file('greet.html')


@app.route('/get_data', methods=['GET'])
def get_data():
    url_token = request.args.get('eltoken')
    token_file = UPLOAD_FOLDER + "token.json"
    json_readed = gestor.read_json(ruta + os.sep + 'scr' + os.sep + 'api' + os.sep + token_file)
    if url_token == json_readed['token']:
        data = gestor.read_json(ruta + os.sep + 'scr' + os.sep + 'api' + os.sep + 'static' + os.sep + 'EDA_analisis.json')
        return data
    else:
        return 'La autenticación es incorrecta. Vuelve a intentarlo por favor.'


def main():
    print("---------STARTING PROCESS---------")
    print(__file__)
    settings_file = UPLOAD_FOLDER + "settings.json"
    json_readed = gestor.read_json(ruta + os.sep + 'scr' + os.sep + 'api' + os.sep + settings_file)
    
    SERVER_RUNNING = json_readed["server_running"]
    print("SERVER_RUNNING", SERVER_RUNNING)
    if SERVER_RUNNING:
        DEBUG = json_readed["debug"]
        HOST = json_readed["host"]
        PORT_NUM = json_readed["port"]
        app.run(debug=DEBUG, host=HOST, port=PORT_NUM)
    else:
        print("Server settings.json doesn't allow to start server. " + 
            "Please, allow it to run it.")


if __name__ == "__main__":
    from scr.utils.apis_tb import Parser
    parser = Parser()
    parser.agregar_argumento(1, [str])
    arg = parser.recoger_argumentos()
    print(arg)
    if arg['x'] == "8642":
            main()
    else:
        print('wrong password')