from io import BytesIO
from pathlib import Path

import cv2
import numpy as np
import tensorflow as tf
from object_detection.builders import model_builder
from object_detection.utils import config_util
from object_detection.utils import visualization_utils as viz_utils
from PIL import Image


class RubbishClassifier:

    __slots__ = ("clf",)

    def __init__(self) -> None:
        tf.keras.backend.clear_session()
        mobile_net = tf.keras.applications.MobileNet(
            input_shape=(192, 192, 3),
            alpha=1.0,
            depth_multiplier=1,
            dropout=0.001,
            include_top=False,
            weights="imagenet",
            classifier_activation="softmax",
        )

        x = tf.keras.layers.MaxPool2D(pool_size=(2, 2))(mobile_net.output)
        x = tf.keras.layers.Flatten()(x)
        x = tf.keras.layers.Dense(100, activation="sigmoid")(x)
        x = tf.keras.layers.Dense(16, activation="sigmoid")(x)
        x = tf.keras.layers.Dense(2, activation="softmax")(x)

        self.clf = tf.keras.models.Model(mobile_net.input, x)
        self.clf.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
            loss=tf.keras.losses.BinaryCrossentropy(),
            metrics=[tf.keras.metrics.BinaryAccuracy(), tf.keras.metrics.AUC()],
        )
        # TODO путь до весов
        self.clf.load_weights(Path(__file__).parent / "data" / "rubbish_clf" / "rubbish_net_long_train")

    def predict(self, img: np.array) -> tuple:
        """Классификация заполненности"""
        img = cv2.resize(img, dsize=(192, 192), interpolation=cv2.INTER_CUBIC)
        predict = self.clf.predict(np.asarray([img]))
        return max(predict), np.argmax(predict)


class RubbishDetector:
    def __init__(self):

        tf.keras.backend.clear_session()
        num_classes = 1
        pipeline_config = (
            Path(__file__).parent
            / "external"
            / "object_detection/configs/tf2/ssd_resnet50_v1_fpn_640x640_coco17_tpu-8.config"
        )
        # TODO путь до чекпоинта
        checkpoint_path = Path(__file__).parent / "data" / "detector_weights" / "our_detector_ckpt-28-30-31-32-33-34-35"

        configs = config_util.get_configs_from_pipeline_file(pipeline_config)
        model_config = configs["model"]
        model_config.ssd.num_classes = num_classes
        model_config.ssd.freeze_batchnorm = True
        self.detection_model = model_builder.build(model_config=model_config, is_training=True)

        fake_box_predictor = tf.compat.v2.train.Checkpoint(
            _base_tower_layers_for_heads=self.detection_model._box_predictor._base_tower_layers_for_heads,
            _box_prediction_head=self.detection_model._box_predictor._box_prediction_head,
        )
        fake_model = tf.compat.v2.train.Checkpoint(
            _feature_extractor=self.detection_model._feature_extractor, _box_predictor=fake_box_predictor
        )
        ckpt = tf.compat.v2.train.Checkpoint(model=fake_model)
        ckpt.restore(checkpoint_path).expect_partial()
        image, shapes = self.detection_model.preprocess(tf.zeros([1, 640, 640, 3]))
        prediction_dict = self.detection_model.predict(image, shapes)
        _ = self.detection_model.postprocess(prediction_dict, shapes)

    @tf.function
    def detect(self, input_tensor):

        preprocessed_image, shapes = self.detection_model.preprocess(input_tensor)
        prediction_dict = self.detection_model.predict(preprocessed_image, shapes)
        return self.detection_model.postprocess(prediction_dict, shapes)

    def plot_detections(self, image_np, boxes, classes, scores, category_index, figsize=(12, 16), image_name=None):

        image_np_with_annotations = image_np.copy()
        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_annotations,
            boxes,
            classes,
            scores,
            category_index,
            use_normalized_coordinates=True,
            min_score_thresh=0.8,
        )
        return plt.imsave(image_name, image_np_with_annotations)

    def predict(self, path, clf):

        num_classes = 2
        category_index = {1: {"id": 1, "name": "full_trash_can"}, 0: {"id": 0, "name": "empty_trash_can"}}

        img_data = tf.io.gfile.GFile(path, "rb").read()
        image = Image.open(BytesIO(img_data))
        (im_width, im_height) = image.size
        img = np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)
        detections = self.detect(tf.convert_to_tensor(img, dtype=tf.float32))

        answ = []
        score_top = []
        classes = []
        for score, bbox in zip(detections["detection_scores"][0].numpy(), detections["detection_boxes"][0].numpy()):
            if score > 0.8:
                answ.append([bbox])
                score_top.append(score)
                normalize_bbox = [
                    int(bbox[0] * img.shape[0]),
                    int(bbox[1] * img.shape[1]),
                    int(bbox[2] * img.shape[0]),
                    int(bbox[3] * img.shape[1]),
                ]
                classes.append(
                    clf.predict(
                        img[normalize_bbox[0][0] : normalize_bbox[0][2], normalize_bbox[0][1] : normalize_bbox[0][3]]
                    )
                )

        return self.plot_detections(
            test_images_np[i][0],
            np.asarray(answ),
            np.asarray(classes),
            np.asarray(score_top),
            category_index,
            figsize=(30, 20),
        )
