# -*- coding: utf-8 -*- 


asd = [None, None, None, [1], [2]]

for i in asd[:]:
    if i is not None:
        print i
    else:
        asd.remove(i)
print asd


#print filter(bool, [None, None, None, [1]])