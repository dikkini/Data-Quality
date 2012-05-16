# -*- coding: utf8 -*-
import oracle
import sqlite
import datetime
import statistic
import wx
import logging
logging.basicConfig(filename='journal_events.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

class DQ(object):
	def __init__(self, connection, schema, table):
		self.connection = connection
		self.table = table
		self.schema = schema

	def mathDQ(self, weights, using_params):
		logging.info(u'starting calculation data quality model')
		self.data = []
		dt = datetime.datetime.now()
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
			emptyvalues = 100 - emptyvalues
			self.data.append(str(emptyvalues))
		else:
			emptyvalues = 0
			self.data.append(u'-')
		print 'Empty:', emptyvalues, '%'

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
				avgnoinf = 100 - avgnoinf
				self.data.append(str(avgnoinf))

				# Расчет расширенной статистики по колонкам
				ext_stat = []
				info = [u'Не несущие значения']
				for i in count1:
					if i == 0.0 and type(i) is float:
						ext_stat.append('-')
					else:
						ext_stat.append(str((float(i) / self.countall * 100)))
				
				for i in ext_stat:
					info.append(i)
				self.extend_stat.append(info)
				logging.info(u'not informable parameter calculation successfully')
			else:
				avgnoinf = 0
				self.data.append(u'-')
				self.extend_stat.append(None)
			print 'No_Inform:', avgnoinf, '%'
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
				avgbadform = 100 - avgbadform
				self.data.append(str(avgbadform))
				ext_stat = []
				info = [u'Не соответствующие формату']
				
				for i in count2:
					if i == 0.0 and type(i) is float:
						ext_stat.append('-')
					else:
						ext_stat.append(str((float(i) / self.countall * 100)))
				
				for i in ext_stat:
					info.append(i)
					
				self.extend_stat.append(info)
				logging.info(u'bad fromat parameter calculation successfully')
			else:
				avgbadform = 0
				self.data.append(u'-')
				self.extend_stat.append(None)
			print 'bad_format', avgbadform, '%'
		except Exception, info:
			print info
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
				avgnoise = 100 - avgnoise
				self.data.append(str(avgnoise))

				ext_stat = []
				info = [u'Уровень шума']
				for i in count3:
					if i == 0.0 and type(i) is float:
						ext_stat.append('-')
					else:
						ext_stat.append(str((float(i) / self.countall * 100)))
				for i in ext_stat:
					info.append(i)
				self.extend_stat.append(info)
				logging.info(u'noise level parameter calculation successfully')
			else:
				avgnoise = 0
				self.data.append(u'-')
				self.extend_stat.append(None)
			print 'noise_level:', avgnoise, '%'
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
				self.data.append(str(avgident))
				logging.info(u'identify parameter calculation successfully')
			else:
				avgident = 0
				self.data.append(u'-')
			print 'identifiabilit:', avgident, '%'
			
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
				self.data.append(str(avgharm))
				logging.info(u'harmony parameter calculation successfully')
			else:
				avgharm = 0
				self.data.append(u'-')
			print 'harmony:', avgharm, '%'
		except Exception, info:
			logging.error(u'harmony parameter calculation failed: %s' % str(info))

		# Унификация
		try:
			if self.using_params[6] == 1:
				count6 = []
				param = 'uniq'
				for column in self.namecols:
					count6.append(orcl.get_uniq_values(column, self.schema, self.table))
				avguniq = (sum(count6) / len(count6)) * self.weights[6]
				avguniq = float(avguniq)
				avguniq = avguniq / self.countall * 100
				self.data.append(str(avguniq))

				ext_stat = []
				info = [u'Унификация']
				for i in count6:
					ext_stat.append(str((float(i) / self.countall * 100)))
				for i in ext_stat:
					info.append(i)
				self.extend_stat.append(info)
				logging.info(u'uniq parameter calculation successfully')
			else:
				avguniq = 0
				self.data.append(u'-')
				self.extend_stat.append(None)
			print 'Uniq:', avguniq, '%'
		except Exception, info:
			logging.error(u'uniq parameter calculation failed: %s' % str(info))
			
		# Оперативность
		try:
			if self.using_params[7] == 1:
				count7 = []
				param = 'efficiency'
				regexp = sql.take_regexps(param)
				for i in range(len(regexp)):
					count7.append(orcl.get_regexp_count(self.schema, self.table, regexp[i]))
				avgeffic = (sum(count7) / len(count7)) * self.weights[7]
				avgeffic = float(avgeffic)
				avgeffic = avgeffic / self.countall * 100
				self.data.append(str(avgeffic))
				logging.info(u'efficiency parameter calculation successfully')
			else:
				avgeffic = 0
				self.data.append(u'-')
			print 'efficiency:', avgeffic, '%'
		except Exception, info:
			logging.error(u'efficiency parameter calculation failed: %s' % str(info))

		# Противоречивость
		try:
			if self.using_params[8] == 1:
				count8 = []
				param = 'inconsistency'
				regexp = sql.take_regexps(param)
				for i in range(len(regexp)):
					count8.append(orcl.get_regexp_count(self.schema, self.table, regexp[i]))
				avgincon = (sum(count8) / len(count8)) * self.weights[8]
				avgincon = float(avgincon)
				avgincon = avgincon / self.countall * 100
				avgincon = 100 - avgincon
				self.data.append(str(avgincon))
				logging.info(u'inconsistency parameter calculation successfully')
			else:
				avgincon = 0
				self.data.append(u'-')
			print 'inconsistency:', avgincon, '%'
		except Exception, info:
			logging.error(u'inconsistency parameter calculation failed: %s' % str(info))

		# Степень классификации
		try:
			if self.using_params[9] == 1:
				count9 = []
				param = 'degree_of_classification'
				regexp = sql.take_regexps(param)
				for i in range(len(regexp)):
					count9.append(orcl.get_regexp_count(self.schema, self.table, regexp[i]))
				avgdoc = (sum(count9) / len(count10)) * self.weights[9]
				avgdoc = float(avgdoc)
				avgdoc = avgdoc / self.countall * 100
				self.data.append(str(avgdoc))
				logging.info(u'degree_of_classification parameter calculation successfully')
			else:
				avgdoc = 0
				self.data.append(u'-')
			print 'degree_of_classification:', avgdoc, '%'
		except Exception, info:
			logging.error(u'degree_of_classification parameter calculation failed: %s' % str(info))
			
		# Степень структуризации
		try:
			if self.using_params[10] == 1:
				count10 = []
				param = 'degree_of_structuring'
				regexp = sql.take_regexps(param)
				for i in range(len(regexp)):
					count11.append(orcl.get_regexp_count(self.schema, self.table, regexp[i]))
				avgdos = (sum(count10) / len(count10)) * self.weights[10]
				avgdos = float(avgdos)
				avgdos = avgdos / self.countall * 100
				self.data.append(str(avgdos))
				logging.info(u'degree_of_structuring parameter calculation successfully')
			else:
				avgdos = 0
				self.data.append(u'-')
			print 'degree_of_structuring:', avgdos, '%'
		except Exception, info:
			logging.error(u'degree_of_structuring parameter calculation failed: %s' % str(info))
		try:
			avgall = emptyvalues + avgnoinf + avgbadform + avgnoise + avgident + avgharm + avguniq + avgeffic + avgincon + avgdoc + avgdos
			allweight = sum(self.weights)
		except Exception, info:
			logging.error(u'avegrage assessment of all parameters calculation failed: %s' % str(info))
			print info
		try:
			result = avgall / allweight
		except Exception, info:
			logging.error(u'calculation dq failed: %s' % str(info))
			return False
		result = str(round(result, 2))
		self.data.append(result)
		self.data.append(self.table)
		self.dat = []
		self.dat.append(self.data)

		print 'ITOGO:', result, '%'

		stat.add_main_stat(timedq, self.data)
		stat.add_ext_stat(timedq, self.extend_stat)
		
		logging.info(u'calculation successfully')
		
		return self.dat