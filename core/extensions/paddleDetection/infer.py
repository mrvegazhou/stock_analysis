# _*_ coding: utf-8 _*_

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import glob

# add python path of PadleDetection to sys.path
parent_path = os.path.abspath(os.path.join(__file__, *(['..'] * 2)))
sys.path.insert(0, parent_path)


from ppdet.utils.logger import setup_logger
logger = setup_logger('train')

import paddle
from ppdet.core.workspace import load_config, merge_config
from ppdet.engine import Trainer
from ppdet.utils.check import check_gpu, check_npu, check_xpu, check_version, check_config
from ppdet.utils.cli import ArgsParser
from ppdet.slim import build_slim_model


class ArgsObj(object):
    def __init__(self,
                 cfg='./configs/modnet/modnet-mobilenetv2.yml',
                 infer_dir=None,
                 infer_img=None,
                 output_dir='output',
                 draw_threshold=0.5,
                 slim_config=None,
                 use_vdl=False,
                 vdl_log_dir="vdl_log_dir/image",
                 save_results=False
                 ):
        self.cfg = cfg
        self.infer_dir = infer_dir
        self.infer_img = infer_img
        self.draw_threshold = draw_threshold
        self.slim_config = slim_config
        self.use_vdl = use_vdl
        self.vdl_log_dir = vdl_log_dir
        self.save_results = save_results
        self.output_dir = output_dir


def get_test_images(infer_dir, infer_img):
    if infer_img is None or infer_dir is None:
        raise Exception("infer_img or infer_dir should be set")
    if infer_img is None or not os.path.isfile(infer_img):
        raise Exception( "{} is not a file".format(infer_img))
    if infer_dir is None or not os.path.isdir(infer_dir):
        raise Exception("{} is not a directory".format(infer_dir))

    # infer_img has a higher priority
    if infer_img and os.path.isfile(infer_img):
        return [infer_img]

    images = set()
    infer_dir = os.path.abspath(infer_dir)
    if not os.path.isdir(infer_dir):
        raise Exception("infer_dir {} is not a directory".format(infer_dir))

    exts = ['jpg', 'jpeg', 'png', 'bmp']
    exts += [ext.upper() for ext in exts]
    for ext in exts:
        images.update(glob.glob('{}/*.{}'.format(infer_dir, ext)))
    images = list(images)

    if len(images) <= 0:
        raise Exception("no image found in {}".format(infer_dir))

    # logger.info("Found {} inference images in total.".format(len(images)))
    return images


def run(FLAGS: ArgsObj, cfg):
    # build trainer
    trainer = Trainer(cfg, mode='test')

    # load weights
    trainer.load_weights(cfg.weights)

    # get inference images
    images = get_test_images(FLAGS.infer_dir, FLAGS.infer_img)

    # inference
    trainer.predict(
        images,
        draw_threshold=FLAGS.draw_threshold,
        output_dir=FLAGS.output_dir,
        save_results=FLAGS.save_results)

def main():
    FLAGS = ArgsObj()
    cfg = load_config(FLAGS.config)
    cfg['use_vdl'] = FLAGS.use_vdl
    cfg['vdl_log_dir'] = FLAGS.vdl_log_dir
    merge_config(FLAGS.opt)

    # disable npu in config by default
    if 'use_npu' not in cfg:
        cfg.use_npu = False

    # disable xpu in config by default
    if 'use_xpu' not in cfg:
        cfg.use_xpu = False

    if cfg.use_gpu:
        place = paddle.set_device('gpu')
    elif cfg.use_npu:
        place = paddle.set_device('npu')
    elif cfg.use_xpu:
        place = paddle.set_device('xpu')
    else:
        place = paddle.set_device('cpu')

    if 'norm_type' in cfg and cfg['norm_type'] == 'sync_bn' and not cfg.use_gpu:
        cfg['norm_type'] = 'bn'

    if FLAGS.slim_config:
        cfg = build_slim_model(cfg, FLAGS.slim_config, mode='test')

    check_config(cfg)
    check_gpu(cfg.use_gpu)
    check_npu(cfg.use_npu)
    check_xpu(cfg.use_xpu)
    check_version()

    run(FLAGS, cfg)


if __name__ == '__main__':
    main()