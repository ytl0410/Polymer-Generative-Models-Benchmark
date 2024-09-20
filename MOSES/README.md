# Download the Moses Docker image.
```
docker pull molecular sets/moses
```

# Create a container.
```
nvidia-docker run -it --name moses --network="host" --shm-size 10G molecularsets/moses
```

# Copy files from the local machine to the Moses Docker container.
```
docker cp /Your address/PolyInfo_train.csv 5cb4325a3cdf:/moses/data/PolyInfo_train.csv
docker cp /Your address/PolyInfo_train.csv 5cb4325a3cdf:/moses/data/PolyInfo_test.csv
docker cp /Your address/PolyInfo_train.csv 5cb4325a3cdf:/moses/scripts/train_polymer.py
```

# Load the Moses Docker container.
```
docker start moses_t
docker attach moses_t
```

# Train a AAE model.
```
mkdir checkpoint_aae
cd checkpoint_aae
touch vocab.pt
touch config.pt
cd ..
python scripts/train_polymer.py aae --device cuda:0 --model_save checkpoint_aae/model.pt --train_load data/PolyInfo_train.csv --config_save checkpoint_aae/config.pt --vocab_save checkpoint_aae/vocab.pt
```

# Use the trained AAE model to generate hypothetical polymer structures.
python scripts/sample.py aae --model_load checkpoint_aae/model.pt --vocab_load checkpoint_aae/vocab.pt --config_load checkpoint_aae/config.pt --n_samples 10000000 --gen_save checkpoint_aae/aae_gene_10m.csv

# Train a VAE model.
```
mkdir checkpoint_vae
cd checkpoint_vae
touch vocab.pt
touch config.pt
cd ..
python scripts/train_polymer.py vae --device cuda:0 --model_save checkpoint_vae/model.pt --train_load data/PolyInfo_train.csv --config_save checkpoint_vae/config.pt --vocab_save checkpoint_vae/vocab.pt
```

# Use the trained VAE model to generate hypothetical polymer structures.
```
python scripts/sample.py vae --model_load checkpoint_vae/model.pt --vocab_load checkpoint_vae/vocab.pt --config_load checkpoint_vae/config.pt --n_samples 10000000 --gen_save checkpoint_vae/vae_gene_10m.csv
```

# Train a CharRNN model.
```
mkdir checkpoint_char_rnn
cd checkpoint_char_rnn
touch vocab.pt
touch config.pt
cd ..
python scripts/train_PolyInfo.py char_rnn --device cuda:0 --model_save checkpoint_char_rnn/model.pt --train_load data/PolyInfo_train.csv --config_save checkpoint_char_rnn/config.pt --vocab_save checkpoint_char_rnn/vocab.pt
```

# Use the trained CharRNN model to generate hypothetical polymer structures.
```
python scripts/sample.py char_rnn --model_load checkpoint_char_rnn/model.pt --vocab_load checkpoint_char_rnn/vocab.pt --config_load checkpoint_char_rnn/config.pt --n_samples 10000000 --gen_save checkpoint_char_rnn/char_rnn_gene_10m.csv
```

# Train a ORGAN model. Chemical validity and uniqueness are defined as rewards.
```
mkdir checkpoint_organ
cd checkpoint_organ
touch vocab.pt
touch config.pt
cd ..
python scripts/train_polymer.py organ --device cuda:0 --model_save checkpoint_organ/model.pt --train_load data/PolyInfo_train.csv --config_save checkpoint_organ/config.pt --vocab_save checkpoint_organ/vocab.pt
```

# Use the trained ORGAN model to generate hypothetical polymer structures.
````
python scripts/sample.py organ --model_load checkpoint_organ/model.pt --vocab_load checkpoint_organ/vocab.pt --config_load checkpoint_organ/config.pt --n_samples 10000000 --gen_save checkpoint_organ/organ_gene_10m.csv
```

#Evaluate the generation results
```
python scripts/eval.py --test_path PolyInfo_eva/PolyInfo_test.csv --train_path PolyInfo_eva/PolyInfo_train.csv --gen_path PolyInfo_eva/aae_gene_10m.csv > PI_aae.txt
python scripts/eval.py --test_path PolyInfo_eva/PolyInfo_test.csv --train_path PolyInfo_eva/PolyInfo_train.csv --gen_path PolyInfo_eva/vae_gene_10m.csv > PI_vae.txt
python scripts/eval.py --test_path PolyInfo_eva/PolyInfo_test.csv --train_path PolyInfo_eva/PolyInfo_train.csv --gen_path PolyInfo_eva/char_rnn_gene_10m.csv > PI_char_rnn.txt
python scripts/eval.py --test_path PolyInfo_eva/PolyInfo_test.csv --train_path PolyInfo_eva/PolyInfo_train.csv --gen_path PolyInfo_eva/organ_gene_10m.csv > PI_organ.txt
```

