# encoding: utf-8
import time
import os
import numpy as np
import multiprocessing as mp
import threading
import math
import config
import torch
import torch.nn as nn
from skimage import io, img_as_ubyte
from urllib import parse, request
import cv2
from concurrent.futures import ProcessPoolExecutor, as_completed  # 线程池
from app_logging import logger
from core.ocr_detection import ocr_cv
from core.ocr_files_class import file_class, img_class_sencod
from core.ocr_recognization import eng_recog
from core.ocr_recognization.ocr_bbox_content import extract_sentence
from core.ocr_recognization import crnn, alphabets
from core.ocr_detection import ocr_rotation
from . import rotation_content_judg
import asyncio
import logging
from socket import error as SocketError
import errno
__all__ = ('image_deal',)

# crnn_model_path = './models/crnn_Rec_done_99.pth'
# alphabet = alphabets.alphabet
# nclass = len(alphabet) + 1
# # crnn network
# model = crnn.CRNN(32, 1, nclass, 256)
# if torch.cuda.is_available() and config.IS_USE_CUDA:
#     model = model.cuda()
#     # 导入已经训练好的crnn模型
#     # # GPU
#     model.load_state_dict(torch.load(crnn_model_path))
#     if torch.cuda.device_count() > 1:
#         model = nn.DataParallel(model)
# # # CPU
# else:
#     model.load_state_dict(torch.load(crnn_model_path, map_location='cpu'))
#     logger.info('CRNN model loaded.')
#global set_method
#set_method=True
if not (torch.cuda.is_available() and config.IS_USE_CUDA):
  crnn_model_path = './models/crnn_Rec_done_99.pth'
  alphabet = alphabets.alphabet
  nclass = len(alphabet) + 1
  # crnn network
  model = crnn.CRNN(32, 1, nclass, 256)
  model.load_state_dict(torch.load(crnn_model_path, map_location='cpu'))
  logger.info('CRNN model loaded.')
else:
  logger.info('will CRNN model loaded with gpu.')

def load_model_with_cuda():
   crnn_model_path = './models/crnn_Rec_done_99.pth'
   alphabet = alphabets.alphabet
   nclass = len(alphabet) + 1
   # crnn network
   model = crnn.CRNN(32, 1, nclass, 256)
   #if torch.cuda.is_available() and config.IS_USE_CUDA:
   model = model.cuda()
   # 导入已经训练好的crnn模型
   # # GPU
   model.load_state_dict(torch.load(crnn_model_path))
   if torch.cuda.device_count() > 1:
      model = nn.DataParallel(model)
   return model


def image_deal(self):
    start_time = time.time()
    # 区域检测
    detection(self)
    logger.info('[ticket:%s] detection_list_len: %d' % (self.ticket, len(self.detection_list)))
    # 区域文字识别
    result_e, result_c = recognization(self)
    cost_time = time.time() - start_time
    # with open('./data/merge_content_test/result_e.txt', 'r', encoding='utf8') as f:
    #     result_e = eval(f.read())
    # with open('./data/merge_content_test/result_c.txt', 'r', encoding='utf8') as f:
    #     result_c = eval(f.read())
    # 将识别的内容按照pdf页码的顺序进行重排,从旋转90和270中的内容中选一个
    result_e = result_rearrange(result_e)
    result_c = result_rearrange(result_c)
    logger.info('[ticket:%s] detection and recognization finished. image number:%s, time cost:%ss' % (self.ticket, self.slice_num, round(cost_time, 3)))
    return result_e, result_c


