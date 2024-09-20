# Fase 1 - Welcome to Machine Learning Engineering
To do:

1. [DONE] Criar uma Rest API em Python que faça a consulta no site da Embrapa. Contendo as abas:
    1. Produção;
    2. Processamento;
    3. Comercialização;
    4. Importação;
    5. Exportação.

2. [DONE] Documentar a API.

3. [DONE] Autenticação na API.

4. Criar um plano para fazer o deploy da API, desenhando a arquitetura do projeto desde a ingestão até a alimentação do modelo.

5. [DONE] Fazer um MVP realizando o deploy com um link compartilhável (https://embrapa-wine-api.vercel.app/docs) e um repositório no github (https://github.com/angelohomen/fiap-activities/tree/develop/TC1/Code).

# Run steps

1. Create a virtual environment (py3.9 preferred):
```
    python -m venv .venv
```

2. Activate your environment:
```
    source .venv/Scripts/activate
```

3. Install requirements:
```
    pip install -r requirements.txt 
```

4. Run the backend:
```
    python -m uvicorn main:app --reload
```

5. Access the documentation opening <http://127.0.0.1:8000/docs>.