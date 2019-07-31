from read_writeyaml import MyYaml
from write_readini import read_ini

class ReadYaml(object):
    def __init__(self, className=None, case_info=None):
        self.className = className
        self.case_info = case_info

    def return_data(self):
        try:
            token = read_ini(node='session', child='token')  #从配置文件获取token
            # print(token)
        except Exception:
            token = '0'
        headers = {'token': token}
        key = self.className.split('_')[1]
        datas = MyYaml().interface_data[key]
        data = []
        for i in datas:
            if i['className'] == self.className:
                data.append(i['url'])   # 0
                for j in i['funName']:
                    for k in j.keys():
                        if k == self.case_info:
                            data.append(j[self.case_info]['bar'])   #参数   1
                            data.append(j[self.case_info]['result'])  #预期结果  2
                            data.append(j[self.case_info]['test_data'])  #预期结果  3
                            # print(data[0],data[1],data[2],data[3])
        return token, headers, data

    def case_id(self, className):
        case_ids = []
        for a, b in MyYaml().interface_data.items():
            for c in b:
                if c['className'] in className:
                    for d in c['funName']:
                        for e, f in d.items():
                            case_ids.append(e)
        return case_ids      #方法名

    def case_data(self, className_list):
        all_fun_data = []  #所有测试用例的数据
        for a, b in MyYaml().interface_data.items():   #返回一个元组对列表 items()
            for c in b:
                if c['className'] in className_list:
                    for d in c['funName']:
                        for e, f in d.items():
                            f['url'] = c['url']
                            if {e: f} not in all_fun_data:
                                all_fun_data.append({e: f})
        return all_fun_data

    def case_info_data(self, className_list):    #用例方法的数据
        all_info = []
        for case in self.case_data(className_list):
            for case_id, case_in in case.items():
                all_info.append((case_id, case_in))
                # print(all_info)
        return all_info

    def return_module(self, module_all, module):
        modle_list = []
        for i in module_all:
            if str(i) in module:
                modle_list.append(i)
        return modle_list

if __name__ == '__main__':
    a = ReadYaml('QBInterface_auth', 'test_login_token')
    a.return_data()
    # a.case_id('QBInterface_auth')
    a.case_data('QBInterface_auth')
    a.case_info_data('QBInterface_auth')





