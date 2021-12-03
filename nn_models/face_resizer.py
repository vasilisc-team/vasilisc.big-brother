from io import BytesIO
from pathlib import Path
from typing import List

import cv2
import numpy as np
from PIL import Image, UnidentifiedImageError
from tensorflow.python.keras.preprocessing.image import img_to_array

# prevent download model from github
from .helper import init_detection_model  # isort:skip
import facexlib  # isort:skip

facexlib.detection.init_detection_model = init_detection_model  # isort:skip
from gfpgan import GFPGANer  # isort:skip


class GFPGANConnector:

    __slots__ = "restorer"

    def __init__(self, upscale: int = 2) -> None:
        self.restorer = GFPGANer(
            model_path=(Path(__file__).parent / "data" / "GFPGANCleanv1-NoCE-C2.pth").as_posix(),
            upscale=upscale,
            arch="clean",
            channel_multiplier=2,
            bg_upsampler=None,
        )

    def get_highres_faces(self, img: np.array) -> List[np.array]:
        _, t_restored_faces, _ = self.restorer.enhance(img, has_aligned=False, only_center_face=False, paste_back=False)
        return t_restored_faces

    def process_file(self, img_path: str) -> List[str]:
        try:
            img_ext = img_path.rsplit(".", 1)[1]
        except IndexError as exp:
            print(exp)
            return []

        try:
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        except (FileNotFoundError, ValueError) as exp:
            print(exp)
            return []

        ret = []
        faces_dir = Path(img_path).parent / "faces"
        faces_dir.mkdir(parents=True, exist_ok=True)
        for i, face in enumerate(self.get_highres_faces(img)):
            face_path = (faces_dir / f"face_{i}.{img_ext}").as_posix()
            cv2.imwrite(face_path, face)
            ret.append(face_path)
        return ret

    def process_raw(self, img_raw: bytes) -> List[bytes]:
        try:
            img = np.asarray(Image.open(BytesIO(img_raw)))[..., ::-1]
        except (FileNotFoundError, UnidentifiedImageError, ValueError) as exp:
            print(exp)
            return []

        ret = []
        for face in self.get_highres_faces(img):
            buf = BytesIO()
            Image.fromarray(np.flip(face, axis=-1)).save(buf, format="JPEG")
            ret.append(buf.getvalue())
        return ret
