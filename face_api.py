# -*- coding: UTF-8 -*-
from typing import Dict, List, Any, Union
from aip import AipFace
import base64
import config
from image_type import ImageType


# 传入照片路径 获得照片的base64值
def get_img(file_path):
    with open(file_path, 'rb') as f:
        base64_img = base64.b64encode(f.read())
    image = str(base64_img, encoding='utf-8')
    return image


class BaiduFace:
    def __init__(self):
        self.GROUP_ID = 'service_robot'
        self.client = AipFace(config.AppId, config.APIKey, config.SecretKey)

    def match(self, image1: str, image2: str, image1_type: ImageType = ImageType.Base64,
              image2_type: ImageType = ImageType.Base64):
        """
        传入两张人脸图片,匹配相似度 相似度大于80可以判断为同一个人
        返回结果的例子 face_token顺序按照传入照片的顺序
        如果错误码不为0则result为None
        {'error_code': 0,
        'result':
            {'score': 17.1104126,
            'face_list':
                [
                {'face_token': '5b1ee95d6bba363db862b771757b203f'},
                {'face_token': 'e305242a96ddc0f0ebb2bc19353ea70e'}
                ]
            }
        }
        """
        images: List[Dict[str, Union[str, Any]]] = [
            {'image': image1, 'image_type': image1_type},
            {'image': image2, 'image_type': image2_type}
        ]

        return self.client.match(images)

    def search(self, image: str, image_type: str = ImageType.Base64):
        """
        1比N的匹配，用人脸信息在用户组中匹配
        如果错误码不为0则result为None
        返回的结果如下：
        {'error_code': 0,
        'result':
            {'face_token': '957cdb6a03f998b304d83a317a014818',
            'user_list':
                [{'group_id': 'service_robot',
                'user_id':
                'Taylor_Swift',
                'user_info': '',
                'score': 100
                }]
            }
        }
        """
        search_result = self.client.search(image, image_type, self.GROUP_ID)
        result = {'error_code': search_result['error_code'], 'result': search_result['result']}
        return result

    def add_user(self, image: str, use_id: str, image_type: str = ImageType.Base64) -> dict:
        """
        添加用户至用户组，如果用户已经存在，则将用户的人脸信息添加到用户人脸库中
        返回的结果的例子：
        如果错误码不为0则result为None
        {
            'error_code': 0,
            'result':
                {
                    'face_token': '957cdb6a03f998b304d83a317a014818',
                    'location':
                        {
                            'left': 70.89,
                            'top': 58.46,
                            'width': 71,
                            'height': 69,
                            'rotation': 1
                        }
                }
        }
        """
        add_result = self.client.addUser(image, image_type, self.GROUP_ID, use_id)
        result = {'error_code': add_result['error_code'], 'result': add_result['result']}
        return result

    def image_info(self, image: str, image_type: str = ImageType.Base64) -> dict:
        """
        传入一张人脸信息默认获取照片中人的年龄、性别、情绪
        如果错误码不为0则result为None
        {
            'error_code': 0,
            'result':
                {
                    'face_num': 1,
                    'face_list':
                    [
                    {
                        'face_token': 'c0cf63842720dd966421a7fe719e5f7e',
                        'location':{'left': 313.76,'top': 477.84,'width': 414,'height': 417,'rotation': -3},
                        'face_probability': 1,
                        'angle':
                            {'yaw': -8.25,'pitch': 10.36,'roll': -4.63},
                        'age': 24,
                        'gender':
                            {'type': 'male', 'probability': 1},
                        'emotion': {'type': 'happy', 'probability': 0.94}
                    }
                    ]
                }
        }
        """
        options = {"face_field": "age,gender,emotion"}
        detect_result = self.client.detect(image, image_type, options=options)
        result: Dict[str, str] = {'error_code': detect_result['error_code'], 'result': detect_result['result']}
        return result

    def add_group(self, group_id: str) -> bool:
        """
        添加用户组
        添加成功返回True 否则返回False
        """
        result = self.client.groupAdd(group_id)
        if result['error_code'] == 0:
            self.GROUP_ID = group_id
            return True
        else:
            return False

    def multi_search(self, image: str, image_type: ImageType = ImageType.Base64, max_face_num: int = 1) -> dict:
        """
        M比N的匹配
        默认是1比N
        {
            "error_code": 0,
            "result": {
            "face_num": 2,
            "face_list": [{"face_token": "6fe19a6ee0c4233db9b5bba4dc2b9233",
                            "location": {"left": 31.95568085,"top": 120.3764267,"width": 87,"height": 85,"rotation": -5},
                            "user_list": [{"group_id": "group1","user_id": "5abd24fd062e49bfa906b257ec40d284","user_info": "userinfo1","score": 69.85684967041},
                                          {"group_id": "group1","user_id": "2abf89cffb31473a9948268fde9e1c3f","user_info": "userinfo2","score": 66.586112976074
                                          }]
                          },
                          {"face_token": "fde61e9c074f48cf2bbb319e42634f41",
                          "location": {"left": 219.4467773,"top": 104.7486954,"width": 81,"height": 77,"rotation": 3},
                          "user_list": [{"group_id": "group1","user_id": "088717532b094c3990755e91250adf7d","user_info": "userinfo","score": 65.154159545898
                                         }]
                          }]
                    }
        }
        """
        options = {"max_face_num": max_face_num}
        result = self.client.multiSearch(image, image_type, self.GROUP_ID, options)
        result = {'error_code': result['error_code'], 'result': result['result']}
        return result
