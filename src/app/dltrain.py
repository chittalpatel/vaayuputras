import numpy as np
from tensorflow.keras.models import load_model
from django.conf import settings
import logging

logger=logging.getLogger('app_api')
#class to deal with User personal model training and predictions
class TrainModel():
    #constructor method
    def __init__(self,api,ws,wp,cap,has_model):
        logger.info('loc10')
        #if user has model already pretrained then load it else load the general model
        if has_model:
            self.model=load_model(settings.MEDIA_ROOT+f'/{api}.h5')
        else:
            logger.info('loc11')
            self.model = load_model(settings.MEDIA_ROOT+'/lstm_baseline_lahaute gef.h5')
        logger.info('loc12')
        self.api=api
        self.wind_speed=ws
        self.wind_power=wp
        self.capacity=cap

    #method to train model
    def train(self):
        try:
            self.wind_speed=np.array(self.wind_speed).reshape((len(self.wind_speed), 1, 1))/25
            self.wind_power = np.array(self.wind_power).reshape((len(self.wind_power), 1, 1)) / self.capacity
        except:
            return False

        try:
            history = self.model.fit(self.wind_speed, self.wind_power, epochs=2, batch_size=4)
        except:
            return False

        self.model.save(settings.MEDIA_ROOT+f'/{self.api}.h5')
        return True

    #method to predict wind power
    def predict(self):
        self.wind_power=self.model.predict(self.wind_speed)*self.capacity
        wind_power=[wp[0][0] for wp in self.wind_power]
        return wind_power
