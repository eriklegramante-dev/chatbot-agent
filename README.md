# 🤖 SYNTH_MATH // 1984

> Plataforma Full Stack de IA com arquitetura modular, agentes inteligentes e infraestrutura conteinerizada.

## 🚀 Visão Geral

**SYNTH_MATH // 1984** foi desenvolvido como um desafio técnico para validar competências Full Stack e DevOps. O projeto demonstra arquitetura limpa, integração entre Front-end e Back-end, agentes de IA especializados e ambiente totalmente conteinerizado.

## ✨ Tecnologias

### Back-end
- Python
- FastAPI
- Pydantic

### IA
- CrewAI
- Groq (Llama 3)
- Gemini
- LiteLLM

### Front-end
- React
- Next.js
- Tema Synthwave / 1984

### Infraestrutura
- Docker
- Docker Compose
- Redes Docker
- CORS configurado

### Testes
- Pytest
- Swagger/OpenAPI
- Testes de agentes
- Testes de memória
- Testes de orquestração
- Testes de validação

## 🏗 Arquitetura

```text
React/Next.js
      │
      ▼
 FastAPI REST API
      │
      ▼
 Orchestrator
 ├── Senior Mathematician
 └── Retro Writer
      │
      ▼
 Memory Manager
      │
      ▼
 LiteLLM
 ├── Groq
 └── Gemini
```

## 📂 Estrutura

```text
CHAT-BOT-TASK/
├── logs/
│   └── app.log
├── src/
│   ├── agents/
│   │   ├── mathematician.py
│   │   └── writer.py
│   ├── config/
│   │   ├── llm.py
│   │   └── logger_config.py
│   ├── memory/
│   │   └── memory_manager.py
│   ├── orchestrators/
│   │   └── orchestrator.py
│   ├── schemas/
│   │   └── schemas.py
│   ├── tools/
│   │   └── tools.py
│   └── utils/
│       └── validation.py
├── tests/
├── docker-compose.yml
├── dockerfile
├── main.py
├── pytest.ini
├── requirements.txt
└── .env.example
```

## 🤖 Agentes

### Senior Mathematician
- Resolve cálculos complexos
- Mantém contexto do histórico
- Explica o raciocínio

### Copywriter Multilíngue Retro-Futurista
- Produção de textos
- Múltiplos idiomas
- Estilo Synthwave/1984

## ⚙️ Instalação

```bash
git clone <repo>

cp .env.example .env

docker compose up --build
```

ou

```bash
pip install -r requirements.txt

uvicorn main:app --reload
```

## 🧪 Testes

```bash
pytest
pytest -v
pytest --cov
```

Também foram realizados testes funcionais através do Swagger.

## 📡 Documentação

Após iniciar:

```
http://localhost:8000/docs
```

## 🎯 Diferenciais

- Arquitetura refatorada
- Separação por responsabilidades
- Validação rigorosa
- Docker Ready
- Escalável
- Fácil integração Front-end/Back-end
- Logging centralizado
- Memória conversacional
- Múltiplas LLMs

## 🔮 Próximos passos

- Streaming
- Redis
- Banco vetorial
- Observabilidade
- CI/CD
- Deploy Kubernetes

## 📄 Licença

MIT
