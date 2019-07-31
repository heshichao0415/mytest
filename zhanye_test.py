import requests
import redis
from write_readini import write_ini
from write_readini import read_ini
from read_writeyaml import MyYaml
import os
from configpath import getpath
path = getpath()
projectName = MyYaml().config('projectName')
matching = MyYaml().config('matching')

# url = "http://twork.zhanye.wallet.openapi.youxin.info:42981"
# urladdress = "http://twork.zhanye.wallet.openapi.youxin.info:42981/v1/access_token"
# payload = {
#             'account': '637A5A9B-13B6-0C9A-D878-A33FE2D988CF',
#             'pass': 'yw2KMlSOXLABj9QZvmG3z8rVDWgunIdx'
#         }
# r = requests.post(urladdress, params=payload)
# result = r.json()
#print(result['token'])
#写入ini文件
# write_ini(node='session', child='tokennn', content=result['token'])


#读取ini文件
# tokk = read_ini(node='session', child='tokennn')
# print(tokk)
# a =  matching.split('_')
# print(a)

#
# moudleName = MyYaml().config('moudleName')
# project_names = os.path.join(path, '{}'.format(projectName))
# # print(project_names)
# dir_list = os.listdir(project_names)
# # print(dir_list)
# moudle_list = []  # 一级目录
# all_import_class = []  # 所有要导入的测试类
# all_moudle = []
#
# if moudleName is None:
#     for i in dir_list:
#         if '.' not in i and '__' not in i:
#             if os.path.exists(project_names + '/{}/__init__.py'.format(i)):
#                 moudle_list.append(i)
#                 # print(moudle_list)
# else:
#     if os.path.exists(project_names + '/{}/__init__.py'.format(moudleName)):
#         moudle_list.append(moudleName)
#         # print(moudle_list)
# for a in moudle_list:
#     dir_name = project_names + '\\' + a
#     # print(dir_name)
#
#     dir_list = os.listdir(dir_name)
#     # print(dir_list)
#     # print(dir_list)
#     for b in dir_list:
#         if matching.split('_')[1] in b:
#             import_name = '{}_{}'.format(b.split('_')[0], a)
#             # print(import_name)
#
#             all_import_class.append('from.{}.{} import {}'.format(a, b.split('.')[0], import_name))
#             # print(all_import_class)
#             # print(all_import_class)
#
#             all_import_class.append('\n')
#
#             all_moudle.append(import_name)
# init_file_py = project_names + '/__init__.py'
#
# # if os.path.exists(init_file_py):          #os.path.exists(init_file_py):判断是否存在文件或目录init_file_py
# #     os.remove(init_file_py)     #os.remove(file):删除一个文件
# all_moudle = str(all_moudle)
# import re
#
# all_moudle = re.sub("'", '', all_moudle)
# # print(all_moudle)
# with open(init_file_py, 'w') as f:
#     f.writelines(all_import_class)
#     f.write('moudle_list = {}'.format(all_moudle))
#     f.write('\n')
#     f.close()
#
# print(all_moudle,moudle_list)
#

# all_moudle, moudle_list = moudle_name()
from ZY import moudle_list
from myloging import Loging
log = Loging()
from models.myunit_per import ReadYaml
from read_writeyaml import MyYaml
from models.MyRedis import Myredis as redis
# redis.all_module(moudle_list)     #存进redis
#创建新线程

dmps = MyYaml().baseData('report_cases')
a = MyYaml().config('ip')
print(a)
print(dmps)