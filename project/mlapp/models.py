# coding: utf-8
import logging

from sklearn.externals import joblib
from django.core.files.storage import default_storage

from mlapp.core.mlmodel import MLModel

logger = logging.getLogger(__name__)


class Trainer:
    def __init__(self):
        self._model = MLModel()

    def prepare(self):
        pass

    def train(self, update_multipliers):
        logger.info('Starting training routine')
        self._model.fit()
        logger.info('Completed training routine')

    def save_model(self):
        logger.info('Saving the model')
        model_file = default_storage.open('mlapp/model/model.pkl', 'wb')
        model_file.write(open(joblib.dump(self._model, '/tmp/model.pkl', compress=5)[0], 'rb').read())
        model_file.close()
        logger.info('Model saved')


class Predictor:
    def __init__(self):
        self._model = None

    def load_model(self):
        try:
            logger.info('Loading model')
            model_file = default_storage.open(settings.MODEL_PATH, 'rb')
            self._model = joblib.load(model_file)
            model_file.close()
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
