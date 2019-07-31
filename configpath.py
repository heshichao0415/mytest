import os

def getpath():
    path = os.path.split(os.path.realpath(__file__))[0] #获取根目录路径
    return path

def getload():
    path = os.path.dirname(os.path.realpath(__file__)) #获取当前文件路径的上一级
    return path

if __name__ == '__main__':
    print(getpath())


