import unittest

from super_gradients.training.metrics.detection_metrics import DetectionMetrics

from super_gradients.training import SgModel
from super_gradients.training.datasets import CoCoDetectionDatasetInterface
from super_gradients.training.models.detection_models.yolo_base import YoloPostPredictionCallback


class TestDatasetStatisticsTensorboardLogger(unittest.TestCase):

    def test_dataset_statistics_tensorboard_logger(self):
        """
        ** IMPORTANT NOTE **
        This test is not the usual fail/pass test - it is a visual test. The success criteria is your own visual check
        After launching the test, follow the log the see where was the tensorboard opened. open the tensorboard in your
        browser and make sure the text and plots in the tensorboard are as expected.
        """
        # Create dataset
        dataset_params = {
            "dataset_dir": "/data/coco",
            "batch_size": 64,
            "test_batch_size": 64,
            "num_classes": 80,
            "train_image_size": 320,
            "test_image_size": 224,
            "train_sample_loading_method": "default",
            "test_sample_loading_method": "default"
        }

        dataset = CoCoDetectionDatasetInterface(dataset_params)

        model = SgModel('dataset_statistics_visual_test',
                        model_checkpoints_location='local',
                        post_prediction_callback=YoloPostPredictionCallback())
        model.connect_dataset_interface(dataset, data_loader_num_workers=8)
        model.build_model("yolox_s")

        training_params = {"max_epochs": 1,  # we dont really need the actual training to run
                           "lr_mode": "cosine",
                           "initial_lr": 0.01,
                           "loss": "yolox_loss",
                           "criterion_params":{"strides": [8, 16, 32], "num_cls": 80},
                           "dataset_statistics": True,
                           "launch_tensorboard": True,
                           "valid_metrics_list": [DetectionMetrics(post_prediction_callback=YoloPostPredictionCallback(),
                                                                   num_cls=80)],

                           "loss_logging_items_names": ["GIoU", "obj", "cls", "Loss"],
                           "metric_to_watch": "mAP@0.50:0.95",
                           }
        model.train(training_params=training_params)


if __name__ == '__main__':
    unittest.main()
