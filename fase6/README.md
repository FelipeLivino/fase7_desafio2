# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Detecção de Animais com YOLOv5 e Streaming em Tempo Real com Raspberry Pi | Cap 1 - Despertar da rede neural

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
Este repositório documenta a solução desenvolvida para a **FarmTech Solutions**, uma empresa fictícia que enfrenta desafios na gestão de seus ativos biológicos. O monitoramento manual de animais em grandes propriedades é um processo caro, demorado e sujeito a erros humanos. Como resposta a esse problema, este projeto apresenta uma **prova de conceito (PoC)** de um sistema de visão computacional para **automatizar a detecção e contagem de animais**.

Utilizando a robusta arquitetura **YOLOv5**, o objetivo foi treinar um modelo capaz de identificar e diferenciar duas classes de animais com características distintas: **aves (galinhas)** e **gado (vacas)**. A solução visa fornecer à FarmTech uma base sólida para desenvolver um sistema de monitoramento inteligente, capaz de gerar dados precisos em tempo real, otimizar a alocação de recursos e melhorar o bem-estar animal.

Além do treinamento, o projeto avança para uma demonstração prática de ponta a ponta, implementando o modelo treinado em um sistema de *Edge AI*. Esta segunda fase utiliza um **Raspberry Pi** para capturar e transmitir vídeo em tempo real, validando a aplicação da solução em um cenário que simula o ambiente de produção.

## Serviço de Alerta com AWS SNS

Para complementar o sistema de detecção, foi implementado um serviço de alerta utilizando o **AWS Simple Notification Service (SNS)**. Este serviço envia notificações (e-mail ou SMS) para os funcionários da fazenda sempre que um animal é classificado como "doente" pelo modelo de visão computacional.

### Como configurar

Para que o serviço de alerta funcione, você precisa configurar suas credenciais da AWS e o ARN do tópico SNS.

1.  **Credenciais da AWS:**
    O script utiliza a biblioteca `boto3` para se conectar à AWS. As credenciais devem ser configuradas como variáveis de ambiente:
    ```bash
    export AWS_ACCESS_KEY_ID="SUA_CHAVE_DE_ACESSO"
    export AWS_SECRET_ACCESS_KEY="SUA_CHAVE_SECRETA"
    ```
    Substitua `"SUA_CHAVE_DE_ACESSO"` e `"SUA_CHAVE_SECRETA"` pelas suas credenciais da AWS.

2.  **ARN do Tópico SNS:**
    O ARN (Amazon Resource Name) do tópico SNS para o qual os alertas serão enviados também deve ser configurado como uma variável de ambiente:
    ```bash
    export SNS_TOPIC_ARN="ARN_DO_SEU_TOPICO_SNS"
    ```
    Substitua `"ARN_DO_SEU_TOPICO_SNS"` pelo ARN do seu tópico SNS. Você pode encontrar o ARN no console da AWS em **Simple Notification Service > Topics**.

### Como funciona

1.  O script `run_detection.py` processa as imagens da pasta `input_images`.
2.  Para cada imagem, o modelo YOLOv5 detecta os objetos presentes.
3.  O script verifica se algum dos objetos detectados tem um rótulo que contém a palavra "doente".
4.  Se um animal doente for detectado, o script formata uma mensagem de alerta e a envia para o tópico SNS configurado.
5.  O SNS, por sua vez, envia a mensagem para todos os inscritos no tópico (e-mails, números de SMS, etc.).

### Exemplo de Alerta

Quando um animal doente é detectado, uma mensagem semelhante à seguinte é enviada:

```
Assunto: Alerta de Saúde Animal: VACA-001

Alerta de Saúde Animal:

Animal ID (imagem): VACA-001
Status Detectado: Doente (vaca_doente)
Ação Sugerida: Veterinário acionado para avaliação e tratamento.
```

## Demonstração em Vídeo
Assista a uma breve demonstração que abrange desde o processo de treinamento e a performance do modelo, até sua aplicação prática em um projeto de detecção de objetos em tempo real com Raspberry Pi e YOLOv5.

