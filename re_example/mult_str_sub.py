import re
def multiple_replace(text, adict):
     rx = re.compile('|'.join(map(re.escape, adict)))
     print('rx:',rx)

     def one_xlat(match):
           print('match:', match.group(0))
           print('adict:',adict[match.group(0)])
           return adict[match.group(0)]
     return rx.sub(one_xlat, text)

if __name__=='__main__':
    text='i and you like dogs'
    dicts={'i':'III','dogs':'ddddd'}
    print(multiple_replace(text,dicts))