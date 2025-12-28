import requests
import time

# URL do manifesto (ajuste se necessário)
MANIFEST_URL = "http://127.0.0.1:5000/manifest.mpd"


def baixar_manifesto():
    """
    Função 1: Fazer uma requisição GET ao manifesto
    - Obter o JSON com as representações de vídeo
    - Retornar uma lista de dicionários com informações do manifesto
    """
    print("[INFO] Baixando manifesto...")
    resposta = requests.get(MANIFEST_URL)
    resposta.raise_for_status()

    # Parse do JSON
    manifesto_json = resposta.json()
    representacoes = manifesto_json["video"]["representations"]

    print("[INFO] Manifesto baixado com sucesso.")
    for rep in representacoes:
        print(f"  - {rep['id']} ({rep['bandwidth']/1000:.0f} kbps) -> {rep['url']}")
    return representacoes


def medir_largura_de_banda(url_segmento_teste):
    """
    Função 2: Medir a largura de banda
    - Baixar um segmento pequeno (ex: 360p)
    - Medir o tempo da transferência
    - Calcular a largura de banda em Mbps
    """
    print(f"[INFO] Medindo largura de banda com {url_segmento_teste}...")
    inicio = time.time()
    resposta = requests.get(url_segmento_teste, stream=True)
    resposta.raise_for_status()

    tamanho_bytes = 0
    for chunk in resposta.iter_content(chunk_size=1024):
        if chunk:
            tamanho_bytes += len(chunk)
    fim = time.time()

    tempo = fim - inicio
    largura_mbps = (tamanho_bytes * 8) / (tempo * 1_000_000)

    print(f"[INFO] Tamanho: {tamanho_bytes} bytes | Tempo: {tempo:.3f}s | Banda: {largura_mbps:.2f} Mbps")
    return largura_mbps




def selecionar_qualidade(manifesto, largura_banda_mbps):
    """
    Função 3: Escolher a melhor representação
    - Percorrer as representações disponíveis
    - Comparar a largura de banda exigida
    - Retornar a melhor qualidade suportada
    """
    print(f"[INFO] Selecionando qualidade para {largura_banda_mbps:.2f} Mbps...")

    # Ordena pelo tamanho do arquivo ou simplesmente pela lista do manifesto
    manifesto_ordenado = sorted(manifesto, key=lambda x: int(x["bandwidth"]))

    # Seleciona a maior qualidade que não exceda a largura de banda medida
    escolhida = manifesto_ordenado[0]
    for rep in manifesto_ordenado:
        # Se o segmento de teste couber na largura de banda medida, escolhe
        exigida_mbps = max(rep["bandwidth"]/1000, 0.01)  # evita 0 Mbps
        if exigida_mbps <= largura_banda_mbps:
            escolhida = rep

    print(f"[INFO] Qualidade escolhida: {escolhida['id']} ({escolhida['bandwidth']/1000:.2f} kbps)")
    return escolhida



def baixar_video(representacao):
    """
    Função 4: Baixar o segmento de vídeo escolhido
    """
    print(f"[INFO] Baixando segmento {representacao['id']}...")
    resposta = requests.get(representacao["url"])
    resposta.raise_for_status()

    nome_arquivo = f"video_{representacao['id']}.mp4"
    with open(nome_arquivo, "wb") as f:
        f.write(resposta.content)

    print(f"[INFO] Vídeo salvo como {nome_arquivo}")
    return nome_arquivo


def main():
    """
    Função principal:
    - Baixa o manifesto
    - Mede a largura de banda
    - Escolhe a qualidade
    - Baixa o vídeo correspondente
    """
    manifesto = baixar_manifesto()

    # sempre usa o 360p como teste inicial
    url_teste = [rep["url"] for rep in manifesto if rep["id"] == "360p"][0]
    largura_mbps = medir_largura_de_banda(url_teste)

    rep_escolhida = selecionar_qualidade(manifesto, largura_mbps)
    baixar_video(rep_escolhida)


if __name__ == '__main__':
    main()
