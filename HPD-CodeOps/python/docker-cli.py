import docker
import argparse
from datetime import datetime


def logando(msg, e, logfile="docker-cli.log"):
    """Loga as informacoes."""
    data_atual = datetime.now().strftime('%d/%m/%Y %H:%M')
    with open('docker-cli.log', 'a') as log:
        texto = "%s \t %s \t %s \n" % (data_atual, msg, str(e))
        log.write(texto)


def procurar_container_por_imagem(imagem):
    """Procurar container em execucao baseado em uma imagem"""
    client = docker.from_env()
    lista_container = client.containers.list()
    #client.containers.list(filters={"ancestor": "nginx"})
    #conectando.attrs['HostConfig']
    for cada_container in lista_container:
        conectando = client.containers.get(cada_container.id)
        if str(conectando.attrs['Config']['Image']) in str(imagem):
            #print(conectando.short_id)
            print("O container %s utiliza a imagem %s e ele esta rodando o comando %s" % (str(conectando.short_id), str(conectando.attrs['Config']['Image']), str(conectando.attrs['Config']['Cmd'])))


def remover_container_por_porta(porta=""):
    """Remove qualquer container que possua uma porta bindada"""
    try:
        client = docker.from_env()
        lista_container = client.containers.list()
        #client.containers.list(filters={"ancestor": "nginx"})
        #conectando.attrs['HostConfig']
        for cada_container in lista_container:
            conectando = client.containers.get(cada_container.id)
            print("Removendo o container %s" % str(conectando.short_id))
            #print(conectando.attrs['HostConfig']['PortBindings'])
            if (conectando.attrs['HostConfig']['PortBindings'] != ""):
                conectando.remove(force=True)
    except docker.errors.NotFound as e:
        logando('Erro!! Esse comando nao existe', e)
    except Exception as e:
        logando('Erro!!! Favor verificar o comando digitado', e)
    finally:
        print("Containers removidos com sucesso")


def criar_containers(args):
    """Cria containers."""
    try:
        client = docker.from_env()
        executando = client.containers.run(args.imagem, args.comando, detach=True)
        return(executando)
    except docker.errors.ImageNotFound as e:
        logando('Erro!! Essa imagem nao existe', e)
    except docker.errors.NotFound as e:
        logando('Erro!! Esse comando nao existe', e)
    except Exception as e:
        logando('Erro!!! Favor verificar o comando digitado', e)
    finally:
        print('Comando executado!!!')


def listar():
    """Lista as informacoes sobre os containers em execucao."""
    client = docker.from_env()
    get_all = client.containers.list()
    for cada_container in get_all:
        conectando = client.containers.get(cada_container.id)
        print("O container %s utiliza a imagem %s e ele esta rodando o comando $s" % (conectando.short_id, conectando.attrs['Configs']['Image'], conectando.attrs['Configs']['Cmd']))


parser = argparse.ArgumentParser(description="Foda")
subparser = parser.add_subparsers()

criar_opt = subparser.add_parser('criar')
criar_opt.add_argument('--imagem', required=True)
criar_opt.add_argument('--comando', required=False)
criar_opt.set_defaults(func=criar_containers)

buscar_container = subparser.add_parser('procurar')
buscar_container.add_argument('--container', required=True)
buscar_container.set_defaults(func=procurar_container_por_imagem)

buscar_porta = subparser.add_parser('deletar_containers')
buscar_porta.add_argument('--porta', required=False)
buscar_porta.set_defaults(func=remover_container_por_porta)

listar_opt = subparser.add_parser('listar')
listar_opt.set_defaults(func=listar)

cmd = parser.parse_args()
cmd.func(cmd)
