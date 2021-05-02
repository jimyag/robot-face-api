# -*- coding: UTF-8 -*-
from enum import Enum, unique


@unique
class ImageType(Enum):
    Base64 = 'BASE64'
    FaceToken = 'FACE_TOKEN'
