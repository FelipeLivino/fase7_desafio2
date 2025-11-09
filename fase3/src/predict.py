import joblib
from typing import List
import os

from src.schemas import PredictCreate

# Construct the absolute path to the model file
path_model = os.path.join(os.path.dirname(__file__), '..', 'saved_models', 'RandomForest_model.joblib')

class ModelPredicter:
    def __init__(self):
        self.model = joblib.load(path_model)

    def predict(self, data : PredictCreate):
        return self.model.predict([self.preprocess(data)])
    
    def preprocess(self, data : PredictCreate) -> List[float]:
        return [data.sensor_humidity, data.sensor_k, data.sensor_p, data.sensor_ph, data.sensor_temperature]
        