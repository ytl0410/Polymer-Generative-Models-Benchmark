# Train a REINVENT model.
Please refer to https://github.com/undeadpixel/reinvent-randomized to install REINVENT, or refer to https://github.com/MolecularAI/REINVENT4 to install the latest version of REINVENT.

```
mkdir -p PI/models
python ./create_model.py -i training_sets/PolyInfo.smi -o PI/models/model.empty
python ./train_model.py -i PI/models/model.empty -o PI/models/model.trained -s training_sets/PolyInfo_train.smi -e 100 --lrm exp --lrg 0.9 --csl PI/tensorboard --csv trained_models/PolyInfo_test.smi --csn 10000
```

# Use the trained REINVENT model to generate hypothetical polymer structures.
```
python ./sample_from_model.py -m PI/models/model.trained.100 -o PI_10m_Reinvent.csv -n 10000000
```

# Train a GraphINVENT model.
Please refer to https://github.com/MolecularAI/GraphINVENT to install GraphINVENT. Modify the file paths in the script according to the address of the dataset.

```
python GI_preprocess.py
python GI_train.py
```

# Use the trained GraphINVENT model to generate hypothetical polymer structures.
```
python GI_generation.py
```
