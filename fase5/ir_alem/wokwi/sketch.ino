#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <DHT.h>
#include "time.h"

// --- CONFIGURAÇÕES DE REDE ---
#define WIFI_SSID "Wokwi-GUEST"
#define WIFI_PASSWORD ""
#define RECONNECT_INTERVAL_MS 5000

// --- CONFIGURAÇÕES NTP ---
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = -3 * 3600; // Fuso Horário GMT-3 (Brasília)
const int   daylightOffset_sec = 0;    // Sem horário de verão

// --- PINOS E SENSORES ---
#define BOTAO_CHUVA 22
#define LDR_PINO 34
#define DHT_PINO 19
#define DHT_TIPO DHT22
#define PO_UMIDADE_SOLO 35
#define PO_PH_SOLO 32

// --- INTERVALOS E CONSTANTES ---
#define INTERVALO_COLETA_MS 5000
#define JSON_DOC_SIZE 512

// --- INICIALIZAÇÃO DOS COMPONENTES ---
DHT dht(DHT_PINO, DHT_TIPO);

// --- ESTRUTURA PARA PASSAR DADOS PARA A TAREFA WEB ---
struct SensorDataPayload {
  int16_t luminosidade_x10;
  int16_t temperatura_x10;
  int16_t umidade_x10;
  int16_t umidadeSolo_x10;
  int16_t phSolo_x10;
  bool simuladorChuva;
};

// --- VARIÁVEIS GLOBAIS OTIMIZADAS ---
unsigned long ultimoTempoColeta = 0;
bool chovendo = false;
bool ultimoEstadoBotao = HIGH; 
unsigned long ultimoTempoDebounce = 0; 
TaskHandle_t tarefaEnvioHandle = NULL;
TimerHandle_t wifiReconnectTimer;

// Protótipos de Funções
void conectarWiFi();
void tarefaEnvioWebService(void *parametros);
void WiFiEvent(WiFiEvent_t event);


void setup() {
  Serial.begin(115200);
  wifiReconnectTimer = xTimerCreate("wifiTimer", pdMS_TO_TICKS(RECONNECT_INTERVAL_MS), pdFALSE, (void*)0, [](TimerHandle_t xTimer){ conectarWiFi(); });

  pinMode(BOTAO_CHUVA, INPUT_PULLUP);
  pinMode(LDR_PINO, INPUT);
  pinMode(PO_UMIDADE_SOLO, INPUT);
  pinMode(PO_PH_SOLO, INPUT);

  dht.begin();
  
  WiFi.onEvent(WiFiEvent);
  conectarWiFi();
}

void loop() {
  bool estadoAtualBotao = digitalRead(BOTAO_CHUVA);
  if (estadoAtualBotao == LOW && ultimoEstadoBotao == HIGH) {
    if ((millis() - ultimoTempoDebounce) > INTERVALO_COLETA_MS) {
      chovendo = !chovendo; // Inverte o estado da chuva
      Serial.printf("--> Simulador de chuva alterado para: %s\n", chovendo ? "ATIVO" : "INATIVO");
      ultimoTempoDebounce = millis();
    }
  }
  ultimoEstadoBotao = estadoAtualBotao;

  if (millis() - ultimoTempoColeta >= INTERVALO_COLETA_MS) {
    ultimoTempoColeta = millis();
    int16_t luminosidade = map(analogRead(LDR_PINO), 0, 4095, 1000, 0); 
    int16_t tempInt = (int16_t)(dht.readTemperature() * 10);
    int16_t umidInt = (int16_t)(dht.readHumidity() * 10);
    int16_t umidadeSolo = map(analogRead(PO_UMIDADE_SOLO), 0, 4095, 0, 1000); 
    int16_t phSolo = map(analogRead(PO_PH_SOLO), 0, 4095, 0, 140);

    Serial.println("\n--- Nova Leitura ---");
    Serial.printf("Luminosidade: %.1f %%\n", luminosidade / 10.0);
    Serial.printf("Temperatura: %.1f *C\n", tempInt / 10.0);
    Serial.printf("Umidade do Ar: %.1f %%\n", umidInt / 10.0);
    Serial.printf("Umidade do Solo: %.1f %%\n", umidadeSolo / 10.0);
    Serial.printf("pH do Solo: %.1f\n", phSolo / 10.0);
    Serial.printf("Chovendo: %s\n", chovendo ? "Sim" : "Nao");

    if (isnan(tempInt / 10.0) || isnan(umidInt / 10.0)) {
      Serial.println("Falha na leitura do sensor DHT!");
      return;
    }

    SensorDataPayload* payload = new SensorDataPayload{
      luminosidade, tempInt, umidInt, umidadeSolo, phSolo, chovendo
    };
    
    if (tarefaEnvioHandle == NULL || eTaskGetState(tarefaEnvioHandle) == eDeleted) {
        xTaskCreate(tarefaEnvioWebService, "WebServiceTask", 8192, (void*)payload, 1, &tarefaEnvioHandle);
    } else {
        Serial.println("A tarefa de envio anterior ainda esta em execucao. Ignorando novo envio.");
        delete payload;
    }
  }
}

