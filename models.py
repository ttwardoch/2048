import torch
from torch import nn
import torch.nn.init as init
import copy


class Model1(nn.Module):
    def __init__(self):
        super(Model1, self).__init__()
        self.features = nn.Sequential(
            nn.Flatten(-2, 1),
            nn.Linear(16, 128),
            nn.Sigmoid(),
            nn.Linear(128, 128),
            nn.Sigmoid(),
            nn.Linear(128, 128),
            nn.Sigmoid(),
            nn.Linear(128, 128),
            nn.Sigmoid(),
            nn.Linear(128, 128),
            nn.Sigmoid(),
            nn.Linear(128, 4),
        )

    def forward(self, x):
        return self.features(x)


# Custom initialization function
def normal_init(m):
    if isinstance(m, nn.Linear):  # Apply only to Linear layers
        init.normal_(m.weight, mean=0.0, std=0.01)
        if m.bias is not None:
            init.normal_(m.bias, mean=0.0, std=0.000001)


def perturb_weights(model, std_dev=0.01):
    """Create a slightly perturbed version of the given model."""
    new_model = copy.deepcopy(model)  # Create a copy of the model
    with torch.no_grad():
        for param in new_model.parameters():
            param.add_(torch.randn_like(param) * std_dev)  # Add small noise
    return new_model