# 图片文字区域检测
def detection(self):
    start_time = time.time()
    if self.data_dir:
        save_dir = self.data_dir + '/detect_image'
        # if os.path.exists(save_dir):
        #     shutil.rmtree(save_dir)
        # if os.path.exists(self.data_dir):
        #     os.mkdir(save_dir)
        if not os.path.exists(save_dir) and os.path.exists(self.data_dir):
            os.mkdir(save_dir)
    else:
        save_dir = ''
    # 以url集合的方式处理图片
    if self.img_data_dir:
        logger.info('[ticket:%s] detection start. by url...' % (self.ticket))
        for i in self.img_data_dir:
            img_url = i.get('path', '')
            suffix = img_url.split('.')[-1]
            if suffix not in ['jpg', 'png', 'jpeg']:
                continue
            # 读取图片
            try:
                # start_time = time.time()
                # logger.info('[ticket:%s] %s read image start.' % (self.ticket, img_url))
                image_path = parse.quote(img_url, encoding='utf8').replace('%3A', ':')
                resp = request.urlopen(image_path)
                img = np.asarray(bytearray(resp.read()), dtype="uint8")
                img = cv2.imdecode(img, cv2.IMREAD_COLOR)
                # logger.info('[ticket:%s] %s read image end.time cost:%ss' % (self.ticket, image_path, round(time.time() - start_time, 3)))
            except Exception as e:
                logger.warning('[ticket:%s] %s error' % (self.ticket, image_path))
                logger.warning(e)
            # 判断图片是否需要旋转
            if not ocr_rotation.detect_rotation(img, 127):
                logger.info('[ticket:%s] %s 旋转图片.' % (self.ticket, img_url))
                # 旋转90度，并进行文本检测
                img_90 = np.rot90(img)
                detection_image(self, img_90, save_dir, i=i, rotation_angle=90)
                # 旋转270度，并进行文本检测
                img_270 = np.rot90(img, 3)
                detection_image(self, img_270, save_dir, i=i, rotation_angle=270)
                detection_image(self, img, save_dir, i=i, rotation_angle=0)
            else:
                # 图片文本检测和表格检测
                detection_image(self, img, save_dir, i=i, rotation_angle=0)
    # 处理本地图片
    elif not self.ocr_data_files and os.path.exists(r'%s/' % self.data_dir):
        # we store unzipped images in company_name's temporary directory
        logger.info('[ticket:%s] detection start. by local path. data_dir:%s' % (self.ticket, self.data_dir))
        for file in sorted(os.listdir(r'%s/' % self.data_dir), key=lambda x: x):
            if os.path.isdir((r'%s/' % self.data_dir) + file):
                for im in sorted(os.listdir((r'%s/' % self.data_dir) + file), key=lambda x: x):
                    suffix = im.split('.')[-1]
                    if suffix not in ['jpg', 'png', 'jpeg']:
                        continue
                    # 读图片
                    image_path = r'%s/%s/%s' % (self.data_dir, file, im)
                    img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
                    # 判断图片是否需要旋转
                    if not ocr_rotation.detect_rotation(img, 127):
                        logger.info('[ticket:%s] %s 旋转图片.' % (self.ticket, image_path))
                        # 旋转90度，并进行文本检测
                        img_90 = np.rot90(img)
                        detection_image(self, img_90, save_dir, rotation_angle=90, file=file, type='path')
                        # 旋转270度，并进行文本检测
                        img_270 = np.rot90(img, 3)
                        detection_image(self, img_270, save_dir, rotation_angle=270, file=file, type='path')
                        detection_image(self, img, save_dir, rotation_angle=0, file=file, type='path')
                    else:
                        # 图片文本检测和表格检测
                        detection_image(self, img, save_dir, rotation_angle=0, file=file, type='path')

    logger.info('[ticket:%s] detection finished. time cost:%ss' % (self.ticket, round(time.time() - start_time, 3)))


def sub_loop(each_params_list,model):
  # print('each_num_list',each_num_list)
  log = logging.getLogger('run_subloop')
  log.info('go sub_loop')

  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  tasks = []
  for param_e in each_params_list:
    if bool(model):
       param_e['model']=model
    tasks.append(recog_box2word(param_e))

  # tasks_e = [recog_box2word(param_e) for param_e in each_params_list]
  # tasks_c = [recog_box2word(**param_c) for param_c in each_params_list_c]

  # tasks.extend(tasks_e)
  # tasks.extend(tasks_c)
  ##最后结果返回的是二维列表，里面每个小列表都是一个进程对应的一组任务，每组任务的顺序是按照task提交顺序返回的
  ##该组任务，必须完成之后才能继续做下面的，且该组任务只能有一个进程控制
  ##返回结果好像是按照调用的顺序的
  results = loop.run_until_complete(asyncio.gather(*tasks))
  return results

async def run(executor, params_list=None):

    if torch.cuda.is_available() and config.IS_USE_CUDA:
         s_t=time.time()
         model = load_model_with_cuda()
         print('model load time',time.time()-s_t)
    else:
        model=None
    log = logging.getLogger('run_blocking_tasks')
    log.info('starting')
    log.info('creating executor tasks')
    loop = asyncio.get_event_loop()
    # url = 'http://127.0.0.1:5000'
    # urls = [url for _ in range(100)]
    # print('excutor',executor)
    results = await loop.run_in_executor(executor, sub_loop, params_list,model)

    # await asyncio.get_event_loop().run_in_executor(executor, sub_loop,urls)
    # results = [t.result() for t in completed]
    # log.info('results: {!r}'.format(results))
    # print('gogo')
    return results


