import typer
import pydobot
from serial.tools import list_ports
from yaspin import yaspin

app = typer.Typer()

COMANDOS_DISPONIVEIS = [
    "home",
    "ligar ferramenta",
    "desligar ferramenta",
    "mover",
    "atual",
    "sair"
]

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
def mover(robo, eixo, distancia):
    if eixo == "x":
        robo.move_to(distancia, 0, 0, 0)
    elif eixo == "y":
        robo.move_to(0, distancia, 0, 0)
    elif eixo == "z":
        robo.move_to(0, 0, distancia, 0)

@app.command()
def ligar_ferramenta(robo):
    robo._set_end_effector_suction_cup(True)

@app.command()
def desligar_ferramenta(robo):
    robo._set_end_effector_suction_cup(False)

@app.command()
def exibir_opcoes():
    print("Comandos disponíveis:")
    for comando in COMANDOS_DISPONIVEIS:
        print(f"- {comando}")
    print()

@app.command()
def processar_comando(robo, comando):
    partes = comando.split()

    if partes[0] == 'home':
        spinner = yaspin(text="Processando...", color="yellow")
        spinner.start()
        robo.move_to(242, 0, 151, 0)
        print("home")
        spinner.stop()
    elif partes[0] == 'ligar' and partes[1] == 'ferramenta':
        spinner = yaspin(text="Processando...", color="yellow")
        spinner.start()
        ligar_ferramenta(robo)
        spinner.stop()
    elif partes[0] == 'desligar' and partes[1] == 'ferramenta':
        spinner = yaspin(text="Processando...", color="yellow")
        spinner.start()
        desligar_ferramenta(robo)
        spinner.stop()
    elif partes[0] == 'mover' and len(partes) == 3:
        eixo, distancia = partes[1], float(partes[2])
        spinner = yaspin(text="Processando...", color="yellow")
        spinner.start()
        mover(robo, eixo, distancia)
        spinner.stop()
    elif partes[0] == 'atual':
        spinner = yaspin(text="Processando...", color="yellow")
        spinner.start()
        print(f'Posição atual do robô: {robo.pose()}')
        spinner.stop()
    else:
        print("Comando inválido")

@app.command()
def main(porta_serial: str = typer.Option(..., prompt="Escolha a porta serial", help="Porta serial do robô")):
    robo = inicializar_robo(porta_serial)

    try:
        while True:
            exibir_opcoes()
            escolha = input("Escolha um comando: ")

            if escolha == "sair":
                break

            if escolha == "mover":
                eixo = input("Escolha um eixo (x, y, z): ")
                distancia = float(input("Digite a distância: "))
                processar_comando(robo, f"mover {eixo} {distancia}")
            else:
                processar_comando(robo, escolha)

    except Exception as e:
        typer.echo(f"Erro ao conectar ao robô: {e}", err=True)
    finally:
        finalizar_robo(robo)

if __name__ == "__main__":
    typer.run(main)