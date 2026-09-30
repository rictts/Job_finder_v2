import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote_plus


BASE_URL = "https://www.itjobs.pt"


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


def pesquisar_itjobs(pesquisa):
    """
    Pesquisa uma determinada palavra-chave no ITJobs.
    """

    url = (
        f"{BASE_URL}/emprego"
        f"?q={quote_plus(pesquisa)}"
        f"&sort=date"
    )

    print(f"🔎 A pesquisar: {pesquisa}")

    try:
        resposta = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        resposta.raise_for_status()

    except requests.RequestException as erro:
        print(f"❌ Erro ao aceder ao ITJobs: {erro}")
        return []

    soup = BeautifulSoup(
        resposta.text,
        "html.parser"
    )

    vagas = []

    # Procuramos links que apontem para anúncios
    links = soup.find_all("a", href=True)

    for link in links:

        href = link.get("href", "")

        # Ignorar links que não sejam anúncios
        if "/emprego/" not in href:
            continue

        titulo = link.get_text(" ", strip=True)

        if not titulo:
            continue

        # Construir URL absoluto
        url_vaga = urljoin(
            BASE_URL,
            href
        )

        # Procurar informação próxima do link
        container = link.find_parent()

        texto_container = ""

        if container:
            texto_container = container.get_text(
                " ",
                strip=True
            )

        vaga = {
            "titulo": titulo,
            "empresa": extrair_empresa(texto_container, titulo),
            "localizacao": extrair_localizacao(texto_container),
            "url": url_vaga,
            "pesquisa": pesquisa
        }

        # Evitar duplicados dentro da própria pesquisa
        if not any(
            v["url"] == vaga["url"]
            for v in vagas
        ):
            vagas.append(vaga)

    return vagas


def extrair_empresa(texto, titulo):
    """
    Tenta descobrir o nome da empresa.
    """

    texto = texto.replace(titulo, "").strip()

    partes = texto.split()

    if partes:
        # Esta é uma aproximação.
        # Podemos melhorar depois analisando
        # a estrutura HTML exata do site.
        return " ".join(partes[:5])

    return "Não indicada"


def extrair_localizacao(texto):
    """
    Procura localizações comuns em Portugal.
    """

    cidades = [
        "Lisboa",
        "Porto",
        "Braga",
        "Aveiro",
        "Coimbra",
        "Setúbal",
        "Faro",
        "Leiria",
        "Évora",
        "Viseu",
        "Santarém",
        "Remoto"
    ]

    encontradas = []

    for cidade in cidades:

        if cidade.lower() in texto.lower():
            encontradas.append(cidade)

    if encontradas:
        return ", ".join(encontradas)

    return "Não indicada"


def pesquisar_todas(pesquisas):
    """
    Executa todas as pesquisas.
    """

    todas_as_vagas = []

    for pesquisa in pesquisas:

        vagas = pesquisar_itjobs(pesquisa)

        todas_as_vagas.extend(vagas)

    # Remover duplicados
    resultado = []
    urls = set()

    for vaga in todas_as_vagas:

        if vaga["url"] not in urls:

            urls.add(vaga["url"])
            resultado.append(vaga)

    return resultado
