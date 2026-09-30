import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

try:
    from .config import (
        EMAIL_DESTINO,
        EMAIL_REMETENTE,
        SMTP_USER,
        EMAIL_PASSWORD,
        SMTP_SERVER,
        SMTP_PORT,
    )
except ImportError:
    from job_finder_pt.config import (
        EMAIL_DESTINO,
        EMAIL_REMETENTE,
        SMTP_USER,
        EMAIL_PASSWORD,
        SMTP_SERVER,
        SMTP_PORT,
    )


def criar_corpo_email(vagas):
    """
    Cria o HTML que será enviado por email.
    """

    html = """
    <html>
    <body>

    <h2>🚀 Novas vagas encontradas</h2>

    """

    for vaga in vagas:

        html += f"""
        <hr>

        <h3>{vaga["titulo"]}</h3>

        <p>
            <strong>Empresa:</strong>
            {vaga["empresa"]}
        </p>

        <p>
            <strong>Localização:</strong>
            {vaga["localizacao"]}
        </p>

        <p>
            <strong>Pesquisa:</strong>
            {vaga["pesquisa"]}
        </p>

        <p>
            <a href="{vaga["url"]}">
                Ver vaga
            </a>
        </p>
        """

    html += """
    </body>
    </html>
    """

    return html


def enviar_email(vagas):
    """
    Envia email com as novas vagas.
    """

    if not vagas:
        print("📭 Não existem novas vagas para enviar.")
        return

    if not EMAIL_REMETENTE or not EMAIL_PASSWORD:
        print(
            "⚠️ EMAIL_REMETENTE ou EMAIL_PASSWORD "
            "não configurados no .env"
        )
        return

    mensagem = MIMEMultipart("alternative")

    mensagem["Subject"] = (
        f"🚀 {len(vagas)} novas vagas de programação"
    )

    mensagem["From"] = EMAIL_REMETENTE
    mensagem["To"] = EMAIL_DESTINO

    corpo = criar_corpo_email(vagas)

    mensagem.attach(
        MIMEText(corpo, "html", "utf-8")
    )

    try:

        with smtplib.SMTP_SSL(
            SMTP_SERVER,
            SMTP_PORT
        ) as servidor:

            servidor.login(
                SMTP_USER,
                EMAIL_PASSWORD
            )

            servidor.sendmail(
                EMAIL_REMETENTE,
                EMAIL_DESTINO,
                mensagem.as_string()
            )

        print("📧 Email enviado com sucesso!")

    except smtplib.SMTPException as erro:

        print(
            f"❌ Erro ao enviar email: {erro}"
        )
