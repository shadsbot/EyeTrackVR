from dataclasses import dataclass
from typing import Union, Dict
from dacite import from_dict
import os.path
import json


# TODO Who even needs synchronization? (We do.)


@dataclass
class RansacCameraConfig:
    threshold: "int" = 0
    rotation_angle: "int" = 0
    roi_window_x: "int" = 0
    roi_window_y: "int" = 0
    roi_window_w: "int" = 640
    roi_window_h: "int" = 480
    focal_length: "int" = 30
    capture_source: "Union[int, str, None]" = None
    vrc_eye_position_scalar: "int" = 3000
    show_color_image: "bool" = False


@dataclass
class RansacConfig:
    version: "int" = 1
    right_eye: RansacCameraConfig = RansacCameraConfig()
    left_eye: RansacCameraConfig = RansacCameraConfig()

    @staticmethod
    def load():
        if not os.path.exists("ransac_settings.json"):
            print("No settings file, using base settings")
            return RansacConfig()
        with open("ransac_settings.json", "r") as settings_file:
            try:
                config: RansacConfig = from_dict(
                    data_class=RansacConfig, data=json.load(settings_file)
                )
                if config.version != RansacConfig().version:
                    raise RuntimeError(
                        "Configuration does not contain version number, consider invalid"
                    )
                return config
            except:
                print("Configuration invalid, creating new config")
                return RansacConfig()

    def save(self):
        with open("ransac_settings.json", "w+") as settings_file:
            json.dump(obj=self.__dict__, fp=settings_file, default=lambda x: x.__dict__)