def chunks(list_num, size):
  n = math.ceil(len(list_num) / size)

  for i in range(0, len(list_num), n):
    yield list_num[i:i + n]
# 区域文字识别，分别使用tesseract和“中文识别模型”
def recognization(self):
    # max_workers = (os.cpu_count() - 2) if os.cpu_count() < config.THREADS_NUMBER else config.THREADS_NUMBER
    max_workers = (os.cpu_count() ) if os.cpu_count() < config.THREADS_NUMBER else config.THREADS_NUMBER

    logger.info('[ticket:%s] recognization start. max_workers:%s' % (self.ticket, max_workers))
    start_time = time.time()
    result_e = {}
    result_c = {}
    # lock = threading.Lock()
    # 多线程
    if self.parallel == 1:
        # 构建线程池, 线程池默认线程是cpu核数*5， (os.cpu_count() or 1)*5
          if torch.cuda.is_available() and config.IS_USE_CUDA :#and set_method:
             #mp.set_start_method('spawn')
             try:
                mp.set_start_method('spawn')
                #set_method=False
             except RuntimeError:
                pass
          with ProcessPoolExecutor(max_workers=max_workers) as recog_executor:
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            event_loop = asyncio.get_event_loop()
            try:

              ss = time.time()
              # all_task_e = []
              # all_task_c = []
              all_task_params_e = []
              all_task_params_c = []
              all_task_params_groups=[]




              ##获取中文和英文模型所需参数的列表
              for i in range(len(self.detection_list)):
                  d = self.detection_list[i]
                  img_name = d['img_name']
                  use_model = [i[1] for i in self.rd.chi_tra if img_name == i[0]]
                  use_model = use_model[0] if use_model else ''
                  # 创建英文任务参数列表
                  if use_model in ('', 'english'):

                      param_e = {'self': self, 'd': d, 'i': i, 'type': 'english', 'use_model': use_model}
                      # english = recog_executor.submit(recog_box2word, (param_e))
                      all_task_params_e.append(param_e)
                  # 创建中文任务参数列表
                  if use_model in ('', 'chinese', 'chi_tra', 'chi_sim'):
                      param_c = {'self': self, 'd': d, 'i': i, 'type': 'chinese',  'use_model': use_model}
                      # chinese = recog_executor.submit(recog_box2word, (param_c))
                      all_task_params_c.append(param_c)

              ##要将任务分组，让每个进程得到几乎均等的任务，并行的进行计算；此处将参数列表进行分组
              # url = 'http://127.0.0.1:5000'
              # all_urls = [url for _ in range(100)]
              ##要加判断两个模型参数都存在的时候才能调用

              len_e=len(all_task_params_e)
              len_c=len(all_task_params_c)
              if len_e>0:
                 all_task_params_groups.extend(chunks(all_task_params_e,recog_executor._max_workers))
              if len_c>0:
                all_task_params_groups.extend(chunks(all_task_params_c,recog_executor._max_workers))

              #if torch.cuda.is_available() and config.IS_USE_CUDA:
              #  if len_e>0:
              #    all_task_params_groups.extend(chunks(all_task_params_e,recog_executor._max_workers))
              #  if len_c>0:
              #    all_task_params_groups.extend(chunks(all_task_params_c,recog_executor._max_workers))
              #else:
              #  if len_e > 0:
              #    all_task_params_groups.extend(chunks(all_task_params_e, len_e/recog_executor._max_workers))
              #  if len_c > 0:
              #    all_task_params_groups.extend(chunks(all_task_params_c, len_c/recog_executor._max_workers))

              tasks = [run(recog_executor, chunked) for chunked in
                       all_task_params_groups]



              res = event_loop.run_until_complete(asyncio.gather(*tasks))
              #将二维列表变成一维列表
              res=sum(res,[])

              logger.info('{} workers cost time final {} s'.format(recog_executor._max_workers, time.time() - ss))
              #print('{} workers cost time final'.format(recog_executor._max_workers), time.time() - ss)
              # print

              # 获取英文任务的执行结果
              for index_e,e in enumerate(res[0:len_e]):
                   result_e[str(index_e)] = e

              # 获取中文任务的执行结果
              for index_c,c in enumerate(res[len_e:]):
                   result_c[str(index_c)] = c
            except Exception as e:
              logger.info('exception err',e,e.errno)
              if e.errno != errno.ECONNRESET:
                raise
              pass
            finally:
              event_loop.close()


    # 单线程
    else:
        for i in range(len(self.detection_list)):
            d = self.detection_list[i]
            img_name = d['img_name']
            use_model = [i[1] for i in self.rd.chi_tra if img_name == i[0]]
            use_model = use_model[0] if use_model else ''
            # 英文模型识别
            if use_model in ('', 'english'):
                param_e = {'self': self, 'd': d, 'i': i, 'type': 'english', 'use_model': use_model}
                try:
                    data_e = recog_box2word(param_e)
                    if data_e:
                        result_e[str(i)] = data_e
                except Exception as e:
                    logger.info('[ticket:%s] ocr_read_image. %s ' % (self.ticket, e))
            # 中文模型识别
            if use_model in ('', 'chinese', 'chi_tra', 'chi_sim'):
                param_c = {'self': self, 'd': d, 'i': i, 'type': 'chinese', 'use_model': use_model}
                try:
                    data_c = recog_box2word(param_c)
                    if data_c:
                        result_c[str(i)] = data_c
                except Exception as e:
                    logger.info('[ticket:%s] ocr_read_image. %s ' % (self.ticket, e))
    if img_class_sencod(self):
        result_class_sencod(self, result_e)
        result_class_sencod(self, result_c)
    if self.data_dir and os.path.exists(self.data_dir):
        logger.info('[ticket:%s] 写文件recoged_result.txt' % (self.ticket))
        write_content = {'result_e': result_e, 'result_c': result_c}
        with open('%s/recoged_result.txt' % self.data_dir, 'w', encoding='utf8') as f:
            f.write(str(write_content) + '\n')
    logger.info('[ticket:%s] recognization finished. time cost:%ss' % (self.ticket, round(time.time() - start_time, 3)))
    return result_e, result_c


