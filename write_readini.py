import configparser
import os
import configpath

path = configpath.getpath()
pathload = os.path.join(path, 'confing.ini')

def write_ini(node='session', child='userKey', content=None):
    """写入ini文件"""
    config = configparser.ConfigParser()
    config.read(pathload, encoding='utf-8')

    try:
        #config.add_section("session") #增加节点
        config.set(node, child, content)
    except configparser.DuplicateSectionError:
        print("ini配置文件写入失败")

    f = open(pathload, "w", encoding='utf-8')
    config.write(f)
    f.close()

def read_ini(node='session', child='token'):
    '''读ini文件'''

    config = configparser.ConfigParser()
    config.read(pathload, encoding='utf-8')
    try:
        connect =config.get(node, child)
        return connect
    except:
        print('error')

if __name__ == '__main__':
    data = read_ini(child='userKey')
    print(data)
    write_ini(content="{'name': '小强', 'mobile': 13718411080}")



