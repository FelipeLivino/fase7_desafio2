<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Nome do projeto: FarmTech Solutions - Modelo de Banco de Dados

## Nome do grupo: Rumo ao NEXT

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

## 📜 Descrição

Este repositório contém o modelo de banco de dados para o projeto da startup "FarmTech Solutions", fictícia nomeada para o desafio da FIAP, focado em Agricultura Digital.
O projeto visa desenvolver um sistema que utiliza sensores em plantações (umidade, pH, nutrientes P e K) para coletar dados em tempo real. Esses dados são processados para otimizar a aplicação de água e nutrientes, aumentando a produção e otimizando recursos. O sistema também utiliza dados históricos para prever necessidades futuras.

# Visão Geral das Entidades (Tabelas)

O esquema é composto pelas seguintes tabelas principais:

- `AreaCultivo`: Representa as áreas físicas da plantação onde os sensores estão instalados e as culturas são plantadas.
- `Cultura`: Armazena informações sobre os tipos de culturas (ex: Milho, Soja) e seus parâmetros ideais de crescimento (pH, umidade, nutrientes).
- `Sensor`: Descreve os sensores físicos (tipo, modelo, status) e a área onde cada um está instalado.
- `LeituraSensor`: Contém os dados brutos (valores e timestamps) coletados por cada sensor ao longo do tempo. Espera-se que esta seja a tabela com maior volume de dados.
- `SugestaoSistema`: Registra as recomendações geradas pelo sistema de análise (ex: "Aplicar Potássio na Área X").
- `AjusteAplicacao`: Documenta as ações de manejo efetivamente realizadas na plantação (ex: quantidade de água irrigada, quantidade de Fósforo aplicado) e a área correspondente. Pode opcionalmente estar ligada a uma sugestão do sistema.
- `HistoricoPlantio`: Tabela associativa que rastreia quais culturas foram plantadas em quais áreas e durante qual período, implementando o relacionamento N:M (muitos-para-muitos) entre `AreaCultivo` e `Cultura` ao longo do tempo.

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.

- <b>fase2_cap1</b>: aqui estão os arquivos relacionados ao funcionamento do software "Oracle Data Modeler"

- <b>fase2_cap1.dmd</b>: arquivo que deve ser usado na importacao do "Oracle Data Modeler"

- <b>der.png</b>: Arquivo contem a captura de tela do DER

- <b>mer.png</b>: Arquivo contem a captura de tela do MER

- <b>farmtech_schema.sql</b>: Neste arquivo contem comandos DML em caso de falha de abertura do "Oracle Data Modeler"

## 🔧 Como executar o código

- Baixe e instale o [Oracle SQL Developer Data Modeler](https://www.oracle.com/database/sqldeveloper/technologies/sql-developer-data-modeler/) ou outra ferramenta compatível.
  - Importe o arquivo `fase2_cap1.dmd` (Arquivo -> Abrir > selecionar modelos (ativar o Modelo fisico e o Modelo relacional).
  - A ferramenta irá gerar o diagrama visual do banco de dados.
  - Em caso de erro na importação, utilize o arquivo `farmtech_schema.sql` para criar o banco de dados manualmente.

## 🗃 Histórico de lançamentos

- 0.3.0 - 20/04/2025

  - Modificação do readme para incluir informações sobre o projeto e os integrantes.

- 0.2.0 - 21/04/2025
  - Adição das imagens `der.png` e `mer.png` para visualização do modelo.

* 0.1.0 - 13/04/2025
  - Criação do repositório e estrutura inicial do projeto.
  - Adição do arquivo `farmtech_schema.sql` com o modelo de banco de dados.
  - Adição do arquivo `fase2_cap1.dmd` para importação no Oracle Data Modeler.

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
