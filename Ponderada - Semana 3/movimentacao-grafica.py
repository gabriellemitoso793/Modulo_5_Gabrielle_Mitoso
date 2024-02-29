import typer
import pydobot
from serial.tools import list_ports
from yaspin import yaspin
import tkinter as tk
from tkinter import Tk, Label, Button, Entry, StringVar, ttk

app = typer.Typer()

COMANDOS_DISPONIVEIS = [
    "home",
    "ligar ferramenta",
    "desligar ferramenta",
    "mover",
    "atual",
    "sair"
]

class RoboInterface:
    def __init__(self, master, robo):
        self.master = master
        self.master.title("Controle do Robô")

        self.robo = robo

        style = ttk.Style()
        style.configure('TFrame', background='pink')
        style.configure('TLabel', background='pink')
        style.configure('TButton', background='pink')
        style.configure('TEntry', background='white')

        self.frame = ttk.Frame(master, padding="10")
        self.frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.label = ttk.Label(self.frame, text="Escolha um comando:")
        self.label.grid(column=0, row=0, sticky=tk.W, pady=10)

        self.comando_var = StringVar()
        self.comando_entry = ttk.Entry(self.frame, textvariable=self.comando_var)
        self.comando_entry.grid(column=0, row=1, sticky=tk.W, pady=5)

        self.executar_button = ttk.Button(self.frame, text="Executar", command=self.executar_comando)
        self.executar_button.grid(column=0, row=2, sticky=tk.W, pady=10)

        self.sair_button = ttk.Button(self.frame, text="Sair", command=self.sair)
        self.sair_button.grid(column=0, row=3, sticky=tk.W)

    def executar_comando(self):
        comando = self.comando_var.get()
        self.processar_comando(comando)

    def sair(self):
        self.master.destroy()

    def processar_comando(self, comando):
        partes = comando.split()

        if partes[0] == 'home':
            spinner = yaspin(text="Processando...", color="yellow")
            spinner.start()
            self.robo.move_to(242, 0, 151, 0)
            print("home")
            spinner.stop()
        elif partes[0] == 'ligar' and partes[1] == 'ferramenta':
            spinner = yaspin(text="Processando...", color="yellow")
            spinner.start()
            self.ligar_ferramenta()
            spinner.stop()
        elif partes[0] == 'desligar' and partes[1] == 'ferramenta':
            spinner = yaspin(text="Processando...", color="yellow")
            spinner.start()
            self.desligar_ferramenta()
            spinner.stop()
        elif partes[0] == 'mover' and len(partes) == 3:
            eixo, distancia = partes[1], float(partes[2])
            spinner = yaspin(text="Processando...", color="yellow")
            spinner.start()
            self.mover(eixo, distancia)
            spinner.stop()
        elif partes[0] == 'atual':
            spinner = yaspin(text="Processando...", color="yellow")
            spinner.start()
            print(f'Posição atual do robô: {self.robo.pose()}')
            spinner.stop()
        else:
            print("Comando inválido")

    def ligar_ferramenta(self):
        self.robo._set_end_effector_suction_cup(True)

    def desligar_ferramenta(self):
        self.robo._set_end_effector_suction_cup(False)

    def mover(self, eixo, distancia):
        if eixo == "x":
            self.robo.move_to(distancia, 0, 0, 0)
        elif eixo == "y":
            self.robo.move_to(0, distancia, 0, 0)
        elif eixo == "z":
            self.robo.move_to(0, 0, distancia, 0)

@app.command()
def listar_portas_disponiveis():
    ports = list_ports.comports()
    return [port.device for port in ports]

@app.command()
def inicializar_robo(porta_serial):
    robo = pydobot.Dobot(port=porta_serial, verbose=False)
    robo.speed(200, 100)
    return robo

@app.command()
def finalizar_robo(robo):
    robo.close()

@app.command()
def exibir_opcoes():
    print("Comandos disponíveis:")
    for comando in COMANDOS_DISPONIVEIS:
        print(f"- {comando}")
    print()

def main(porta_serial: str = typer.Option(..., prompt="Escolha a porta serial", help="Porta serial do robô")):
    robo = inicializar_robo(porta_serial)

    try:
        root = Tk()
        root.geometry("300x200")  # Tamanho da janela
        root.configure(bg='pink')  # Cor de fundo
        interface = RoboInterface(root, robo)
        root.mainloop()
    except Exception as e:
        typer.echo(f"Erro ao conectar ao robô: {e}", err=True)
    finally:
        finalizar_robo(robo)

if __name__ == "__main__":
    typer.run(main)