def result_class_sencod(self, result):
    for i, r in result.items():
        img_url = r['img_url']
        img_name = r['img_name']
        img_name_1 = self.img_url_class[img_url]
        if img_name != img_name_1:
            r['img_name'] = img_name_1
            # result[str(i)]['img_name'] = img_name_1
    # return result


async def recog_box2word(param):
    # model=load_model_with_cuda()
    #global model
    if not  (torch.cuda.is_available() and config.IS_USE_CUDA):
      global model
      model = model
    else:
      model = param['model']
    self = param['self']
    d = param['d']
    type = param['type']
    use_model = param['use_model']
    if use_model:
        type = use_model
    img_name = d['img_name']
    # lock = param['lock']
    logger.info('[ticket:%s] %s %s %s model start.' % (self.ticket, d['img_name'], d['img_url'], type))
    start_time = time.time()
    img_gray = d['img_gray']
    detectied_region = d['detectied_region']
    table_bbox = d['table_bbox']
    point_sets = d['point_sets']
    tmp = {}
    # lock.acquire()  # 获取锁
    recoged_result = eng_recog.box2word(img_gray, detectied_region, model, type, img_name)
    recoged_result = y_axis_deviation_deal(recoged_result)
    # lock.release()  # 释放锁
    tmp['img_url'] = d['img_url']
    tmp['rotation_angle'] = d['rotation_angle']

    # 文件分类， 只有“其他文件”和“打包文件”入口的文件才需要进行分类，
    # 且当“合同”、“发票”，“箱单”，“运单”，“申报要素”，“入库单”等入口有对应文件时，
    # 舍弃掉“其他文件”和“打包文件”入口对应的文件
    if img_name in ('other_files', 'package_upload'):
        # class_time = time.time()
        # lock.acquire()
        img_name_new = file_class(recoged_result, self.rd, self.img_url_class, d['img_url'], img_name)
        logger.info('[ticket:%s] 文件分类.origin:%s,new:%s' % (self.ticket, img_name, img_name_new))
        # lock.release()
        if img_name_new not in ('other_files', 'package_upload') and img_name_new in self.source_list:
            tmp = {}
        elif not recoged_result:  # recoged_result的内容为空
            tmp = {}
        else:
            tmp['img_name'] = img_name_new
            # result[str(i)] = tmp
    else:
        tmp['img_name'] = d['img_name']
    if recoged_result:
        recoged_result = extract_sentence(table_bbox, recoged_result, d['img_gray'], tmp['img_name'])
    tmp['recoged_result'] = recoged_result
    tmp['id'] = d.get('id', '')
    tmp['page'] = d.get('page', '')
    tmp['table_bbox'] = table_bbox
    tmp['point_sets'] = point_sets
    logger.info('[ticket:%s] %s %s %s model end.time cost:%ss' % (self.ticket, img_name, d['img_url'], type, round(time.time() - start_time, 3)))
    return tmp if tmp else None


