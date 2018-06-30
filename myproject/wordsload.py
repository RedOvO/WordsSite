import json
import pymysql
import random

def loadWords4():
    f = open("CET4_word_list.json", encoding='utf-8')
    dic = json.load(f)
    num = 1
    print('cet4 starts')
    
    for key in dic:
        write = pymysql.connect("localhost", "root", "123456", "myproject", use_unicode=True, charset="utf8")
        Wcursor = write.cursor()
        writeSql = "INSERT INTO myapp_cet4(cet4_num, cet4_word, cet4_describe) " \
                    " VALUES ('%d', '%s', '%s')" %\
                    (num, key, dic[key])
        #print(num)
        try:
            Wcursor.execute(writeSql)
            write.commit()
        except:
            write.rollback()
            write.close()
        num = num + 1
        #print('%s\n%s\n' % (key, dic[key]))

    print('cet4 finished')
    return dic

def loadWords6():
    f = open("CET6_word_list.json", encoding='utf-8')
    dic = json.load(f)
    num = 1
    print('cet6 starts')
    
    for key in dic:
        write = pymysql.connect("localhost", "root", "123456", "myproject", use_unicode=True, charset="utf8")
        Wcursor = write.cursor()
        writeSql = "INSERT INTO myapp_cet6(cet6_num, cet6_word, cet6_describe) " \
                    " VALUES ('%d', '%s', '%s')" %\
                    (num, key, dic[key])
        #print(num)
        try:
            Wcursor.execute(writeSql)
            write.commit()
        except:
            write.rollback()
            write.close()
        num = num + 1
        #print('%s\n%s\n' % (key, dic[key]))
    print('cet6 finished')
    return dic

t = loadWords4()
t = loadWords6()