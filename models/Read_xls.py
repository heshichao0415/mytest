import os
from configpath import getpath
from xlrd import open_workbook
import openpyxl


class Case:
    def __init__(self):
        self.case_id = None
        self.case_name = None
        self.method = None
        self.url = None
        self.data = None
        self.expected = None
        self.actual = None
        self.result = None
        self.sql = None


# class readExcel():
#     def get_xls(self, xls_name, sheet_name):
#         cls = []
#         xlsPath = os.path.join(getpath(), "Case_data", xls_name)
#         file = open_workbook(xlsPath, 'r')
#         sheet = file.sheet_by_name(sheet_name)
#         rows = sheet.nrows
#         for i in range(rows):
#             if sheet.row_values(i)[0] != 'case_id':
#                 cls.append(sheet.row_values(i))
#         return cls

class readExcel():
    def get_xls(self, xls_name, sheet_name):
        cases = []
        xlspath = os.path.join(getpath(), "Case_data", xls_name)
        file = openpyxl.load_workbook(xlspath)
        sheet = file[sheet_name]
        rows = sheet.max_row
        for i in range(2, rows+1):
            case = Case()
            case_id = sheet.cell(row=i, column=1).value
            case_name = sheet.cell(row=i, column=2).value
            case_method = sheet.cell(row=i, column=3).value
            case_url = sheet.cell(row=i, column=4).value
            case_datas = sheet.cell(row=i, column=5).value
            case_expected = sheet.cell(row=i, column=6).value
            case.id = case_id
            case.name = case_name
            case.method = case_method
            case.url = case_url
            case.datas = case_datas
            case.expected = case_expected
            cases.append(case)
        file.close()
        return cases
if __name__ == "__main__":
    readExcel().get_xls('case_xy_huawei.xlsx', 'Sheet1')