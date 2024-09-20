import argparse
import os
import sys
import torch
import rdkit

from moses.script_utils import add_train_args, read_smiles_csv, set_seed
from moses.models_storage import ModelsStorage
from moses.dataset import get_dataset

lg = rdkit.RDLogger.logger()
lg.setLevel(rdkit.RDLogger.CRITICAL)

MODELS = ModelsStorage()

from sklearn.model_selection import train_test_split
import pandas as pd
def get_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        title='Models trainer script', description='available models'
    )
    for model in MODELS.get_model_names():
        add_train_args(
            MODELS.get_model_train_parser(model)(
                subparsers.add_parser(model)
            )
        )
    return parser


def main(model, config):
    set_seed(config.seed)
    device = torch.device(config.device)
    #data = pd.read_csv('./data/DF_pubchem_1million.csv')
    #train_data, val_data = train_test_split(list(data['SMILES']), test_size=0.2, random_state=42)
    
    # Load the pre-split dataset.
    train_data = pd.read_csv('./data/PolyInfo_train.csv')['Smiles']
    val_data = pd.read_csv('./data/PolyInfo_test.csv')['Smiles']
    
    if config.config_save is not None:
        torch.save(config, config.config_save)

    # For CUDNN to work properly
    if device.type.startswith('cuda'):
        torch.cuda.set_device(device.index or 0)

    trainer = MODELS.get_model_trainer(model)(config)

    if config.vocab_load is not None:
        assert os.path.exists(config.vocab_load), \
            'vocab_load path does not exist!'
        vocab = torch.load(config.vocab_load)
    else:
        vocab = trainer.get_vocabulary(train_data)

    if config.vocab_save is not None:
        torch.save(vocab, config.vocab_save)

    model = MODELS.get_model_class(model)(vocab, config).to(device)

    
    print("in train.py")
    #print(data)
    print('train_data')
    print(type(train_data))
    print(len(train_data))
    print('val_data')
    print(type(val_data))
    print(len(val_data))
#    train_data = ['*CCC*','*CCC*','*CCC*','*CCC*','*CCC*',
#                  '*CCC*','*CCC*','*CCC*','*CCC*','*CCC*',
#                  '*CCC*','*CCC*','*CCC*','*CCC*','*CCC*',
#                  '*CCC*','*CCC*','*CCC*','*CCC*','*CCC*',
#                  '*CCC*','*CCC*','*CCC*','*CCC*','*CCC*',]
#    val_data =   ['*CCC*','*CCC*','*CCC*','*CCC*','*CCC*',
#                  '*CCC*','*CCC*','*CCC*','*CCC*','*CCC*',
#                  '*CCC*','*CCC*','*CCC*','*CCC*','*CCC*',
#                  '*CCC*','*CCC*','*CCC*','*CCC*','*CCC*',
#                  '*CCC*','*CCC*','*CCC*','*CCC*','*CCC*',]

    trainer.fit(model, train_data, val_data)

    model = model.to('cpu')
    torch.save(model.state_dict(), config.model_save)


if __name__ == '__main__':
    parser = get_parser()
    config = parser.parse_args()
    model = sys.argv[1]
    main(model, config)
