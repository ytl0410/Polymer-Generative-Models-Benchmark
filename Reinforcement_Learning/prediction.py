import torch
import torch.nn as nn
import pandas as pd
import argparse
from rdkit import Chem
from rdkit.Chem import AllChem

# Define the Feedforward Neural Network
class FFNN(nn.Module):
    def __init__(self):
        super(FFNN, self).__init__()
        self.fc1 = nn.Linear(1024, 256)
        self.fc2 = nn.Linear(256, 64)
        self.fc3 = nn.Linear(64, 2048)
        self.fc4 = nn.Linear(2048, 512)
        self.fc5 = nn.Linear(512, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = torch.relu(self.fc4(x))
        x = self.fc5(x)
        return x

def load_model(model_path='Tg.pth'):
    # Load the pre-trained model
    model = FFNN()
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

def smiles_to_fingerprint(smiles):
    """Convert a SMILES string to a Morgan fingerprint."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES string: {smiles}")
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=3, nBits=1024)
    return torch.tensor(list(fp), dtype=torch.float32).unsqueeze(0)  # Add batch dimension

def predict(model, smiles):
    """Predict property for a single SMILES string."""
    fingerprint = smiles_to_fingerprint(smiles)
    with torch.no_grad():
        prediction = model(fingerprint).item()  # Get single prediction value
    return prediction

def main(input_file):
    # Load the model
    model = load_model()

    # Load SMILES from CSV
    df = pd.read_csv(input_file)
    if 'Smiles' not in df.columns:
        raise ValueError("Input CSV must contain a 'Smiles' column")

    # Predict for each SMILES
    predictions = []
    for smiles in df['Smiles']:
        try:
            result = predict(model, smiles)
            predictions.append((smiles, result))
            print(f"SMILES: {smiles}, Prediction: {result}")
        except ValueError as e:
            print(e)
            predictions.append((smiles, None))

    # Optionally save predictions to CSV
    output_df = pd.DataFrame(predictions, columns=['Smiles', 'Prediction'])
    output_df.to_csv("predictions_output.csv", index=False)
    print("Predictions saved to predictions_output.csv")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict properties for SMILES in a CSV file.")
    parser.add_argument("input_file", type=str, help="Path to the input CSV file containing SMILES.")
    args = parser.parse_args()
    main(args.input_file)
