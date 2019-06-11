
import thulac
thu1 = thulac.thulac() #默认模式
text = thu1.cut("我爱北京天安门", text=True)
print(text)



thu1 = thulac.thulac(seg_only=True) #只进行分词，不进行词性标注
text = thu1.cut("我爱北京天安门", text=True)
print(text)

# thu1.cut_f("input.txt", "output.txt") #对input.txt文件内容进行分词，输出到output.txt