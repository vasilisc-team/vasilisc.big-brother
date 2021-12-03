from copy import deepcopy
from pathlib import Path

import torch


def init_detection_model(model_name, half=False, device="cuda"):
    from facexlib.detection.retinaface import RetinaFace

    model = RetinaFace(network_name="resnet50", half=half)
    model_path = (Path(__file__).parent / "data" / "detection_Resnet50_Final.pth").as_posix()
    # TODO: clean pretrained model
    load_net = torch.load(model_path, map_location=lambda storage, loc: storage)
    # remove unnecessary 'module.'
    for k, v in deepcopy(load_net).items():
        if k.startswith("module."):
            load_net[k[7:]] = v
            load_net.pop(k)
    model.load_state_dict(load_net, strict=True)
    model.eval()
    model = model.to(device)
    return model
