from speechset import AcousticDataset
from speechset.config import Config as DataConfig
from tacospawn.config import Config as ModelConfig


class TrainConfig:
    """Configuration for training loop.
    """
    def __init__(self):
        # optimizer
        self.learning_rate = 2e-4
        self.beta1 = 0.9
        self.beta2 = 0.999
        self.eps = 1e-8

        # loader settings
        self.batch = 32
        self.shuffle = True
        self.num_workers = 4
        self.pin_memory = True

        # train iters
        self.epoch = 100

        # path config
        self.log = './log'
        self.ckpt = './ckpt'

        # model name
        self.name = 't1'

        # commit hash
        self.hash = 'unknown'


class Config:
    """Integrated configuration.
    """
    def __init__(self, speakers: int):
        self.train = TrainConfig()
        # reset data.batch, use train.batch instead.
        self.data = DataConfig(batch=None)
        self.model = ModelConfig(
            AcousticDataset.VOCABS,
            self.data.mel,
            speakers)

    def dump(self):
        """Dump configurations into serializable dictionary.
        """
        return {k: vars(v) for k, v in vars(self).items()}

    @staticmethod
    def load(dump_):
        """Load dumped configurations into new configuration.
        """
        conf = Config()
        for k, v in dump_.items():
            if hasattr(conf, k):
                obj = getattr(conf, k)
                load_state(obj, v)
        return conf


def load_state(obj, dump_):
    """Load dictionary items to attributes.
    """
    for k, v in dump_.items():
        if hasattr(obj, k):
            setattr(obj, k, v)
    return obj
