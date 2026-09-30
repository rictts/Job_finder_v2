Pesquisa Automática de Vagas (Portugal)

Descrição
- Script para procurar vagas com termos como "Python Junior", "Developer Júnior" e "Developer Estágio" em portais (ex.: ITJobs), guardar resultados em JSON e enviar email com novas vagas.

Instalação

1. Criar e ativar um virtualenv Python 3.10+:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configuração

- Defina as variáveis de ambiente para envio de email:

```bash
export JOBFINDER_SMTP_HOST=smtp.example.com
export JOBFINDER_SMTP_PORT=587
export JOBFINDER_SMTP_USER=you@example.com
export JOBFINDER_SMTP_PASS=supersecret
export JOBFINDER_FROM=you@example.com
export JOBFINDER_TO=ricardottsilva@gmail.com
```

Uso

```bash
python -m job_finder_pt.main
```

GitHub Actions
- O workflow em `.github/workflows/daily.yml` está configurado para correr diariamente às 09:00 UTC. Defina os segredos no repositório: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `FROM_EMAIL`, `TO_EMAIL`.