void conectarWiFi() {
    Serial.println("Conectando ao WiFi...");
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
}

void WiFiEvent(WiFiEvent_t event) {
    Serial.printf("[WiFi Event] evento: %d\n", event);

    switch(event) {
        case ARDUINO_EVENT_WIFI_STA_GOT_IP:
            Serial.println("WiFi conectado!");
            Serial.print("IP: ");
            Serial.println(WiFi.localIP());
            
            configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
            Serial.println("Relógio sincronizado com servidor NTP.");
            
            if (xTimerIsTimerActive(wifiReconnectTimer)) {
                xTimerStop(wifiReconnectTimer, 0);
            }
            break;

        case ARDUINO_EVENT_WIFI_STA_DISCONNECTED:
            Serial.println("WiFi desconectado. Tentando reconectar...");
            xTimerStart(wifiReconnectTimer, 0);
            break;
            
        default:
            break;
    }
}

void tarefaEnvioWebService(void *parametros) {
  SensorDataPayload* dados = (SensorDataPayload*)parametros;

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin("https://newsfacd.herokuapp.com/journeybuilder/success");
    http.setTimeout(15000);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<JSON_DOC_SIZE> doc;
    doc["sensor"] = "ESP32_Otimizado";

    struct tm timeinfo;
    if (getLocalTime(&timeinfo)) {
        char timestamp[32];
        strftime(timestamp, sizeof(timestamp), "%Y-%m-%dT%H:%M:%SZ", &timeinfo);
        doc["timestamp"] = timestamp;
    } else {
        doc["timestamp"] = "1970-01-01T00:00:00Z"; 
    }

    JsonArray leituras = doc.createNestedArray("leituras");
    
    JsonObject luzObj = leituras.createNestedObject();
    luzObj["item"] = "luminosidade";
    luzObj["valor"] = dados->luminosidade_x10 / 10.0;
    
    JsonObject tempObj = leituras.createNestedObject();
    tempObj["item"] = "temperatura";
    tempObj["valor"] = dados->temperatura_x10 / 10.0;

    JsonObject umidObj = leituras.createNestedObject();
    umidObj["item"] = "umidade";
    umidObj["valor"] = dados->umidade_x10 / 10.0;

    JsonObject umidadeSoloObj = leituras.createNestedObject();
    umidadeSoloObj["item"] = "umidade_solo";
    umidadeSoloObj["valor"] = dados->umidadeSolo_x10 / 10.0;

    JsonObject phObj = leituras.createNestedObject();
    phObj["item"] = "ph";
    phObj["valor"] = dados->phSolo_x10 / 10.0; 

    JsonObject chuvaObj = leituras.createNestedObject();
    chuvaObj["item"] = "chovendo";
    chuvaObj["valor"] = dados->simuladorChuva;

    char httpRequestData[JSON_DOC_SIZE];
    serializeJsonPretty(doc, httpRequestData, sizeof(httpRequestData));

    Serial.println("\n[TAREFA WEB] Enviando JSON:");
    Serial.println(httpRequestData);

    int httpResponseCode = http.POST(httpRequestData);

    if (httpResponseCode > 0) {
      Serial.printf("[TAREFA WEB] Resposta HTTP: %d\n", httpResponseCode);
    } else {
      Serial.printf("[TAREFA WEB] Falha na requisicao: %s\n", http.errorToString(httpResponseCode).c_str());
    }
    http.end();
  } else {
    Serial.println("[TAREFA WEB] Sem WiFi. Envio cancelado.");
  }
  
  delete dados;
  vTaskDelete(NULL);
}
