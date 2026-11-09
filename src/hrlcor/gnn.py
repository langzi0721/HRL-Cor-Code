"""The supplied SI GNN architecture and training schedule, without changing preprocessing."""
import random
import numpy as np
import pandas as pd
from .data import DESCRIPTORS
from .models import metrics


def run(frame, save):
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from rdkit import Chem
    random.seed(42); np.random.seed(42); torch.manual_seed(42)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(42)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def graph(smiles):
        mol = Chem.MolFromSmiles(smiles)
        if mol is None: raise ValueError('Invalid SMILES: ' + smiles)
        adjacency = Chem.GetAdjacencyMatrix(mol) + np.eye(mol.GetNumAtoms())
        features = [[atom.GetAtomicNum(), atom.GetDegree()] for atom in mol.GetAtoms()]
        return torch.tensor(adjacency, dtype=torch.float32, device=device), torch.tensor(features, dtype=torch.float32, device=device)

    class HybridGNN(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = nn.Linear(2, 32); self.conv2 = nn.Linear(32, 64)
            self.descr_fc = nn.Linear(5, 32)
            self.fc_out = nn.Sequential(nn.Linear(96, 64), nn.ReLU(), nn.Dropout(.1), nn.Linear(64, 1))

        def forward(self, adj, x, descr):
            x = F.relu(self.conv1(torch.mm(adj, x)))
            x = F.relu(self.conv2(torch.mm(adj, x))).mean(dim=0)
            return self.fc_out(torch.cat([x, F.relu(self.descr_fc(descr))], dim=0))

    # Original GNN input order differs from FS60 order and must be preserved.
    columns = ['LUMO / eV', 'CATS3D_02_AP', 'Mor04m', 'E1p', 'P_VSA_MR_5']
    descriptors = torch.tensor(frame[columns].to_numpy(), dtype=torch.float32, device=device)
    labels = torch.tensor(frame.ie_ze41.to_numpy(), dtype=torch.float32, device=device)
    graphs = [graph(s) for s in frame.isomeric_smiles]
    model = HybridGNN().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=.0005, weight_decay=.0001)
    model.train()
    for epoch in range(200):
        for i in range(60):
            optimizer.zero_grad()
            loss = F.mse_loss(model(*graphs[i], descriptors[i]), labels[i].reshape(1))
            loss.backward(); optimizer.step()
    model.eval()
    with torch.no_grad(): predictions = np.array([model(*graphs[i], descriptors[i]).item() for i in range(60, 75)])
    save('gnn_metrics', pd.DataFrame([{'Model': 'GNN', 'Device': str(device), **metrics(frame.ie_ze41.to_numpy()[60:], predictions)}]))
    save('gnn_predictions', pd.DataFrame({'Molecule': frame.name.iloc[60:].to_numpy(), 'True_IE': frame.ie_ze41.iloc[60:].to_numpy(), 'Predicted_IE': predictions}))
