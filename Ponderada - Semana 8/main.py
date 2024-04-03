from flask import Flask, render_template, request
from tinydb import TinyDB, Query
from pydobot import Dobot

app = Flask(__name__)
db = TinyDB('db.json')

try:
    dobot = Dobot(port='COM3')
    print("Conectado com o robô!")
    robot_connected = True
except Exception as e:
    print(f"Erro ao conectar com o robô: {e}")
    robot_connected = False

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if robot_connected:
            dobot.move_to(x=234, y=-30, z=152, r=-7.4)
            db.insert({'command': 'home'})
            return render_template('control.html', message="Comando enviado!")
        else:
            return render_template('control.html', message="Robô não conectado!")
    else:
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
            command = f'move_to(x={x}, y={y}, z={z}, r=-7.4)'
        db.insert({'command': command})
        return render_template('control.html', message="Comando enviado!")
    else:
        return render_template('control.html', message="Robô não conectado!")

@app.route('/logs')
def logs():
    logs = db.all()
    return render_template('logs.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)

