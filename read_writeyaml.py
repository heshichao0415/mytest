
import yaml
import os
import configpath

path = configpath.getpath()

class MyYaml:
    def __init__(self, name='config.yaml', encoding='utf-8'):
        self.name = name
        self.encoding = encoding


    def ALLYaml(self):
        '''读取yaml里面的所有内容'''
        yamlpath = os.path.join(path, '{}'.format(self.name))
        f = open(yamlpath, encoding=self.encoding)
        data = yaml.load(f, Loader=yaml.FullLoader)
        f.close()
        return data

    @property
    def ALLAPPYaml(self):
        """读取yaml里面的所有内容"""
        APPyamlpath = os.path.join(path, 'ZY', '{}'.format(self.name))
        f = open(APPyamlpath, encoding=self.encoding)
        data = yaml.load(f, Loader=yaml.FullLoader)
        f.close()
        return data


    def config(self, node):
        """config配置信息"""
        return self.ALLYaml()['config'][node]

    def log(self, node):
        """log日志"""
        return self.ALLYaml()['log'][node]

    def mysql(self,node):
        """mysql"""
        return self.ALLYaml()['mysql'][node]

    def sql(self,node):
        """sql"""
        return self.ALLYaml()['sql'][node]

    def baseData(self,node):
        """基础数据"""
        return self.ALLYaml()['data'][node]

    @property
    def interface_data(self):
        """获取接口数据"""
        return self.ALLAPPYaml['interface']

    @property
    def return_keys(self):
        """按顺序返回yaml列表里所有的key，list"""
        return list(self.interface_data.keys())


if __name__ == '__main__':
    # dress = MyYaml().config('url')
    # print(dress)
    a = MyYaml().interface_data
    print(a)





