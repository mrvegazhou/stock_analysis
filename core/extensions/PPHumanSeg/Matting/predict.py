# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from paddleseg.cvlibs import manager, Config
from paddleseg.utils import get_sys_env, logger

from .core import predict
from .model import *
from .dataset import MattingDataset
from .transforms import Compose
from .utils import get_image_list


class ArgsObj(object):
    def __init__(self,
                 cfg='./configs/modnet/modnet-mobilenetv2.yml',
                 model_path='./export_model/modnet-mobilenetv2/modnet-mobilenetv2.pdparams',
                 image_path=None,
                 save_dir='./output/results', fg_estimate=True, trimap_path=None):
        self.cfg = cfg
        self.model_path = model_path
        self.image_path = image_path
        self.save_dir = save_dir
        self.fg_estimate = fg_estimate
        self.trimap_path = trimap_path


def main(args: ArgsObj):
    env_info = get_sys_env()
    place = 'gpu' if env_info['Paddle compiled with cuda'] and env_info[
        'GPUs used'] else 'cpu'

    paddle.set_device(place)
    if not args.cfg:
        raise RuntimeError('No configuration file specified.')

    cfg = Config(args.cfg)

    msg = '\n---------------Config Information---------------\n'
    msg += str(cfg)
    msg += '------------------------------------------------'
    logger.info(msg)

    model = cfg.model
    transforms = Compose(cfg.val_transforms)

    image_list, image_dir = get_image_list(args.image_path)
    if args.trimap_path is None:
        trimap_list = None
    else:
        trimap_list, _ = get_image_list(args.trimap_path)
    logger.info('Number of predict images = {}'.format(len(image_list)))

    predict(
        model,
        model_path=args.model_path,
        transforms=transforms,
        image_list=image_list,
        image_dir=image_dir,
        trimap_list=trimap_list,
        save_dir=args.save_dir,
        fg_estimate=args.fg_estimate)


if __name__ == '__main__':
    args = ArgsObj()
    args.cfg = 'configs/modnet/modnet-mobilenetv2.yml'
    args.image_path = 'image1.jpg'
    args.save_dir = './output/results'
    args.model_path = 'export_model/modnet-mobilenetv2/modnet-mobilenetv2.pdparams'
    main(args)
