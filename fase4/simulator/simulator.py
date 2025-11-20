from time import sleep
import random
import requests

valores_sensores = {}

API_URL = "http://localhost:8004"

def sensor_simulator(sensor_name, valor_sensor = 0):
    if valor_sensor == 0:
        if "temperature" in sensor_name.lower():
            return random.uniform(28, 50)
        elif "humidity" in sensor_name.lower():
            return random.uniform(20, 55)
        elif "ph" in sensor_name.lower():
            return random.uniform(6, 14)
        else:
            return random.uniform(0, 100)

    else:
        valor = valor_sensor + random.uniform(-3, 3)
        if "temperature" in sensor_name.lower():
            return max(28, min(50, valor))
        elif "humidity" in sensor_name.lower():
            return max(20, min(55, valor))
        elif "ph" in sensor_name.lower():
            return max(6, min(14, valor))
        else:
            return max(0, min(100, valor))


def create_sensors():
    sensor_temperature = requests.post(f"{API_URL}/sensores/", json={"nome": "sensor_temperature"})
    sensor_humidity = requests.post(f"{API_URL}/sensores/", json={"nome": "sensor_humidity"})
    sensor_ph = requests.post(f"{API_URL}/sensores/", json={"nome": "sensor_ph"})
    sensor_p = requests.post(f"{API_URL}/sensores/", json={"nome": "sensor_p"})
    sensor_k = requests.post(f"{API_URL}/sensores/", json={"nome": "sensor_k"})


    return [sensor_temperature.json(), sensor_humidity.json(), sensor_ph.json(), sensor_p.json(), sensor_k.json()]


def execSimulator():
    while True:
        sleep(1)
        print("Simulando leitura")

        #resgatar sensores
        response = requests.get(f"{API_URL}/sensores/")
        sensores = response.json()

        if not sensores:
            sensores = create_sensors()

        for sensor in sensores:
            valor_anterior_sensor = valores_sensores.get(sensor['nome']) or 0

            #simular leitura
            valor = sensor_simulator(sensor['nome'], valor_anterior_sensor)

            print(f"Valor sensor {sensor['nome']}: {valor}")
            
            response = requests.post(f"{API_URL}/leituras/", json={"valor": valor, "sensor_id": sensor['id']})
            print(response.json())
            valores_sensores[sensor['nome']] = valor

        #prever
        response = requests.post(f"{API_URL}/predict", json={"sensor_humidity": valores_sensores['sensor_humidity'], "sensor_k": valores_sensores['sensor_k'], "sensor_p": valores_sensores['sensor_p'], "sensor_ph": valores_sensores['sensor_ph'], "sensor_temperature": valores_sensores['sensor_temperature']})
        print(response.json())