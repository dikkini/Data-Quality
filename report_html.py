#-*- coding: utf8 -*-
import wx
import os
from jinja2 import Environment, FileSystemLoader, Template, PackageLoader
import logging

logging.basicConfig(filename='journal_events.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

###########################################################################
## Class ReportClass
###########################################################################

def make_report(name_main, main_stat, name_ext, ext_stat, date):
    try:
        OUTPUT_ROOT = os.path.join(os.path.dirname(__file__), 'reports')
        outfile = 'Report-%s.html' % date
        ext_stat = filter(bool, ext_stat)
        main_stat = list(main_stat)
        main_stat.insert(0, date)
        main_s = zip(name_main, main_stat)
        env = Environment(loader=PackageLoader('DataQuality', '/data/source_reports/'))
        template = env.get_template('template.html')
        code = template.render(main_s=main_s, date=date, name_ext=name_ext, ext_stat=ext_stat)
        #todo-write_in_file: bad encoding
        with open(os.path.join(OUTPUT_ROOT, outfile), 'w') as f:
            f.write(code.encode('utf8'))
        wx.MessageBox(u'Отчет сформирован и сохранен в папке reports!')
        logging.info('report succesfully done')
    except Exception, info:
        wx.MessageBox(str(info))
        wx.MessageBox(u'В ходе формирования отчета произошла непоправимая ошибка!')
        logging.error('report failed: %s -- code 28' % str(info))
