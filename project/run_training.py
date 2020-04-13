from mlapp.models import Trainer

if __name__ == '__main__':
    trainer = Trainer()
    trainer.prepare()
    trainer.train()
    trainer.save_model()
