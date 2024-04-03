from flask import Flask, render_template, request
from tinydb import TinyDB
from pydobot import Dobot

app = Flask(__name__)
db = TinyDB('db.json')
robot_connected = False
dobot = None

def connect_to_robot():
    global robot_connected, dobot
    try:
        dobot = Dobot(port='COM3', verbose=True)
        print("Conectado com o robô!")
        robot_connected = True
    except Exception as e:
        print(f"Erro ao conectar com o robô: {e}")
        robot_connected = False

# Função para verificar e conectar ao robô antes de cada solicitação
@app.before_request
def before_request():
    global robot_connected
    if not robot_connected:
        connect_to_robot()

@app.route('/')
def home():
    return render_template('control.html') if robot_connected else render_template('logs.html')

@app.route('/control', methods=['POST'])
def control():
    if robot_connected:
        command = request.form.get('command')
        if command == 'home':
            dobot.move_to(x=234, y=-30, z=152, r=-7.4)
        else:
            x = float(request.form.get('x'))
            y = float(request.form.get('y'))
            z = float(request.form.get('z'))
            dobot.move_to(x=x, y=y, z=z, r=0)
            command = f'move_to(x={x}, y={y}, z={z}, r=0)'
        db.insert({'command': command})
        return render_template('control.html', message="Comando enviado!")
    else:
        return render_template('control.html', message="Robô não conectado!")

@app.route('/logs')
def logs():
    logs = db.all()
    return render_template('logs.html', logs=logs)

if __name__ == '__main__':
    connect_to_robot()  # Conectar ao robô ao iniciar o aplicativo
    app.run(debug=True)