# y轴偏差处理， y相差2-3个距离时，进行统一
def y_axis_deviation_deal(DL):
    DL_sorted = sorted(DL, key=lambda x: x[2])
    DL_mask = [0 for _ in range(len(DL_sorted))]
    for i in range(len(DL_sorted)):
        DL_i = DL_sorted[i]
        for j in range(i + 1, len(DL_sorted)):
            DL_j = DL_sorted[j]
            if DL_j[2] - DL_j[2] > 30:
                break
            elif DL_mask[j] == 1:
                continue
            elif 0 < abs(DL_i[2] - DL_j[2]) < 10:
                y_offset = DL_j[2] - DL_i[2]
                DL_sorted[j][2] -= y_offset
                DL_mask[j] == 1
    return DL_sorted


def result_rearrange(result):
    try:
        pdf_id_dict = {}
        for i, r in result.items():
            img_url = r['img_url']
            pdf_id = r.get('id', 'pdf_id_default')
            page = r.get('page', 0)
            if str(page).strip() == '':
                page = 0
            if pdf_id in pdf_id_dict:
                if img_url in pdf_id_dict[pdf_id]:
                    pdf_id_dict[pdf_id][img_url]['index_list'].append(i)

                else:
                    pdf_id_dict[pdf_id][img_url] = {'index_list': [i], "page": page}
            else:
                pdf_id_dict[pdf_id] = {img_url: {"index_list": [i], "page": page}}

        result_new = {}
        for pdf_id, values in pdf_id_dict.items():
            # 将识别的内容按照pdf页码的顺序进行重排
            for im_url, v in sorted(values.items(), key=lambda x: int(x[1]['page'])):
                index_list = v['index_list']
                # 从旋转90和270,0中的内容中选一个
                if len(index_list) == 3:
                    index_0 = [i for i in index_list
                               if result[str(i)].get('rotation_angle', None) == 0][0]
                    index_90 = [i for i in index_list
                                if result[str(i)].get('rotation_angle', None) == 90][0]
                    index_270 = [i for i in index_list
                                 if result[str(i)].get('rotation_angle', None) == 270][0]
                    _, rotation_angle = \
                        rotation_content_judg.content_judgment_three(result[str(index_0)]['recoged_result'],
                                                                     result[str(index_90)]['recoged_result'],
                                                                     result[str(index_270)]['recoged_result'])
                    if rotation_angle == 0:
                        index = index_0
                    elif rotation_angle == 90:
                        index = index_90
                    else:
                        index = index_270
                else:
                    index = index_list[0]
                result_new[str(index)] = result[str(index)]
        return result_new
    except Exception as e:
        logger.info(e)
        return result


def detection_image(self, img, save_dir, rotation_angle, i=None, file=None, type='url'):
    if type == 'url':
        source = i.get('type', '')
        img_url = i.get('path', '')
        img_time = time.time()
        logger.info('[ticket:%s] %s %s detection start.' % (self.ticket, source, img_url))
        detectied_region, img_gray, table_bbox, point_sets = ocr_cv.detect_word(img, img_url, 'url', self.ticket, companyName=self.companyName, source=source, data_dir=save_dir)
        logger.info('[ticket:%s] %s %s detection end. time cost:%ss' % (self.ticket, source, img_url, round(time.time() - img_time, 3)))
        tmp = {}
        tmp['rotation_angle'] = rotation_angle
        tmp['detectied_region'] = detectied_region
        tmp['img_gray'] = img_gray
        tmp['img_name'] = source
        tmp['img_url'] = img_url
        tmp['id'] = i.get('id', '')
        tmp['page'] = i.get('page', '')
        tmp['table_bbox'] = table_bbox
        tmp['point_sets'] = point_sets
        self.detection_list.append(tmp)
    else:
        img_path = r'%s/%s/%s' % (self.data_dir, file, img)
        tmp_img_path = '%s/%s' % (file, img)
        detectied_region, img_gray, table_bbox, point_sets = ocr_cv.detect_word(img, img_path, data_dir=save_dir)
        tmp = {}
        tmp['rotation_angle'] = rotation_angle
        tmp['detectied_region'] = detectied_region
        tmp['img_gray'] = img_gray
        tmp['img_name'] = file
        tmp['img_url'] = ''
        tmp['id'] = ''
        tmp['page'] = ''
        tmp['table_bbox'] = table_bbox
        tmp['point_sets'] = point_sets
        self.detection_list.append(tmp)

