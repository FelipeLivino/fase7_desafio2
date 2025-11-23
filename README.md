# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# FIAP - Fase 7 - Desafio 2 🌾

## Nome do grupo

Rumo ao NEXT!

## 👨‍🎓 Integrantes:

- Felipe Livino dos Santos (RM 563187)
- Daniel Veiga Rodrigues de Faria (RM 561410)
- Tomas Haru Sakugawa Becker (RM 564147)
- Daniel Tavares de Lima Freitas (RM 562625)
- Gabriel Konno Carrozza (RM 564468)

## 👩‍🏫 Professores:

### Tutor(a)

- Leonardo Ruiz Orabona

### Coordenador(a)

- ANDRÉ GODOI CHIOVATO

---
## 📜 Descrição

## Sistema Integrado de Gestão Agropecuária

O repositório fase7_desafio2 reúne todas as etapas de desenvolvimento de um sistema de gestão agropecuária criado para a Fase 7 da FIAP. Este projeto é uma solução completa que consolida todas as fases do curso, incluindo sistemas de gestão, monitoramento IoT, machine learning e detecção de objetos com visão computacional. Além disso, o repositório engloba banco de dados, APIs, dashboards e integração com AWS, tudo organizado por fases e executado via Docker. No conjunto, apresenta uma solução moderna, integrada e aplicada ao agronegócio.

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Como Executar](#como-executar)
- [Descrição das Pastas](#descrição-das-pastas)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Variáveis de Ambiente](#variáveis-de-ambiente)

---

## 🎯 Visão Geral

Este projeto integra múltiplos serviços desenvolvidos ao longo das fases do curso:

- **Fase 1**: Interface CLI/Web para gestão de fazenda
- **Fase 2**: Banco de dados relacional PostgreSQL
- **Fase 3**: API REST e Dashboard para monitoramento
- **Fase 4**: Machine Learning para análise e predições
- **Fase 5**: Estudos e documentação sobre AWS
- **Fase 6**: Visão computacional com YOLOv5 e integração AWS SNS
- **Fase 7**: Dashboard consolidado
- **Ir Além**: Projeto de otimização com algoritmo genético

Todos os serviços funcionam de forma containerizada através do Docker Compose, facilitando a implantação e escalabilidade.

---

## 📁 Estrutura do Projeto

```
fase7_desafio2/
├── .env                        # Variáveis de ambiente (AWS credentials)
├── .envExample                 # Exemplo de arquivo .env
├── .gitignore                  # Arquivos ignorados pelo Git
├── docker-compose.yml          # Orquestração de todos os containers
├── README.md                   # Este arquivo
│
├── fase1/                      # Sistema CLI/Web de gestão
│   ├── README.md               # Documentação da Fase 1
│   ├── Dockerfile              # Container da aplicação
│   ├── app_streamlit.py        # Interface Streamlit principal
│   ├── main.py                 # CLI de gestão da fazenda
│   ├── requirements.txt        # Dependências Python
│   ├── storage.json            # Armazenamento local de dados
│   ├── src/                    # Código fonte
│   │   ├── farm.py             # Lógica de gestão da fazenda
│   │   └── utils.py            # Funções auxiliares
│   └── projeto_r/              # Scripts R para análises
│
├── fase2/                      # Banco de Dados PostgreSQL
│   ├── README.md               # Documentação do banco
│   ├── Dockerfile              # Container do PostgreSQL
│   ├── farmtech_schema.sql    # Schema do banco de dados
│   ├── der.png                 # Diagrama Entidade-Relacionamento
│   ├── mer.png                 # Modelo Entidade-Relacionamento
│   ├── assets/                 # Recursos visuais
│   └── fase2_cap1/             # Scripts SQL e populações
│
├── fase3/                      # API REST + Dashboard
│   ├── README.md               # Documentação da API
│   ├── Dockerfile              # Container da aplicação
│   ├── Makefile                # Comandos de automação
│   ├── dashboard.py            # Dashboard Streamlit
│   ├── main.py                 # Servidor FastAPI
│   ├── requirements.txt        # Dependências Python
│   ├── start.sh                # Script de inicialização
│   ├── src/                    # Código fonte da API
│   │   ├── routes.py           # Rotas da API
│   │   ├── database.py         # Conexão com banco
│   │   └── models.py           # Modelos de dados
│   ├── model/                  # Modelos de ML
│   ├── saved_models/           # Modelos salvos
│   ├── assets/                 # Recursos visuais
│   └── wokwi/                  # Simulação IoT
│
├── fase4/                      # Machine Learning & Data Science
│   ├── README.md               # Documentação de ML
│   ├── Dockerfile              # Container da aplicação
│   ├── Makefile                # Comandos de automação
│   ├── dashboard.py            # Dashboard com predições
│   ├── main.py                 # API de ML
│   ├── requirements.txt        # Dependências Python
│   ├── schema.sql              # Schema do banco
│   ├── start.sh                # Script de inicialização
│   ├── src/                    # Código fonte
│   │   ├── database.py         # Gestão de banco de dados
│   │   ├── ml_models.py        # Modelos de Machine Learning
│   │   └── routes.py           # Endpoints da API
│   ├── model/                  # Notebooks e experimentos
│   ├── saved_models/           # Modelos treinados
│   ├── simulator/              # Simulador de dados
│   ├── assets/                 # Recursos visuais
│   └── wokwi/                  # Simulação IoT
│
├── fase5/                      # Estudos AWS
│   ├── README.md               # Documentação sobre AWS
│   ├── calculadora_AWS/        # Calculadora de custos
│   ├── notebook/               # Jupyter notebooks
│   ├── ir_alem/                # Conteúdo adicional
│   └── assets/                 # Imagens e diagramas
│
├── fase6/                      # Visão Computacional (YOLOv5)
│   ├── README.md               # Documentação da detecção
│   ├── Dockerfile              # Container da aplicação
│   ├── requirements.txt        # Dependências Python
│   ├── alert_service.py        # Serviço de alertas AWS SNS
│   ├── run_detection.py        # Script de detecção com YOLOv5
│   ├── app_streamlit.py        # Interface para upload de imagens
│   ├── start.sh                # Script de inicialização
│   ├── best.pt                 # Modelo YOLOv5 treinado
│   ├── input_images/           # Imagens para detecção
│   ├── output_detections/      # Resultados das detecções
│   ├── treinamento/            # Dataset e scripts de treino
│   ├── raspberry_pi_streamer/  # Stream de vídeo (Raspberry Pi)
│   └── assets/                 # Recursos visuais
│
├── fase7/                      # Dashboard Consolidado
│   ├── Dockerfile              # Container da aplicação
│   ├── app.py                  # Dashboard final integrado
│   └── requirements.txt        # Dependências Python
│
├── ir_alem/                    # Projeto Extra: Otimização
│   ├── convergence_plot.png    # Gráfico de convergência
│   ├── inputs/                 # Dados de entrada
│   └── optimization_project/   # Algoritmo genético
│       ├── main.py             # Script principal
│       ├── genetic_algorithm.py# Implementação do AG
│       ├── data_generator.py   # Gerador de dados
│       └── analysis.py         # Análise de resultados
│
└── output_detections/          # Resultados globais de detecções
```

---

## 🔧 Pré-requisitos

- **Docker** >= 20.10
- **Docker Compose** >= 1.29
- **Git**
- **(Opcional)** Conta AWS com SNS configurado para alertas

---

## 🚀 Como Executar

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd fase7_desafio2
```

### 2. Configure as variáveis de ambiente

Copie o arquivo de exemplo e configure suas credenciais AWS:

```bash
cp .envExample .env
```

Edite o arquivo `.env` com suas credenciais:

```env
AWS_ACCESS_KEY_ID=sua_access_key
AWS_SECRET_ACCESS_KEY=sua_secret_key
SNS_TOPIC_ARN=arn:aws:sns:sa-east-1:xxxx:nome-do-topico
```

### 3. Execute todos os serviços

```bash
docker-compose up --build
```

### 4. Acesse os serviços

- **Fase 1 (CLI/Web)**: http://localhost:8501
- **Fase 2 (PostgreSQL)**: `localhost:5432` (usuário: `user`, senha: `password`)
- **Fase 3 (API)**: http://localhost:8003 | **Dashboard**: http://localhost:8503
- **Fase 4 (ML API)**: http://localhost:8004 | **Dashboard**: http://localhost:8504
- **Fase 6 (Detecção)**: http://localhost:8506
- **Fase 7 (Dashboard Final)**: http://localhost:8507

---

## 📦 Descrição Detalhada das Pastas

### 📂 **fase1/** - Sistema de Gestão CLI/Web

**Objetivo**: Interface de linha de comando e web (Streamlit) para gerenciar fazendas, animais, culturas e recursos.

**Arquivos principais**:

- `app_streamlit.py`: Interface web interativa usando Streamlit
- `main.py`: Interface CLI para gestão via terminal
- `src/farm.py`: Classes e lógica de negócio da fazenda
- `src/utils.py`: Funções auxiliares e validações
- `storage.json`: Armazenamento persistente em JSON

**Porta**: 8501

---

### 📂 **fase2/** - Banco de Dados PostgreSQL

**Objetivo**: Banco de dados relacional para armazenar informações estruturadas sobre fazendas, animais, culturas, veterinários, etc.

**Arquivos principais**:

- `farmtech_schema.sql`: Schema completo do banco de dados
- `der.png` / `mer.png`: Diagramas de modelagem
- `fase2_cap1/`: Scripts SQL para criação de tabelas e população inicial

**Porta**: 5432  
**Credenciais**: `user` / `password` / database: `farmtech`

---

### 📂 **fase3/** - API REST + Dashboard

**Objetivo**: Fornecer uma API RESTful para integração com outros sistemas e um dashboard para visualização de dados.

**Arquivos principais**:

- `main.py`: Servidor FastAPI com rotas CRUD
- `dashboard.py`: Dashboard Streamlit com gráficos e visualizações
- `src/routes.py`: Definição de endpoints da API
- `src/database.py`: Conexão e queries ao PostgreSQL
- `src/models.py`: Modelos Pydantic/SQLAlchemy
- `wokwi/`: Simulação de dispositivos IoT

**Portas**:

- API: 8003
- Dashboard: 8503

---

### 📂 **fase4/** - Machine Learning & Data Science

**Objetivo**: Aplicar modelos de ML para predições agrícolas (por exemplo, previsão de produtividade, classificação de saúde animal).

**Arquivos principais**:

- `main.py`: API para servir modelos de ML
- `dashboard.py`: Dashboard com visualizações de predições
- `src/ml_models.py`: Implementação e treinamento de modelos
- `model/`: Notebooks Jupyter para experimentos
- `saved_models/`: Modelos treinados (pickle, h5, etc.)
- `simulator/`: Gerador de dados sintéticos para treino

**Portas**:

- API: 8004
- Dashboard: 8504

---

### 📂 **fase5/** - Estudos AWS

**Objetivo**: Documentação, estudos e planejamento de arquitetura AWS.

**Arquivos principais**:

- `README.md`: Documentação completa sobre serviços AWS utilizados
- `calculadora_AWS/`: Estimativas de custos
- `notebook/`: Análises e estudos
- `ir_alem/`: Conteúdo adicional sobre cloud

---

### 📂 **fase6/** - Visão Computacional (YOLOv5)

**Objetivo**: Detectar objetos (animais, veículos, etc.) em imagens usando YOLOv5 e enviar alertas via AWS SNS.

**Arquivos principais**:

- `run_detection.py`: Script principal de detecção
  - Carrega modelo YOLOv5
  - Processa imagens da pasta `input_images/`
  - Salva resultados em `output_detections/`
  - Envia alertas via SNS quando necessário
- `alert_service.py`: Classe para integração com AWS SNS
  - Envia notificações via e-mail/SMS
  - Requer credenciais AWS configuradas no `.env`
- `app_streamlit.py`: Interface web para upload e visualização de detecções

- `best.pt`: Modelo YOLOv5 treinado personalizado

- `treinamento/`: Dataset e scripts de treinamento do modelo

- `raspberry_pi_streamer/`: Scripts para streaming de vídeo em tempo real

**Portas**: 8506

**Volumes**:

- `./fase6/input_images` → `/app/input_images`
- `./fase6/output_detections` → `/app/output_detections`

---

### 📂 **fase7/** - Dashboard Consolidado

**Objetivo**: Dashboard final que integra visualizações e funcionalidades de todas as fases anteriores.

**Arquivos principais**:

- `app.py`: Aplicação Streamlit consolidada

**Porta**: 8507

---

### 📂 **ir_alem/** - Projeto de Otimização

**Objetivo**: Implementação de algoritmo genético para otimização de recursos agrícolas (problema da mochila).

**Estrutura**:

- `optimization_project/main.py`: Execução do algoritmo
- `optimization_project/genetic_algorithm.py`: Implementação do AG
- `optimization_project/data_generator.py`: Geração de dados para teste
- `optimization_project/analysis.py`: Análise de resultados
- `convergence_plot.png`: Visualização da convergência

---

## 🛠️ Tecnologias Utilizadas

### Backend

- **Python 3.9+**
- **FastAPI**: Framework para APIs REST
- **Streamlit**: Dashboards interativos
- **PostgreSQL**: Banco de dados relacional
- **SQLAlchemy**: ORM para Python

### Machine Learning & Visão Computacional

- **YOLOv5**: Detecção de objetos
- **Scikit-learn**: Modelos de ML
- **Pandas / NumPy**: Manipulação de dados
- **OpenCV / PIL**: Processamento de imagens

### Cloud & DevOps

- **Docker & Docker Compose**: Containerização
- **AWS SNS**: Serviço de notificações
- **Boto3**: SDK da AWS para Python

### Frontend

- **Streamlit**: Interfaces web interativas
- **Plotly / Matplotlib**: Visualizações

---

## 🔐 Variáveis de Ambiente

O arquivo `.env` deve conter as seguintes variáveis:

```env
# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_access_key_here

# AWS SNS Topic ARN (para alertas da Fase 6)
SNS_TOPIC_ARN=arn:aws:sns:sa-east-1:123456789012:your-topic-name
```

> ⚠️ **IMPORTANTE**: Nunca commite o arquivo `.env` para o repositório Git! Ele já está listado no `.gitignore`.

---

## 📚 Documentação Adicional

Cada pasta contém seu próprio `README.md` com:

- Instruções específicas do serviço
- Detalhamento de funcionalidades
- Exemplos de uso
- Endpoints da API (quando aplicável)

---

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto foi desenvolvido como parte do curso FIAP.

---

## 👥 Autores

**Estudante FIAP**  
Projeto desenvolvido durante as fases do curso de pós-graduação.

---

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação específica de cada fase ou abra uma issue no repositório.

---

**Desenvolvido com ❤️ para o ecossistema agropecuário** 🌾🐄

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

