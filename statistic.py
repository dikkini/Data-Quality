#-*- coding: utf8 -*-
import shelve
import logging
logging.basicConfig(filename='file.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

class stats():
    def __init__(self, schema, table):
        self.schema = schema
        self.table = table
        #self.using_params = using_params
        
    def take_main_stat(self, date):
        key = str(date)
        filename = './data/%s_%s_main_stat.dat' % (self.schema, self.table)
        d = shelve.open(filename)
        data = d[key]
        d.close()
        return data
    
    def take_ext_stat(self, date):
        key = str(date)
        filename = './data/%s_%s_ext_stat.dat' % (self.schema, self.table)
        d = shelve.open(filename)
        data = d[key]
        d.close()
        return data
    
    def add_main_stat(self, date, data):
        key = str(date)
        filename = './data/%s_%s_main_stat.dat' % (self.schema, self.table)
        d = shelve.open(filename)
        d[key] = data
        d.sync()
        d.close()
    
    def del_stat(self, date):
        key = str(date)
        filename = './data/%s_%s_main_stat.dat' % (self.schema, self.table)
        d = shelve.open(filename)
        del d[key]
        d.close()
        filename = './data/%s_%s_ext_stat.dat' % (self.schema, self.table)
        d = shelve.open(filename)
        del d[key]
        d.close()
        
    def add_ext_stat(self, date, data):
        key = str(date)
        filename = './data/%s_%s_ext_stat.dat' % (self.schema, self.table)
        d = shelve.open(filename)
        d[key] = data
        d.sync()
        d.close()
    
    def history_stat(self, parent):
        main = parent
        filename = './data/%s_%s_main_stat.dat' % (self.schema, self.table)
        d = shelve.open(filename)
        keys = d.keys()
        dat = []
        for key in keys:
            data = d[key]
            dat.append(data)
        d.close()
        return dat
        
#file = 'ext_stat.dat'
#data = ("abc", 12)      # - данные (объект)
#key = "key"             # - ключ (строка)
#filename = "polka.dat"  # - имя файла для хранения полки
#d = shelve.open(file)       # открытие полки
#d.close()
#d[key] = data           # сохранить данные под ключом key 
#                        # (удаляет старое значение, если оно было)
#data = d[key]           # загрузить значение по ключу 
#len(d)                  # получить количество объектов на полке
#d.sync()                # запись изменений в БД на диске
#del d[key]              # удалить ключ и значение
#flag = d.has_key(key)   # проверка наличия ключа
#lst = d.keys()          # список ключей 
#d.close()               # закрытие полки