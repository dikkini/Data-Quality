#-*- coding: utf8 -*-
import wx
import os
from jinja2 import Environment, FileSystemLoader, Template, PackageLoader

def make_report(name_main, main_stat, name_ext, ext_stat):
    print name_main
    print main_stat
    print name_ext
    print ext_stat
    env = Environment(loader=PackageLoader('DataQuality', '/data/reports/'))
    template = env.get_template('rep.html')
    print template.render(name_main=name_main, main_stat=main_stat, name_ext=name_ext, ext_stat=ext_stat)