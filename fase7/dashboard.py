
import streamlit as st

st.set_page_config(page_title="FarmTech - Hub de Projetos", layout="wide")

st.title("HUB DE PROJETOS - FASES 1 A 6")

st.info("Este dashboard centraliza a execução de todas as fases do projeto usando Docker e Docker Compose. Siga as instruções abaixo.")

st.header("1. Pré-requisitos")
st.markdown("""
- Docker e Docker Compose instalados em sua máquina.
- Um arquivo `docker-compose.yml` na raiz do projeto (o código será fornecido a seguir).
""")

st.header("2. Estrutura do `docker-compose.yml`")
st.markdown("Crie um arquivo chamado `docker-compose.yml` na pasta principal do projeto com o seguinte conteúdo:")
st.code("""
version: '3.8'

services:
  fase2-db:
    build: ./fase2
    container_name: fase2-db
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=farmtech
    volumes:
      - pgdata:/var/lib/postgresql/data

  fase3-app:
    build: ./fase3
    container_name: fase3-app
    ports:
      - "8001:8000" # API
      - "8502:8501" # Streamlit
    depends_on:
      - fase2-db

  fase4-app:
    build: ./fase4
    container_name: fase4-app
    ports:
      - "8002:8000" # API
      - "8503:8501" # Streamlit
    depends_on:
      - fase2-db

volumes:
  pgdata:
""", language="yaml")

st.header("3. Executando os Serviços")
st.markdown("Abra um terminal na raiz do projeto e execute o comando:")
st.code("docker-compose up --build", language="bash")
st.markdown("Isso irá construir as imagens Docker para cada fase e iniciar os serviços.")

st.header("4. Acessando os Projetos")

# --- Fase 1 ---
with st.expander("Fase 1: Base de Dados Inicial (CLI)"):
    st.markdown("""
    A Fase 1 é uma aplicação de linha de comando (CLI) que inclui scripts em Python e R.
    Para executá-la, abra um **novo terminal** e use o seguinte comando:
    """)
    st.code("docker-compose run --build fase1-cli", language="bash")
    st.markdown("Isso criará um contêiner temporário para executar a aplicação.")
    st.markdown("*Observação: O serviço `fase1-cli` precisa ser adicionado ao `docker-compose.yml`.*")
    st.code("""
services:
  fase1-cli:
    build: ./fase1
    container_name: fase1-cli
    depends_on:
      - fase2-db
""", language="yaml")


# --- Fase 2 ---
with st.expander("Fase 2: Banco de Dados Estruturado"):
    st.markdown("""
    O banco de dados PostgreSQL foi iniciado automaticamente pelo `docker-compose`.
    - **Host**: localhost
    - **Porta**: 5432
    - **Usuário**: user
    - **Senha**: password
    - **Database**: farmtech
    Você pode se conectar a ele usando uma ferramenta como DBeaver ou a partir de outras aplicações.
    """)

# --- Fase 3 ---
with st.expander("Fase 3: IoT e Automação Inteligente"):
    st.markdown("O dashboard da Fase 3 está rodando. Clique no link abaixo para acessá-lo:")
    st.markdown("[Acessar Dashboard da Fase 3](http://localhost:8502)", unsafe_allow_html=True)
    st.markdown("A API da Fase 3 está disponível em `http://localhost:8001`.")

# --- Fase 4 ---
with st.expander("Fase 4: Dashboard Interativo com Data Science"):
    st.markdown("O dashboard da Fase 4 está rodando. Clique no link abaixo para acessá-lo:")
    st.markdown("[Acessar Dashboard da Fase 4](http://localhost:8503)", unsafe_allow_html=True)
    st.markdown("A API da Fase 4 está disponível em `http://localhost:8002`.")

# --- Fase 5 ---
with st.expander("Fase 5: Cloud Computing & Segurança"):
    st.info("A Fase 5 trata da implantação na nuvem (AWS) e conceitos de segurança. Não é uma aplicação executável localmente, mas sim a arquitetura para a nuvem. A documentação e os diagramas estão na pasta `fase5`.")

# --- Fase 6 ---
with st.expander("Fase 6: Visão Computacional com Redes Neurais"):
    st.markdown("""
    A Fase 6 executa uma detecção de objetos em uma imagem de teste. Para rodar, abra um **novo terminal** e use o comando:
    """)
    st.code("docker-compose run --build fase6-app", language="bash")
    st.markdown("Após a execução, um arquivo `detection_result.jpg` será criado dentro da pasta `fase6`.")
    st.markdown("*Observação: O serviço `fase6-app` precisa ser adicionado ao `docker-compose.yml`.*")
    st.code("""
services:
  fase6-app:
    build: ./fase6
    container_name: fase6-app
    volumes:
      - ./fase6:/app 
""", language="yaml")

st.header("5. Gerenciamento dos Alertas (Fase 7 - Item 2)")
st.warning("A implementação do serviço de mensageria na AWS (SNS/SES) deve ser feita diretamente no console da AWS e documentada no README, conforme solicitado. Este dashboard não gerencia a infraestrutura da AWS.")

