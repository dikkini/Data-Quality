#-*- coding: utf8 -*-
import wx
import os
from jinja2 import Environment, FileSystemLoader, Template, PackageLoader

def make_report(name_main, main_stat, name_ext, ext_stat, date):
    OUTPUT_ROOT = os.path.join(os.path.dirname(__file__), 'reports')
    print date
    print str(list(date))
    outfile = 'Report-%s.html' % date
    ext_stat = filter(bool, ext_stat)
    main_stat = list(main_stat)
    main_stat.insert(0, date)
    main_s = zip(name_main, main_stat)
    #extend_s = zip(name_ext, ext_stat)
    env = Environment(loader=PackageLoader('DataQuality', '/data/source_reports/'))
    template = env.get_template('template.html')
    code = template.render(main_s= main_s, date=date, name_ext=name_ext, ext_stat=ext_stat)
    #todo-write_in_file: не записывается файл, так как время сделано через :, а это не приемлимо для имени файла в ОС Windows
    with open(os.path.join(OUTPUT_ROOT, outfile), 'w') as f:
        f.write(code.encode('utf-8'))
