# Train a REINVENT model with Reinforcement Learning

Please refer to https://github.com/MolecularAI/Reinvent to install REINVENT 3.2.
ReinventCommunity (Jupyter notebook tutorials for REINVENT 3.2) is an excellent collection of useful Jupyter notebooks, code snippets, and example JSON files that illustrate how to use REINVENT 3.2.

Before using reinforcement learning to train REINVENT, it is necessary to pretrain a REINVENT model. Please refer to https://github.com/undeadpixel/reinvent-randomized to install REINVENT. And train your model by

```
mkdir -p PI_BS/models
python ./create_model.py -i training_sets/PolyInfo.smi -o PI/models/model.empty
python ./train_model.py -i PI/models/model.empty -o PI/models/model.trained -s training_sets/PolyInfo_train.smi -e 100 --lrm exp --lrg 0.9 --csl PI/tensorboard --csv trained_models/PolyInfo_test.smi --csn 10000
```

You can also use the well-trained REINVENT models provided in `Polymer-Generative-Models-Benchmark/Well-trained models/`.

In addition, a well-trained machine learning (ML) model is required to predict the $T_g$ values of the polymer, acting as the predictor.
You can directly download and use the 'Tg_1.pkl' model available in this folder.
Be sure to update the `"model_path"` under `"scoring_function"` in the script accordingly.
If you wish to apply reinforcement learning to other properties, you will need to train a different model specific to that property.

After modifying all the address information in the script, you can start reinforcement learning in the `reinvent.v3.2` environment using
```
python [Your address]/Reinvent-master/input.py REINVENT_RL.json
```

# Train a GraphINVENT model with Reinforcement Learning

