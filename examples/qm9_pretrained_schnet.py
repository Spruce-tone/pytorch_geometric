import os.path as osp

import torch

from torch_geometric.nn import SchNet
from torch_geometric.data import DataLoader
from torch_geometric.datasets import QM9

path = osp.join(osp.dirname(osp.realpath(__file__)), '..', 'data', 'QM9')
dataset = QM9(path)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

for target in range(12):
    model, datasets = SchNet.from_qm9_pretrained(path, dataset, target)
    train_dataset, val_dataset, test_dataset = datasets

    model = model.to(device)
    loader = DataLoader(test_dataset, batch_size=256)

    maes = []
    for data in loader:
        data = data.to(device)
        with torch.no_grad():
            pred = model(data.z, data.pos, data.batch)
        mae = (pred.view(-1) - data.y[:, target]).abs()
        maes.append(mae)

    mae = torch.cat(maes, dim=0)
    print(f'Target: {target:02d}, MAE: {mae.mean():.5f} ± {mae.std():.5f}')
