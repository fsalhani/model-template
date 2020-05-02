# coding: utf-8
import logging

import joblib
from mlapp.core.mlmodel import MLModel

logger = logging.getLogger(__name__)


class Trainer:
    def __init__(self):
        self._model = MLModel()

    def prepare(self):
        pass

    def train(self):
        logger.info('Starting training routine')
        self._model.fit()
        logger.info('Completed training routine')

    def save_model(self):
        logger.info('Saving the model')
        with open('mlapp/model/model.pkl', 'wb') as model_file:
            joblib.dump(self._model, model_file)
        logger.info('Model saved')


class Predictor:
    def __init__(self):
        self._model = None

    def load_model(self):
        try:
            logger.info('Loading model')
            with open('mlapp/model/model.pkl', 'rb') as model_file:
                self._model = joblib.load(model_file)
            logger.info('Model loaded')
            return True
        except (ValueError, IOError) as e:
            logger.info('Model is either empty or the wrong type')
            raise e

    def predict(self, data):
        if self._model is None:
            self.load_model()

        predicted_data = self._model.predict()

        return predicted_data
