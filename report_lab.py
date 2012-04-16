#-*- coding: utf8 -*-

from reportlab.platypus import Paragraph,SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import reportlab.rl_config #@UnusedImport
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import statistic
import logging

logging.basicConfig(filename='journal_events.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

class CreateRep:
    def __init__(self, data):
        print data
        # пути к фонтам и регистрация фонта
        reportlab.rl_config.TTFSearchPath='./data/fonts/'
        pdfmetrics.registerFont(TTFont('Arial', './data/reports/arial.ttf'))
        story=[]  # словарь документа
        styles = getSampleStyleSheet() # дефолтовые стили
        # создаем объект документа с размером страницы A4
        #doc=SimpleDocTemplate('test.pdf',pagesize = A4,title='sss',author=u'test')
        #story.append(Paragraph(u'TEST', styles['Heading1']))
        MyCanvas = canvas.Canvas('./data/reports/results.pdf')
        MyCanvas.drawString(10*cm, 15*cm, u'Результаты оценки качества данных:')
        MyCanvas.drawString(1*cm, 1*cm, '%s' % str(data))
        MyCanvas.save()
        


