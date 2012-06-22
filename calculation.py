# -*- coding: utf8 -*-
import oracle
import sqlite
import datetime
from datetime import timedelta
from datetime import datetime
import statistic
import wx
import logging
logging.basicConfig(filename='journal_events.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

class DQ(object):
	def __init__(self, connection):
		self.connection = connection
		
	
	def mathDQ(self, weights, using_params, user_choice_catalog, user_number_allfields, user_number_composite_fileds, user_days_can_be, list_of_fields, schema, table):
		self.table = table
		self.schema = schema
		logging.info(u'starting calculation data quality model')
		self.data = []
		dt = datetime.now()
		timedq = dt.strftime('%Y.%m.%d-%H-%M-%S')
		self.data.append(timedq)
		sql = sqlite.sqliteDB(self.schema, self.table)
		stat = statistic.stats(self.schema, self.table)
		orcl = oracle.WorkDB(self.connection)
		self.countall = orcl.get_all_count(self.schema, self.table)
		self.weights = weights
		self.using_params = using_params
		if self.weights is None or self.weights == []:
			wx.MessageBox(u'Выберите параметры оценки прежде чем запускать оценку качества данных.')
			return None
		for i in range(len(self.weights)):
			self.weights[i] = float(self.weights[i])

		self.namecols = orcl.get_cols(self.table)
		
		# Пустые значения
		if self.using_params[0] == 1:
			# Количество значений подпадающих под критерий
			count0 = orcl.get_empty_values(self.schema, self.table)
			count0 = count0 * self.weights[0]
			emptyvalues = count0 / self.countall * 100
			emptyvalues = str(round(emptyvalues, 2))
			self.data.append(emptyvalues)
		else:
			emptyvalues = 100
			self.data.append(u'-')

		self.extend_stat = []


		# Не несущие информации значения
		try:
			if self.using_params[1] == 1:
				count1 = []
				param = 'no_information'
				regexp = sql.take_regexps(param)
				for col in self.namecols:
					count1.append(0.0)
					for reg in regexp:
						if col in reg:
							col_index = self.namecols.index(col)
							count1[col_index] = orcl.get_regexp_count(self.schema, self.table, reg)
				avgnoinf = (sum(count1) / len(count1)) * self.weights[1]
				avgnoinf = float(avgnoinf)
				avgnoinf = avgnoinf / self.countall * 100
				avgnoinf = str(round(avgnoinf, 2))
				self.data.append(avgnoinf)
				
				
				# Расчет расширенной статистики по колонкам
				ext_stat = []
				info = [u'Не несущие значения']
				for i in count1:
					if i == 0.0 and type(i) is float:
						ext_stat.append('-')
					else:
						ext_stat.append(str(round((float(i) / self.countall * 100),2)))
				
				for i in ext_stat:
					info.append(i)
				self.extend_stat.append(info)
				logging.info(u'not informable parameter calculation successfully')
			else:
				avgnoinf = 100
				self.data.append(u'-')
				self.extend_stat.append(None)
		except Exception, info:
			logging.error(u'not informable parameter calculation failed: %s' % str(info))

		# Не соответствующие формату значения
		try:
			if self.using_params[2] == 1:
				count2 = []
				param = 'bad_format'
				
				regexp = sql.take_regexps(param)

				for col in self.namecols:
					count2.append(0.0)
					for reg in regexp:
						if col in reg:
							col_index = self.namecols.index(col)
							count2[col_index] = orcl.get_regexp_count(self.schema, self.table, reg)
				
				avgbadform = (sum(count2) / len(count2)) * self.weights[2]
				avgbadform = float(avgbadform)
				avgbadform = avgbadform / self.countall * 100
				avgbadform = str(round(avgbadform, 2))
				self.data.append(avgbadform)
				ext_stat = []
				info = [u'Не соответствующие формату']
				
				for i in count2:
					if i == 0.0 and type(i) is float:
						ext_stat.append('-')
					else:
						ext_stat.append(str(round((float(i) / self.countall * 100),2)))
				
				for i in ext_stat:
					info.append(i)
					
				self.extend_stat.append(info)
				logging.info(u'bad fromat parameter calculation successfully')
			else:
				avgbadform = 100
				self.data.append(u'-')
				self.extend_stat.append(None)
		except Exception, info:
			logging.error(u'bad format parameter calculation failed: %s' % str(info))

		# Значение уровня шума
		try:
			if self.using_params[3] == 1:
				count3 = []
				param = 'noise_level'
				regexp = sql.take_regexps(param)
				for col in self.namecols:
					count3.append(0.0)
					for reg in regexp:
						if col in reg:
							col_index = self.namecols.index(col)
							count3[col_index] = orcl.get_regexp_count(self.schema, self.table, reg)
				avgnoise = (sum(count3) / len(count3)) * self.weights[3]
				avgnoise = float(avgnoise)
				avgnoise = avgnoise / self.countall * 100
				avgnoise = str(round(avgnoise, 2))
				self.data.append(avgnoise)

				ext_stat = []
				info = [u'Уровень шума']
				for i in count3:
					if i == 0.0 and type(i) is float:
						ext_stat.append('-')
					else:
						ext_stat.append(str(round((float(i) / self.countall * 100),2)))
				for i in ext_stat:
					info.append(i)
				self.extend_stat.append(info)
				logging.info(u'noise level parameter calculation successfully')
			else:
				avgnoise = 100
				self.data.append(u'-')
				self.extend_stat.append(None)
		except Exception, info:
			logging.error(u'noise level parameter calculation failed: %s' % str(info))

		# Идентифицируемость
		try:
			if self.using_params[4] == 1:
				count4 = []
				param = 'identifiability'
				regexp = sql.take_regexps(param)
				for i in range(len(regexp)):
					count4.append(orcl.get_regexp_count(self.schema, self.table, regexp[i]))
				avgident = (sum(count4) / len(count4)) * self.weights[4]
				avgident = float(avgident)
				avgident = avgident / self.countall * 100
				avgident = str(round(avgident, 2))
				self.data.append(avgident)
				logging.info(u'identify parameter calculation successfully')
			else:
				avgident = 0
				self.data.append(u'-')
			
		except Exception, info:
			logging.error(u'indentify parameter calculation failed: %s' % str(info))
			
		# Согласованность
		try:
			if self.using_params[5] == 1:
				count5 = []
				param = 'harmony'
				regexp = sql.take_regexps(param)
				for i in range(len(regexp)):
					count5.append(orcl.get_regexp_count(self.schema, self.table, regexp[i]))
				avgharm = (sum(count5) / len(count5)) * self.weights[5]
				avgharm = float(avgharm)
				avgharm = avgharm / self.countall * 100
				avgharm = str(round(avgharm, 2))
				self.data.append(avgharm)
				logging.info(u'harmony parameter calculation successfully')
			else:
				avgharm = 0
				self.data.append(u'-')
		except Exception, info:
			logging.error(u'harmony parameter calculation failed: %s' % str(info))

		# Унификация
		try:
			if self.using_params[6] == 1:
				count6 = []
				param = 'uniq'
				for column in self.namecols:
					val = orcl.get_uniq_values(column, self.schema, self.table)
					count6.append(val)
				avguniq = (sum(count6) / len(count6)) * self.weights[6]
				avguniq = float(avguniq)
				avguniq = avguniq / self.countall * 100
				avguniq = str(round(avguniq, 2))
				self.data.append(avguniq)

				ext_stat = []
				info = [u'Унификация']
				for i in count6:
					ext_stat.append(str(round((float(i) / self.countall * 100),2)))
				for i in ext_stat:
					info.append(i)
				self.extend_stat.append(info)
				logging.info(u'uniq parameter calculation successfully')
			else:
				avguniq = 0
				self.data.append(u'-')
				self.extend_stat.append(None)
		except Exception, info:
			logging.error(u'uniq parameter calculation failed: %s' % str(info))
			
		# Оперативность
		try:
			if self.using_params[7] == 1:
				count7 = []
				param = 'efficiency'
				nowdate=datetime.now()
				#nowdate = nowdate.strftime('%Y-%m-%d %H:%M:%S')
				realdate = orcl.get_date_table(self.table, self.schema)
				realdate = str(realdate)
				format = '%Y-%m-%d %H:%M:%S'
				realdate = datetime.strptime(realdate, format)
				delta = nowdate - realdate
				delta = delta.days
				if int(user_days_can_be) < delta:
					avgeffic = int(user_days_can_be) / delta * 100
					avgeffic = str(avgeffic)
				elif int(user_days_can_be) > delta:
					avgeffic = '100'
				self.data.append(avgeffic)
				logging.info(u'efficiency parameter calculation successfully')
			else:
				avgeffic = 0
				self.data.append(u'-')
		except Exception, info:
			logging.error(u'efficiency parameter calculation failed: %s' % str(info))

		# Противоречивость
		try:
			if self.using_params[8] == 1:
				count8 = []
				count8_1 = []
				count8_2 = []
				param = 'inconsistency'
				for column in list_of_fields:
					val = orcl.get_uniq_values(column, self.schema, self.table)
					count8.append(val)
				for var in count8:
					var = int(var)
					newvar = float(self.countall - var)
					count8_1.append(newvar)
				for var in count8_1:
					temp = float(var / self.countall)
					endvar = float(temp) * 100
					count8_2.append(endvar)
					
				avgincon = sum(count8_2)
				avgincon = float(avgincon)
				avgincon = str(avgincon)
				self.data.append(avgincon)
				logging.info(u'inconsistency parameter calculation successfully')
			else:
				avgincon = 100
				self.data.append(u'-')
		except Exception, info:
			logging.error(u'inconsistency parameter calculation failed: %s' % str(info))

		# Степень классификации
		try:
			if self.using_params[9] == 1:
				const = 0.1
				uniq_values = []
				count9 = []
				param = 'degree_of_classification'
				
				for column in self.namecols:
					uniq_values.append(orcl.get_uniq_values(column, self.schema, self.table))
				
				for value in uniq_values:
					count9.append(float(value / self.countall))
				i = 0
				for value in count9:
					if value < const:
						i = i + 1
				if i == 0:
					wx.MessageBox(u'Для данного массива данных степень классификации не может быть посчитана, так как ни одно поле не заполнено по справочнику')
					logging.info(u'degree_of_classification parameter not calculated, because there are no catalogs used')
					avgdoc = 0
					self.data.append(u'-')
				else:
					avgdoc = float(float(user_choice_catalog) / float(i))
					avgdoc = avgdoc * self.weights[9] * 100
					avgdoc = float(avgdoc)
					avgdoc = str(round(avgdoc, 2))
					self.data.append(avgdoc)
					logging.info(u'degree_of_classification parameter calculation successfully')
			else:
				avgdoc = 0
				self.data.append(u'-')
		except Exception, info:
			logging.error(u'degree_of_classification parameter calculation failed: %s' % str(info))
		
		# Степень структуризации
		try:
			if self.using_params[10] == 1:
				count10 = []
				param = 'degree_of_structuring'
				avgdos = float(float(user_number_composite_fileds) / float(user_number_allfields)) * 100
				avgdos = float(avgdos)
				avgdos = round(avgdos, 2)
				avgdos = str(avgdos)
				self.data.append(avgdos)
				logging.info(u'degree_of_structuring parameter calculation successfully')
			else:
				avgdos = 0
				self.data.append(u'-')
		except Exception, info:
			logging.error(u'degree_of_structuring parameter calculation failed: %s' % str(info))
			
		try:
			# Итоговая оценка. 100 - параметр для тех параметров которые в сущности отрицательные
			avgall = float(100 - float(emptyvalues)) + float(100 - float(avgnoinf)) + float(100 - float(avgbadform)) + float(100 - float(avgnoise)) + float(avgident) + float(avgharm) + float(avguniq) + float(avgeffic) + float(100 - float(avgincon)) + float(avgdoc) + float(avgdos)
			# Вычисляем количество параметров имеющих оценку
			i = 0
			for param in self.using_params:
				if param == 1:
					i = i + 1
		except Exception, info:
			logging.error(u'average assessment of all parameters calculation failed: %s' % str(info))
		try:
			result = avgall / i
		except Exception, info:
			logging.error(u'calculation dq failed: %s' % str(info))
			return False
		result = str(round(result, 2))
		self.data.append(result)
		tabl_schema = ('%s:%s' % (self.schema, self.table))
		self.data.append(tabl_schema)
		self.dat = []
		self.dat.append(self.data)

		stat.add_main_stat(timedq, self.data)
		stat.add_ext_stat(timedq, self.extend_stat)
		
		logging.info(u'calculation successfully')
		
		return self.dat