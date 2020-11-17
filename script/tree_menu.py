#!/usr/bin/env python

#三级菜单

dic = {'jiadian': {'tv': {'xiaomi': 3999, 'letv': 4299},
                     'kongtiao': {'geli': 8999, 'hair': 6000},
                     'bingxinag': {'media': 5099, 'ximenzi': 4599}},
        '3C': {'computer': {'dell': 6888, 'mac air': 8009},
               'phone': {'mi5': 1999, 'iPhone6': 5299}},
        'live': {'shoes': {'NIKE': 899, 'anta': 399},
                'Txue': {'senma': 89, 'levis': 75}}}
dic_key = {}

def menu1():
    print('one menu')
    for index1,key1 in enumerate(dic.keys(),1):
        print(index1,key1)
        dic_key[str(index1)] = key1
    #print(dic_key)
    choose = raw_input("please choose one menu,input b is return,input q is quit:")
    if choose == 'q':quit()
    elif choose == 'b':
        print("one menu can't return")
    elif dic_key.get(choose):
        menu2(dic_key[choose])
    else:
        print("input error ,please input")
def menu2(choose1):
    print('two menu')
    for index2,key2 in enumerate(dic[choose1].keys(),1):
        print(index2,key2)
        dic_key[str(index2)] = key2
   # print(dic_key)
    choose2 = raw_input("please choose two menu,input b is return,input q is quit:")
    if choose2 == 'q':quit()
    elif choose2 == 'b':
        menu1()
    elif dic_key.get(choose2):
        menu3(choose1,dic_key[choose2])
    else:
        print("input error ,please input")

def menu3(choose1,choose2):
    print('three menu')
    for index3, key3 in enumerate(dic[choose1][choose2].keys(), 1):
        print(index3, key3)
        dic_key[str(index3)] = key3
    choose3 = raw_input("please choose three menu,input b is return,input q is quit:")
    if choose3 == 'q':
        quit()
    elif choose3 == 'b':
        menu2(choose1)
    elif dic_key.get(choose3):
        print dic_key[choose3],':',dic[choose1][choose2][dic_key[choose3]]
    else:
        print("input error ,please input")


menu1()
