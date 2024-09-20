# Download the Moses Docker image.
# You can choose the official version.
```
docker pull molecular sets/moses
```

# Create a container.
nvidia-docker run -it --name moses --network="host" --shm-size 10G molecularsets/moses


# Copy files from the local machine to the Moses Docker container.
docker cp /home/data1/ytl/BenchmarkInverse/PolyInfo_BigSMILES_train.csv 5cb4325a3cdf:/moses/data/PolyInfo_BigSMILES_train.csv
docker cp /home/data1/ytl/BenchmarkInverse/PolyInfo_BigSMILES_test.csv 5cb4325a3cdf:/moses/data/PolyInfo_BigSMILES_test.csv
docker cp /home/data1/ytl/BenchmarkInverse/train_PolyInfo_BigSMILES.py 5cb4325a3cdf:/moses/scripts/train_PolyInfo_BigSMILES.py

# Load the Moses Docker container.
docker start moses_t
docker attach moses_t

# Train a AAE model.
mkdir checkpoint_aae_PI_BS
cd checkpoint_aae_PI_BS
touch vocab.pt
touch config.pt
cd ..
python scripts/train_PolyInfo_BigSMILES.py aae --device cuda:0 --model_save checkpoint_aae_PI_BS/model.pt --train_load data/PolyInfo_BigSMILES_train.csv --config_save checkpoint_aae_PI_BS/config.pt --vocab_save checkpoint_aae_PI_BS/vocab.pt

# Use the trained AAE model to generate hypothetical polymer structures.
python scripts/sample.py aae --model_load checkpoint_aae_PI_BS/model.pt --vocab_load checkpoint_aae_PI_BS/vocab.pt --config_load checkpoint_aae_PI_BS/config.pt --n_samples 10000000 --gen_save checkpoint_aae_PI_BS/aae_BS_gene_10m.csv

# Train a VAE model.
mkdir checkpoint_vae_PI_BS
cd checkpoint_vae_PI_BS
touch vocab.pt
touch config.pt
cd ..
python scripts/train_PolyInfo_BigSMILES.py vae --device cuda:0 --model_save checkpoint_vae_PI_BS/model.pt --train_load data/PolyInfo_BigSMILES_train.csv --config_save checkpoint_vae_PI_BS/config.pt --vocab_save checkpoint_vae_PI_BS/vocab.pt

# Use the trained VAE model to generate hypothetical polymer structures.
python scripts/sample.py vae --model_load checkpoint_vae_PI_BS/model.pt --vocab_load checkpoint_vae_PI_BS/vocab.pt --config_load checkpoint_vae_PI_BS/config.pt --n_samples 10000000 --gen_save checkpoint_vae_PI_BS/vae_BS_gene_10m.csv

# Train a CharRNN model.
mkdir checkpoint_char_rnn_PI_BS
cd checkpoint_char_rnn_PI_BS
touch vocab.pt
touch config.pt
cd ..
python scripts/train_PolyInfo_BigSMILES.py char_rnn --device cuda:0 --model_save checkpoint_char_rnn_PI_BS/model.pt --train_load data/PolyInfo_BigSMILES_train.csv --config_save checkpoint_char_rnn_PI_BS/config.pt --vocab_save checkpoint_char_rnn_PI_BS/vocab.pt

# Use the trained CharRNN model to generate hypothetical polymer structures.
python scripts/sample.py char_rnn --model_load checkpoint_char_rnn_PI_BS/model.pt --vocab_load checkpoint_char_rnn_PI_BS/vocab.pt --config_load checkpoint_char_rnn_PI_BS/config.pt --n_samples 10000000 --gen_save checkpoint_char_rnn_PI_BS/char_rnn_BS_gene_10m.csv

# Train a ORGAN model. Chemical validity and uniqueness are defined as rewards.
mkdir checkpoint_organ_PI_BS
cd checkpoint_organ_PI_BS
touch vocab.pt
touch config.pt
cd ..
python scripts/train_PolyInfo_BigSMILES.py organ --device cuda:0 --model_save checkpoint_organ_PI_BS/model.pt --train_load data/PolyInfo_BigSMILES_train.csv --config_save checkpoint_organ_PI_BS/config.pt --vocab_save checkpoint_organ_PI_BS/vocab.pt

# Use the trained ORGAN model to generate hypothetical polymer structures.
python scripts/sample.py organ --model_load checkpoint_organ_PI_BS/model.pt --vocab_load checkpoint_organ_PI_BS/vocab.pt --config_load checkpoint_organ_PI_BS/config.pt --n_samples 10000000 --gen_save checkpoint_organ_PI_BS/organ_BS_gene_10m.csv

#Evaluate the generation results
python scripts/eval.py --test_path PolyInfo_eva/PolyInfo_test.csv --train_path PolyInfo_eva/PolyInfo_train.csv --gen_path PolyInfo_eva/aae_BS_gene_10m.csv > PI_aae_BS.txt
python scripts/eval.py --test_path PolyInfo_eva/PolyInfo_test.csv --train_path PolyInfo_eva/PolyInfo_train.csv --gen_path PolyInfo_eva/vae_BS_gene_10m.csv > PI_vae_BS.txt
python scripts/eval.py --test_path PolyInfo_eva/PolyInfo_test.csv --train_path PolyInfo_eva/PolyInfo_train.csv --gen_path PolyInfo_eva/char_rnn_BS_gene_10m.csv > PI_char_rnn_BS.txt
python scripts/eval.py --test_path PolyInfo_eva/PolyInfo_test.csv --train_path PolyInfo_eva/PolyInfo_train.csv --gen_path PolyInfo_eva/organ_BS_gene_10m.csv > PI_organ_BS.txt

# Train a REINVENT model.
# Please refer to https://github.com/undeadpixel/reinvent-randomized to install REINVENT, or refer to https://github.com/MolecularAI/REINVENT4 to install the latest version of REINVENT.
mkdir -p PI_BS/models
python ./create_model.py -i training_sets/PolyInfo_BigSMILES.smi -o PI_BS/models/model.empty
python ./train_model.py -i PI_BS/models/model.empty -o PI_BS/models/model.trained -s training_sets/PolyInfo_BigSMILES_train.smi -e 100 --lrm exp --lrg 0.9 --csl PI_BS/tensorboard --csv trained_models/PolyInfo_BigSMILES_test.smi --csn 10000
python ./sample_from_model.py -m PI_BS/models/model.trained.100 -o PI_BS_10m_Reinvent.csv -n 10000000

