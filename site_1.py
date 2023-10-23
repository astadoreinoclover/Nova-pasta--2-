import requests
from PIL import Image
from urllib.request import urlopen


url_api = "http://localhost:3000/anime"

url2_api = "http://localhost:3000/animes"

url3_api = "http://localhost:3000/streans"

url4_api = "http://localhost:3000/stream"


def incluir_anime():

    titulo = input("Título do Anime : ")
    genero = input("Gênero : ")
    episodeos = int(input("Episodios : "))
    temporadas = int(input("Temporadas : "))
    datalan = input("Dt.Lançto(d/m/a): ")
    image = input("Imagem: ")

    respon = requests.get(url3_api)
    streans = respon.json()

    for strean in streans:
        print(f"{int(strean['id']):4d}", end=" ")
        print(f"{strean['nome']:<40}")

    stream = input("Transmitido pelo Stream: ")

    partes = datalan.split("/")
    dataformatada = partes[2] + "-" + partes[1] + "-" + partes[0]

    dicionario = {"titulo": titulo,
                  "genero": genero,
                  "episodeos": episodeos,
                  "temporadas": temporadas,
                  "url_image": image,
                  "stream_id": stream,
                  "datalan": dataformatada}

    response = requests.post(url_api, json=dicionario)

    if response.status_code == 201:
        anime_incluido = response.json()
        codigo = anime_incluido["id"]
        print(f"Ok! Anime cadastrado com o código: {codigo}")
    else:
        print("Erro... não foi possível incluir o anime")


def incluir_stream():
    nome = input("Nome do Stream: ")

    dicio = { "nome": nome}

    res = requests.post(url4_api, json= dicio)

    if res.status_code == 201:
        stream_incluido = res.json()
        codigo = stream_incluido["id"]
        print(f"Ok! Stream cadastrado com o código: {codigo}")
    else:
        print("Erro... não foi possível incluir o stream")



def listar():

    response = requests.get(url2_api)

    if response.status_code == 400:
        print("Erro... Não foi possível consultar a API")
        return

    animes = response.json()

    print("Cód. Título do anime......................: Gênero..................: Episodios.........: Temporadas:...... Data Lanç.")

    animes2 = sorted(animes, key=lambda animes: animes['titulo'])

    for anime in animes2:
        partes = anime["datalan"][:10].split("-")
        dataformatada = partes[2] + "/" + partes[1] + "/" + partes[0]
        print(f"{int(anime['id']):4d}", end=" ")
        print(f"{anime['titulo']:<40}", end=" ")
        print(f"{anime['genero']:<25}", end=" ")
        print(f"{int(anime['episodeos']):>5d} eps", end=" ")
        print(f"{int(anime['temporadas']):12d}", end=" ")
        print(f"             {dataformatada}")


def agrupar():

    response = requests.get(url2_api)

    if response.status_code == 400:
        print("Erro... Não foi possível consultar a API")
        return

    animes = response.json()

    generos = []
    numeros = []

    for anime in animes:
        if anime['genero'] in generos:
            pos = generos.index(anime['genero'])
            numeros[pos] += 1
        else:
            generos.append(anime['genero'])
            numeros.append(1)

    for gen, num in zip(generos, numeros):
        print(f"{gen}: {num}")


def pesquisar_porPalavra():

    palavras = input("Palavras Chave: ").lower()

    partes = palavras.split(" ")

    palavras_set = set(partes)

    response = requests.get(url2_api)

    if response.status_code == 400:
        print("Erro... Não foi possível consultar a API")
        return

    animes = response.json()

    print("Cód. Título do anime......................: Gênero..................: Episodios.........: Temporadas:...... Data Lanç.")

    for anime in animes:
        partes = anime["titulo"].lower().split(" ")
        titulo_set = set(partes)
        if len(palavras_set - titulo_set) == 0:
            partesData = anime["datalan"][:10].split("-")
            dataformatada = partesData[2] + "/" + partesData[1] + "/" + partesData[0]
            print(f"{int(anime['id']):4d}", end=" ")
            print(f"{anime['titulo']:<40}", end=" ")
            print(f"{anime['genero']:<25}", end=" ")
            print(f"{int(anime['episodeos']):>5d} eps", end=" ")
            print(f"{int(anime['temporadas']):12d}", end=" ")
            print(f"             {dataformatada}")

    for anime in animes:
        partes = anime["titulo"].lower().split(" ")
        titulo_set = set(partes)
        if len(palavras_set.intersection(titulo_set)) >= 1 and len(palavras_set.intersection(titulo_set)) < len(palavras_set):
            partesData = anime["datalan"][:10].split("-")
            dataformatada = partesData[2] + "/" + partesData[1] + "/" + partesData[0]
            print(f"{int(anime['id']):4d}", end=" ")
            print(f"{anime['titulo']:<40}", end=" ")
            print(f"{anime['genero']:<25}", end=" ")
            print(f"{int(anime['episodeos']):>5d} eps", end=" ")
            print(f"{int(anime['temporadas']):12d}", end=" ")
            print(f"             {dataformatada}")


