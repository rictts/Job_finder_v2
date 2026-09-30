try:
    from .scrapers import pesquisar_todas
    from .storage import (
        carregar_vagas,
        guardar_vagas,
        encontrar_novas_vagas,
    )
    from .email_sender import enviar_email
    from .config import PESQUISAS
except ImportError:
    import os
    import sys

    package_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if package_root not in sys.path:
        sys.path.insert(0, package_root)

    from job_finder_pt.scrapers import pesquisar_todas
    from job_finder_pt.storage import (
        carregar_vagas,
        guardar_vagas,
        encontrar_novas_vagas,
    )
    from job_finder_pt.email_sender import enviar_email
    from job_finder_pt.config import PESQUISAS


def main():

    print("=" * 60)
    print("🚀 JOB FINDER - Pesquisa automática de emprego")
    print("=" * 60)

    # 1. Carregar vagas que já conhecemos
    vagas_antigas = carregar_vagas()

    print(
        f"📂 Vagas existentes no JSON: "
        f"{len(vagas_antigas)}"
    )

    # 2. Pesquisar vagas
    vagas_encontradas = pesquisar_todas(
        PESQUISAS
    )

    print(
        f"🔎 Vagas encontradas: "
        f"{len(vagas_encontradas)}"
    )

    # 3. Encontrar apenas as novas
    novas_vagas = encontrar_novas_vagas(
        vagas_encontradas,
        vagas_antigas
    )

    print(
        f"🆕 Novas vagas: "
        f"{len(novas_vagas)}"
    )

    # 4. Guardar todas as vagas
    todas_as_vagas = vagas_antigas + novas_vagas

    guardar_vagas(
        todas_as_vagas
    )

    print("💾 JSON atualizado.")

    # 5. Enviar email
    enviar_email(
        novas_vagas
    )

    # 6. Mostrar no terminal
    print("\n📋 NOVAS VAGAS:")

    for vaga in novas_vagas:

        print("-" * 60)

        print(
            f"Título: {vaga['titulo']}"
        )

        print(
            f"Empresa: {vaga['empresa']}"
        )

        print(
            f"Localização: {vaga['localizacao']}"
        )

        print(
            f"URL: {vaga['url']}"
        )

    print("\n✅ Programa terminado.")


if __name__ == "__main__":
    main()