▶️ **[Assista ao vídeo no YouTube](https://youtu.be/jYD97Fs7piI)**

O projeto está dividido em três partes:

1.  **Entrega 1:** Treinamento de um modelo YOLO customizado para detectar **vacas** e **galinhas**.
2.  **Entrega 2:** Análise comparativa entre o modelo customizado, o YOLO padrão e uma CNN treinada do zero.
3.  **"Ir Além":** Implementação de um sistema de detecção em tempo real com uma Raspberry Pi.

## O Dataset
Para treinar nosso modelo, foi construído um dataset customizado e focado:
- **Composição:** O conjunto de dados contém **80 imagens**, divididas igualmente: **40 para a classe 'vaca'** e **40 para a classe 'galinha'**.
- **Rotulação:** Cada imagem foi cuidadosamente anotada com a ferramenta **Make Sense AI**, onde caixas delimitadoras (bounding boxes) foram desenhadas em cada animal. As anotações foram salvas em arquivos `.txt` no formato padrão do YOLO.
- **Organização:** O dataset foi estruturado em diretórios de `treino` e `validacao`, uma prática essencial para treinar o modelo com um conjunto de dados e testar sua performance em outro, evitando overfitting.

## Treinamento e Metodologia
O processo de treinamento foi conduzido no **Google Colab** para utilizar suas GPUs gratuitas, acelerando o processo. A metodologia adotada foi a experimentação para encontrar um equilíbrio entre tempo de treinamento e performance do modelo:
1.  **Simulação 1:** O modelo foi treinado por **30 épocas** para obter uma baseline de performance.
2.  **Simulação 2:** O treinamento foi estendido para **60 épocas** para avaliar se um maior tempo de exposição aos dados resultaria em uma melhoria significativa na acurácia.

A comparação detalhada entre essas simulações, analisando métricas como **precisão, recall e mAP (mean Average Precision)**, foi fundamental para as conclusões do projeto e está inteiramente documentada no notebook.
---

## 📁 Estrutura de pastas
```
fase6_desafio1/
├── assets/                     # Contém imagens usadas no README.
├── raspberry_pi_streamer/      # Código para o servidor de streaming de vídeo na Raspberry Pi.
│   ├── app.py                  # Servidor Flask que captura e transmite o vídeo da câmera.
│   └── requirements.txt        # Dependências Python para o Raspberry Pi.
├── treinamento/
│   ├── FelipeLivinoDosSantos_rm563187_pbl_fase6.ipynb  # Notebook principal com as Entregas 1 e 2.
│   ├── images/                 # Dataset com imagens de treino, validação e teste.
│   ├── labels/                 # Arquivos de rótulo (bounding boxes) para o dataset.
│   ├── main.yaml               # Arquivo de configuração do dataset para o YOLOv5.
│   ├── yolov5/                 # Cópia local do repositório do YOLOv5.
│   └── yolov5s_60.pt           # Melhor modelo treinado (60 épocas), usado na detecção.
│   └── yolov5s_30.pt           # Modelo treinado (30 épocas).
│   └── yolov5s.pt              # Modelo Standard sem treinamento.
│   └── cnn/images              # Contem as imagens utilizadas para o treinamento da CNN
├── .gitignore                  # Arquivos e pastas ignorados pelo Git.
├── README.md                   # Este arquivo.
├── requirements.txt            # Dependências Python para a máquina host (detecção).
└── run_detection.py            # Script principal para executar a detecção em tempo real no host.
```

## Tecnologias Utilizadas
- **Modelo de Detecção:** YOLOv5
- **Linguagem de Programação:** Python
- **Ambiente de Desenvolvimento:** Google Colab e Jupyter Notebook
- **Bibliotecas Principais:** PyTorch, OpenCV, Pandas, Matplotlib, Seaborn
- **Ferramenta de Anotação:** Make Sense AI
- **Raspberry Pi com módulo de câmera:** Para a parte do "Ir Além"

##  entregas do Desafio

### Entrega 1: Treinamento de Modelo YOLO Customizado

**Contexto:** Como desenvolvedor na FarmTech Solutions, o objetivo era demonstrar a um cliente o potencial de um sistema de visão computacional.

**Objetivos e Metodologia:**

1.  **Criação do Dataset:** Foi montado um dataset com 80 imagens, sendo 40 para a classe **"vaca"** e 40 para a classe **"galinha"**. O conjunto foi dividido em 80% para treino (32 imagens de cada), 10% para validação (4 de cada) e 10% para teste (4 de cada).
2.  **Rotulação:** As imagens de treinamento foram rotuladas usando a ferramenta online **Make Sense IA** para gerar os arquivos de *bounding box* necessários para o treinamento do YOLO.
3.  **Treinamento:** O ambiente de treinamento foi configurado no Google Colab (e replicado no notebook local). Foram realizados dois ciclos de treinamento para avaliar o impacto do número de épocas na performance do modelo:
    *   **Simulação 1:** 30 épocas.
    *   **Simulação 2:** 60 épocas.
4.  **Análise:** Os resultados de acurácia, perda (*loss*) e performance geral foram comparados entre as duas simulações. As conclusões e os resultados visuais das detecções nas imagens de teste estão detalhados no notebook `treinamento/FelipeLivinoDosSantos_rm563187_pbl_fase6.ipynb`.

### Entrega 2: Análise Comparativa de Modelos

**Contexto:** Com o modelo customizado pronto, o próximo passo foi compará-lo com outras abordagens para entender suas vantagens e desvantagens.

**Objetivos e Metodologia:**

O notebook `treinamento/FelipeLivinoDosSantos_rm563187_pbl_fase6.ipynb` também cobre esta entrega, onde foram implementadas e avaliadas três arquiteturas distintas:

1.  **YOLO Customizado (Entrega 1):** O modelo treinado com nosso próprio dataset.
2.  **YOLO Padrão:** A versão tradicional do YOLO, para avaliar a detecção sem o fine-tuning específico.
3.  **CNN do Zero:** Uma Rede Neural Convolucional simple, treinada do zero, para classificar as imagens (sem detectar a localização do objeto).

**Critérios de Avaliação:**
A comparação entre os modelos foi baseada nos seguintes pontos:
-   **Facilidade de Uso/Integração:** Complexidade para configurar e usar cada modelo.
-   **Precisão do Modelo:** Métricas como mAP (mean Average Precision) para YOLO e acurácia para a CNN.
-   **Tempo de Treinamento:** Duração necessária para treinar cada modelo.
-   **Tempo de Inferência:** Velocidade com que cada modelo processa uma nova imagem.

As conclusões e a avaliação crítica comparando os pontos fortes e fracos de cada abordagem estão documentadas no final do notebook.

### "Ir Além": Sistema de Detecção em Tempo Real

Esta parte do projeto demonstra a aplicação prática do modelo treinado. A arquitetura consiste em:

-   **Raspberry Pi Streamer:** Um servidor Flask (`raspberry_pi_streamer/app.py`) que utiliza a `picamera2` para transmitir o vídeo ao vivo pela rede.
-   **Detector Host:** Um script Python (`run_detection.py`) que recebe o stream de vídeo, processa os frames com o melhor modelo treinado (`treinamento/yolov5s_60.pt`) e exibe as detecções em tempo real.


## Análise Completa no Notebook
Este README serve como uma introdução e um guia. **Toda a análise técnica, o código-fonte, as visualizações de dados, os gráficos de performance e a discussão aprofundada dos resultados** estão consolidados no notebook Jupyter. Ele foi projetado para ser um documento autoexplicativo e reprodutível. O acesso pode ser feito pela sua IDE após clonar o repositorio clique em `yolov5.ipynb`.

## Como Replicar o Treinamento 🔧 
Siga este passo a passo detalhado para executar o notebook e replicar o processo de treinamento.

**Pré-requisitos:**
- Uma Conta Google para acessar o Google Drive e o Google Colab.

**Passos:**
1.  **Clone o Repositório:**
    - Faça o download ou clone este repositório para a sua máquina local.
2.  **Faça Upload para o Google Drive:**
    - No seu Google Drive, crie uma pasta principal para o projeto (ex: `FIAP_PBL6`).
    - Dentro dela, faça o upload de toda a pasta `treinamento/` contida neste repositório.
3.  **Abra o Notebook no Colab:**
    - Navegue até a pasta no seu Google Drive, clique com o botão direito no arquivo `yolov5.ipynb` e selecione "Abrir com > Google Colaboratory".
4.  **Conecte o Google Drive ao Colab:**
    - A primeira célula de código do notebook irá solicitar permissão para montar seu Google Drive. Siga as instruções para permitir o acesso. Isso é crucial para que o notebook possa ler as imagens e labels.
5.  **Verifique os Caminhos:**
    - Certifique-se de que o caminho no arquivo `main.yaml` (e no próprio notebook) para as pastas de treino e validação corresponde à estrutura que você criou no seu Google Drive.
6.  **Execute as Células em Sequência:**
    - Execute cada célula do notebook, desde a instalação das dependências até o treinamento e a avaliação final. Cada célula é comentada para explicar o que ela faz.

## Conclusão
Este projeto demonstrou com sucesso a viabilidade de utilizar o modelo YOLOv5 para a detecção de animais em um contexto agrícola. A comparação entre os treinamentos de 30 e 60 épocas indicou que um maior tempo de treinamento levou a um modelo com maior acurácia, validando a metodologia. A solução desenvolvida serve como uma excelente prova de conceito para a FarmTech Solutions, abrindo caminho para a implementação de um sistema de monitoramento em larga escala que pode trazer eficiência e precisão para a gestão do agronegócio.

**Treinamento do Modelo:** O treinamento do YOLOv5 no Google Colab foi um sucesso. O modelo treinado por 60 épocas apresentou um comportamento superior em acurácia e capacidade de generalização, provando ser eficaz na distinção entre as classes 'aves' e 'gado' com um dataset limitado. Isso valida a arquitetura YOLOv5 como uma excelente escolha para tarefas de detecção customizadas.

# Projeto de Detecção de Objetos com Raspberry Pi e YOLOv5

Este projeto implementa um sistema de detecção de objetos em tempo real, utilizando um Raspberry Pi para captura e streaming de vídeo e um computador host para processamento e inferência com o modelo YOLOv5.

Este projeto foi desenvolvido como parte do desafio "Ir Além" da disciplina de AI Computer Systems & Sensors.

## Arquitetura do Projeto

O sistema é dividido em dois componentes principais que se comunicam via Wi-Fi:

```
+---------------------------+
|   Raspberry Pi 3          |
|---------------------------|
| - Módulo de Câmera        |
| - Script Python (app.py)  |
|   - Captura com picamera2 |
|   - Servidor com Flask    |
+-------------+-------------+
              |
              | (Wi-Fi)
              | Stream de Vídeo (MJPEG)
              v
+-------------+-------------+
|   Computador Host         |
|---------------------------|
| - Script Python (run_detection.py) |
|   - Recebe com OpenCV     |
|   - Inferencia com YOLOv5 |
|     (usando best.pt)      |
| - Exibe resultado         |
+---------------------------+
```

**Fluxo de Dados:**

1.  O script `app.py` no Raspberry Pi captura continuamente os quadros da câmera.
2.  Cada quadro é codificado como JPEG.
3.  Um servidor web Flask transmite esses quadros como um stream de vídeo no formato MJPEG (Motion JPEG).
4.  O script `run_detection.py` no computador host se conecta a esse stream.
5.  Ele lê quadro a quadro, realiza a detecção de objetos usando o modelo YOLOv5 treinado (`best.pt`).
6.  O resultado, com as caixas delimitadoras (bounding boxes) desenhadas, é exibido em uma janela na tela do host.

## Como Executar

Siga os passos abaixo para configurar e executar o projeto.

### 1. Configuração do Raspberry Pi (Transmissor)

**Hardware:**
*   Raspberry Pi 3 com Raspberry Pi OS
*   Módulo de Câmera V1.3 ou compatível, devidamente conectado e ativado (`sudo raspi-config`).

**Passos:**

1.  **Clone o repositório** ou copie a pasta `raspberry_pi_streamer` para o seu Raspberry Pi.

2. **Crie o ambiente na pasta do seu projeto**
    python -m venv venv

    # Ative o ambiente (Windows)
    .\venv\Scripts\activate

    # Ative o ambiente (Linux/macOS)
    # source venv/bin/activate

3.  **Instale as dependências:**
    ```bash
    cd raspberry_pi_streamer
    pip install -r requirements.txt
    ```

4.  **Execute o servidor de streaming:**
    ```bash
    python app.py
    ```

5.  O terminal exibirá uma mensagem indicando que o servidor foi iniciado. Anote o endereço IP do seu Raspberry Pi na rede.

### 2. Configuração do Computador Host (Detector)

**Passos:**

1.  **Clone o repositório** no seu computador.

2. **Crie o ambiente na pasta do seu projeto**
    python -m venv venv

    # Ative o ambiente (Windows)
    .\venv\Scripts\activate

    # Ative o ambiente (Linux/macOS)
    source venv/bin/activate

3.  **Instale as dependências:**
    *   É altamente recomendado criar um ambiente virtual (`venv`).
    *   Instale o PyTorch seguindo as instruções oficiais para seu sistema (CPU ou GPU): [https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/)
    
    * pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu129

    *   Instale as demais dependências:
        ```bash
        pip install -r requirements.txt
        ```

4.  **Atualize o endereço do Stream:**
    *   Abra o arquivo `run_detection.py`.
    *   Na linha `STREAM_URL = 'http://192.168.0.131:5000/video_feed'`, **substitua `192.168.0.131` pelo endereço IP real do seu Raspberry Pi**.

5.  **Execute o script de detecção:**
    ```bash
    python run_detection.py
    ```

6.  Uma janela do OpenCV aparecerá, exibindo o vídeo ao vivo do Raspberry Pi com os objetos detectados.

## Justificativa das Escolhas

*   **Hardware (Raspberry Pi 3):** A escolha do Raspberry Pi 3 em vez do ESP32-CAM se deu pela maior flexibilidade e poder de processamento. O Raspberry Pi possui um sistema operacional completo (Raspberry Pi OS), facilitando o desenvolvimento com bibliotecas Python robustas como `picamera2` e `Flask`. Sua capacidade de 1GB de RAM é mais do que suficiente para a tarefa de captura e streaming, garantindo uma transmissão estável e com menor latência.

*   **Comunicação (Wi-Fi e Flask):** A comunicação Wi-Fi é essencial para a mobilidade do sistema de câmera. O uso de um servidor web com Flask para criar um stream MJPEG é uma abordagem padrão da indústria, de fácil implementação e amplamente compatível. Qualquer cliente HTTP, como o OpenCV neste projeto, pode consumir o stream sem a necessidade de protocolos complexos.

*   **Software (Python, OpenCV, YOLOv5):** Python foi escolhido por ser a linguagem padrão para projetos de IA e Visão Computacional, com um vasto ecossistema de bibliotecas. O OpenCV é a ferramenta ideal para manipulação de imagens e vídeo. O YOLOv5 foi utilizado para manter a consistência com o ambiente do projeto original, aproveitando o modelo `best.pt` já treinado para realizar a detecção de objetos de forma eficiente no computador host.

## 🔧 Como executar o código

Este projeto foi desenvolvido em **Python** e utiliza **Jupyter Notebook** para documentar todo o fluxo de análise de dados e Machine Learning.

### Pré-requisitos

- Python 3.9 ou superior  
- Jupyter Notebook ou Jupyter Lab  
- Bibliotecas Python:
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `seaborn`
  - `scikit-learn`(from `sklearn.model_selection` import `train_test_split`)

> **Dica:** É recomendado criar um ambiente virtual antes de instalar as bibliotecas.

### Passo a passo

1. **Clonar o repositório**  
   ```bash
   git clone https://github.com/danivrf/challenge-fase5-FIAP.git
2. **Navegar até a pasta do projeto**
    ```bash
   cd challenge-fase5-FIAP
3. **Instalar as bibliotecas necessárias**
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn
4. **Abrir o notebook**
   - Entre na pasta `_notebooks`
   - Abra o arquivo `.ipynb` no Jupyter Notebook ou Jupyter Lab
 5. **Executar o notebook**
    - Execute as células na ordem, que incluem:
        - Análise exploratória dos dados
        - Preparação do dataset
        - Construção e treinamento do modelo de Machine Learning
        - Visualizações e gráficos de resultados
 **Visualizar resultados**
    - Os gráficos e outputs do notebook mostram insights sobre os dados coletados pelos sensores e as predições do modelo.
   
**Concluindo a Aplicação em Tempo Real:** O modelo treinado foi integrado com sucesso em um sistema de edge computing. O sistema se comportou de forma robusta: o Raspberry Pi provou ser uma solução de baixo custo e eficiente para a captura e streaming de vídeo com baixa latência, enquanto o computador host conseguiu processar o feed em tempo real e aplicar o modelo para detecção ao vivo. A comunicação entre os dispositivos foi estável e consistente.

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