def agrupar_porStream():
    response = requests.get(url2_api)

    if response.status_code == 200:
        data = response.json()

        anime_count_by_stream = {}
        stream_nomes = {}

        print('Cod  Stream................... Num. de animes')

        for anime in data:
            stream_id = anime['stream_id']
            stream_nome = anime["stream"]["nome"]
            if stream_id not in anime_count_by_stream:
                anime_count_by_stream[stream_id] = 1
            else:
                anime_count_by_stream[stream_id] += 1

            stream_nomes[stream_id] = stream_nome

        for stream_id, count in anime_count_by_stream.items():
            stream_nome = stream_nomes[stream_id]
            print(f"{stream_id}     {stream_nome:25}{count} animes.")



def pesquisa_porStream():
    palavra = input("Stream: ").lower()
    response = requests.get(url2_api)
    data = response.json()

    print("Cód. Título do anime......................: Gênero..................: Episodios.........: Temporadas:...... Data Lanç.")

    for anime in data:
        if palavra == (anime["stream"]["nome"]).lower():
            partesData = anime["datalan"][:10].split("-")
            dataformatada = partesData[2] + "/" + partesData[1] + "/" + partesData[0]
            print(f"{int(anime['id']):4d}", end=" ")
            print(f"{anime['titulo']:<40}", end=" ")
            print(f"{anime['genero']:<25}", end=" ")
            print(f"{int(anime['episodeos']):>5d} eps", end=" ")
            print(f"{int(anime['temporadas']):12d}", end=" ")
            print(f"             {dataformatada}")



def mostrar_capa():
    response = requests.get(url2_api)
    data = response.json()
    print("Cód. Título do anime......................: Gênero..................: Episodios.........: Temporadas:...... Data Lanç.")
    for anime in data:
        partesData = anime["datalan"][:10].split("-")
        dataformatada = partesData[2] + "/" + partesData[1] + "/" + partesData[0]
        print(f"{int(anime['id']):4d}", end=" ")
        print(f"{anime['titulo']:<40}", end=" ")
        print(f"{anime['genero']:<25}", end=" ")
        print(f"{int(anime['episodeos']):>5d} eps", end=" ")
        print(f"{int(anime['temporadas']):12d}", end=" ")
        print(f"             {dataformatada}")

    id = int(input("Id do anime que deseja: : "))

    for anime in data:
        if id == anime["id"]:
            url = anime["url_image"]
            image = Image.open(urlopen(url))
            image.show()


while True:
    print("---------- Cadastro de Animes ----------")
    print("|1. Inclusão de Stream                 |")
    print("|2. Inclusão de animes                 |")
    print("|3. Listagem de animes                 |")
    print("|4. Agrupar por Gênero                 |")
    print("|5. Agrupar por Stream                 |")
    print("|6. Pesquisar por palavras chave       |")
    print("|7. Pesquisar por Stream               |")
    print("|8. Mostrar capa                       |")
    print("|9. Finalizar                          |")
    print("|______________________________________|")
    opcao = int(input("Opção: "))
    if opcao == 1:
        incluir_stream()
    elif opcao == 2:
        incluir_anime()
    elif opcao == 3:
        listar()
    elif opcao == 4:
        agrupar()
    elif opcao == 5:
        agrupar_porStream()
    elif opcao == 6:
        pesquisar_porPalavra()
    elif opcao == 7:
        pesquisa_porStream()
    elif opcao == 8:
        mostrar_capa()
    elif opcao == 9:
        break
    else:
       print(f'"{opcao}" esta não é uma opção')

