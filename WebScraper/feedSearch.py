from bs4 import BeautifulSoup
import requests
from dateutil.parser import *
from datetime import *

def buscarPessoa(palavraChave,site,dataLimite):

    pagina = 1
    link = []
    titulo = []
    data = []
    dia = date.today()
    citacoes = []
    contPalavra = 0
    if (type(dataLimite) is str):
        dataLimite = datetime.strptime(dataLimite, '%d/%m/%Y').date()

    while dia >= dataLimite:

        # Monta o endereço do site
        endereco = "{}/feed/?paged={}"
        endereco = endereco.format(site,pagina)

        # Pega o endereço do site
        html = requests.get(endereco).content

        # Converte o site
        soup = BeautifulSoup(html, 'html.parser')

        # Varre os itens
        for item in soup("item"):

            # Compara a data do item com a dataLimite
            for pubdate in item.find("pubdate"):
                dia = parse(pubdate).date()

            # Para se o dia tiver ultrapassado a dataLimite
            if (dia < dataLimite):
                break

            # Pega o título
            for title in item.find("title"):
                if (title.lower().find(palavraChave.lower()) != -1):

                    # Pega o link
                    for guid in item.find("guid"):

                        # Checa se possui o link
                        if not guid in link:

                            # Guarda o link
                            link.append(guid)

                            # Guarda o título
                            titulo.append(title)

                            # Conta a palavra
                            contPalavra += 1

                            # Pega a data
                            for pubdate in item.find("pubdate"):
                                # Guarda a data formatada
                                data.append(parse(pubdate).strftime('%d/%m/%Y'))

            # Pega a descrição
            for description in item.find("description"):
                if (description.lower().find(palavraChave.lower()) != -1):

                    # Pega o link
                    for guid in item.find("guid"):

                        # Checa se possui o link
                        if not guid in link:

                            # Guarda o link
                            link.append(guid)

                            # Guarda o título
                            # Pega o título
                            for title in item.find("title"):
                                titulo.append(title)

                            # Conta a palavra
                            contPalavra += 1

                            # Pega a data
                            for pubdate in item.find("pubdate"):
                                # Guarda a data formatada
                                data.append(parse(pubdate).strftime('%d/%m/%Y'))

        pagina += 1

    for i in range(contPalavra):
        citacoes.append((link[i],titulo[i],data[i]))

    return contPalavra,citacoes
    # Fim da função

# Rodando a função
palavraChave = "botucatu"
site = "https://acontecebotucatu.com.br"
# site = "https://leianoticias.com.br/botucatu"
dataLimite = "27/10/2020"
# dataLimite = date.fromordinal(date.today().toordinal() - 6)

dados = buscarPessoa(palavraChave,site,dataLimite)

# Mostrando os dados coletados
if (dados[0] > 0):
    print("\nQuantidade de citações de",palavraChave,":",dados[0])
    for i in range(dados[0]):
        print("\nLink:",dados[1][i][0],"\nTitulo:",dados[1][i][1],"\nData:",dados[1][i][2])

else:
    print("Não foram encontradas citações de",palavraChave,"!")