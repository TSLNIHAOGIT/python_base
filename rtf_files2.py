#
#
# import sys
# import os,os.path
# # import comtypes.client
# # from comtypes import  client
#
# from comtypes.client import CreateObject
# wdFormatPDF = 17
#
# input_dir =r'F:\陶士来文件\tsl_python_project\python_base\data_files'
# output_dir =input_dir
#
# for subdir, dirs, files in os.walk(input_dir):
#     for file in files:
#         if file!='关键词纠正.docx':
#             continue
#         print(file)
#         in_file = os.path.join(subdir, file)
#         output_file = file.split('.')[0]
#         out_file = output_dir+output_file+'.pdf'
#         word = CreateObject('Word.Application')
#
#         print('word',word)
#         print(help(word))
#
#         doc = word.Documents.Open(in_file)
#         doc=word.QueryInterface(in_file)
#         doc.SaveAs(out_file, FileFormat=wdFormatPDF)
#         doc.Close()
#         word.Quit()

# encoding:utf-8
import sys
print (sys.getdefaultencoding())


from striprtf.striprtf import rtf_to_text
from striprtf import striprtf
# with open('data_files/test.rtf','rb') as f:
#         data=f.read().decode('g')
#
#         # print(data)
#         rtf = "some rtf encoded string"
#         text = rtf_to_text(data)
#         print(text)


print(help(striprtf))