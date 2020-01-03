# import sys
# sys.path.append('F:\陶士来文件\downloads\PyRTF-0.45\PyRTF-0.45')
# # from PyRTF import *
# with open('test.rtf','rb') as f:
#     for each in f:
#         print(each)
from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter
import re
with open('test2.rtf','rb') as f:
    # for each in f :
    #     each=re.sub('\n','',each)
        doc = Rtf15Reader.read(f,clean_paragraphs=True)
        print(doc)
        print (PlaintextWriter.write(doc,newline="\n").getvalue(),end="")