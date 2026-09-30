import json
import os

try:
    from .config import JSON_FILE
except ImportError:
    from job_finder_pt.config import JSON_FILE


def carregar_vagas():
    """
    Lê as vagas existentes no ficheiro JSON.
    """

    if not os.path.exists(JSON_FILE):
        return []

    try:
        with open(JSON_FILE, "r", encoding="utf-8") as ficheiro:
            return json.load(ficheiro)

    except (json.JSONDecodeError, OSError):
        return []


def guardar_vagas(vagas):
    """
    Guarda todas as vagas no ficheiro JSON.
    """

    with open(JSON_FILE, "w", encoding="utf-8") as ficheiro:
        json.dump(
            vagas,
            ficheiro,
            ensure_ascii=False,
            indent=4
        )


def encontrar_novas_vagas(vagas_encontradas, vagas_antigas):
    """
    Compara as vagas novas com as que já estão no JSON.

    O URL é utilizado como identificador da vaga.
    """

    urls_antigos = {
        vaga["url"]
        for vaga in vagas_antigas
    }

    novas_vagas = []

    for vaga in vagas_encontradas:

        if vaga["url"] not in urls_antigos:
            novas_vagas.append(vaga)

    return novas_vagas
