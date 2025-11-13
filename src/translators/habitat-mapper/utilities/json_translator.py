################################################################################
#                                                                              #
#                              json_translator.py                              #
#                                                                              #
################################################################################
#                                                                              #
#        This is a class for translating Habitat Mapper json data.             #
#                                                                              #
#        Author(s): Abe Megahed                                                #
#                                                                              #
#        This file is subject to the terms and conditions defined in           #
#        'LICENSE.txt', which is part of this source code distribution.        #
#                                                                              #
################################################################################
#        Copyright (C) 2025 - Global Mosquito Observations Dashboard           #
################################################################################

import os

#
# globals
#

current = os.path.dirname(os.path.abspath(__file__))
schema = current + '/output_schema.txt'

#
# class
#

class HabitatMapperTranslator:
	columns = []
	count = 0

	#
	# constructor
	#

	def __init__(self):
		global schema

		# read schema
		#
		with open(schema, 'r') as file:
			for line in file:
				column = line.replace(',', '').replace('REQUIRED', '').replace('MANDATORY', '').strip()
				if not column.startswith('//'):
					self.columns.append(column)

	#
	# converting methods
	#

	def object_to_array(self, object):

		"""
		Convert an object to an array of values.

		Args:
			object (dict): An associative array.

		Returns:
			array: The array of values.
		"""

		values = []
		for key in object:
			values.append(object[key])
		return values

	#
	# translating methods
	#

	def translate_value(self, key, observation):

		"""
		Translate a value with a particular name (key) from an observation.

		Args:
			key: the name of the desired field.
			observation (dict): The observation data.

		Returns:
			object: The translated value.
		"""

		#
		# casting functions
		#

		def is_integer(s):
			try:
				int(s)
				return True
			except ValueError:
				return False

		def val(data, name):
			try:
				if name in data:
					value = str(data[name])
					if value != None:
						value = value.encode('utf-8').decode('ascii')
						return value
					else:
						return ''
				else:
					return ''
			except ValueError:
				return ''

		def to_integer(value):
			try:
				if value == None:
					return 0
				elif isinstance(value, int):
					return value
				elif value == '':
					return 0
				else:
					return int(value)
			except ValueError:
				return 0

		def to_float(value):
			try:
				if value == None:
					return 0
				elif isinstance(value, float):
					return value
				elif value == '':
					return 0
				else:
					return float(value)
			except ValueError:
				return 0

		def to_count(value):
			try:
				if value == None:
					return 0
				elif is_integer(value):
					return to_integer(value)
				elif '-' in value:
					return to_integer(value.split('-')[1])
				elif 'more than' in value:
					return to_integer(value.replace('more than', ''))
				else:
					return 0
			except ValueError:
				return 0

		def intval(data, name):
			if name in data:
				return to_integer(data[name])
			else:
				return 0

		def floatval(data, name):
			if name in data:
				return to_float(data[name])
			else:
				return 0

		def countval(data, name):
			if name in data:
				return to_count(data[name])
			else:
				return 0

		data = observation['data']

		match key:
			case 'mhm_protocol':
				return 'mosquito_habitat_mapper'

			case 'mhm_measuredDate':
				return val(observation, 'measuredDate')

			case 'mhm_createDate':
				return val(observation, 'createDate')

			case 'mhm_updateDate':
				return val(observation, 'updateDate')

			case 'mhm_publishDate':
				return val(observation, 'publishDate')

			case 'mhm_organizationId':
				return val(observation, 'organizationId')

			case 'mhm_organizationName':
				return val(observation, 'organizationName')

			case 'mhm_siteId':
				return val(observation, 'siteName')

			case 'mhm_siteName':
				return val(observation, 'countryName')

			case 'mhm_ExtraData':
				return val(data, 'mosquitohabitatmapperExtraData')

			case 'mhm_AbdomenCloseupPhotoUrls':
				return val(data, 'mosquitohabitatmapperAbdomenCloseupPhotoUrls')

			case 'mhm_WaterSourcePhotoUrls':
				return val(data, 'mosquitohabitatmapperWaterSourcePhotoUrls')

			case 'mhm_LarvaeCount':
				return countval(data, 'mosquitohabitatmapperLarvaeCount')

			case 'mhm_MosquitoEggs':
				return val(data, 'mosquitohabitatmapperMosquitoEggs')

			case 'mhm_LocationAccuracyM':
				return floatval(data, 'mosquitohabitatmapperLocationAccuracyM')

			case 'mhm_MosquitoEggCount':
				return countval(data, 'mosquitohabitatmapperMosquitoEggCount')

			case 'mhm_Comments':
				return val(data, 'mosquitohabitatmapperComments')

			case 'mhm_Latitude':
				return floatval(data, 'mosquitohabitatmapperMeasurementLatitude')

			case 'mhm_Longitude':
				return floatval(data, 'mosquitohabitatmapperMeasurementLongitude')

			case 'mhm_MosquitoHabitatMapperId':
				return intval(data, 'mosquitohabitatmapperMosquitoHabitatMapperId')

			case 'mhm_BreedingGroundEliminated':
				return val(data, 'mosquitohabitatmapperBreedingGroundEliminated')

			case 'mhm_MeasuredAt':
				return val(data, 'mosquitohabitatmapperMeasuredAt')
		
			case 'mhm_MeasurementElevation':
				return val(data, 'mosquitohabitatmapperMeasurementElevation')

			case 'mhm_Userid':
				return val(data, 'mosquitohabitatmapperUserid')

			case 'mhm_Genus':
				return val(data, 'mosquitohabitatmapperGenus')

			case 'mhm_LocationMethod':
				return val(data, 'mosquitohabitatmapperLocationMethod')

			case 'mhm_WaterSource':
				return val(data, 'mosquitohabitatmapperWaterSource')

			case 'mhm_MosquitoAdults':
				return val(data, 'mosquitohabitatmapperMosquitoAdults')

			case 'mhm_Species':
				return val(data, 'mosquitohabitatmapperSpecies')

			case 'mhm_MosquitoPupae':
				return val(data, 'mosquitohabitatmapperMosquitoPupae')

			case 'mhm_DataSource':
				return val(data, 'mosquitohabitatmapperDataSource')

			case 'mhm_LarvaFullBodyPhotoUrls':
				return val(data, 'mosquitohabitatmapperLarvaFullBodyPhotoUrls')

			case 'mhm_LastIdentifyStage':
				return val(data, 'mosquitohabitatmapperLastIdentifyStage')

			case 'mhm_WaterSourceType':
				return val(data, 'mosquitohabitatmapperWaterSourceType')

			case 'mhm_GlobeTeams':
				if 'mosquitohabitatmapperGlobeTeams' in data:
					if len(data['mosquitohabitatmapperGlobeTeams']) > 0:
						return data['mosquitohabitatmapperGlobeTeams'][0]

			case 'x':
				# return val(observation, 'longitude')
				 return floatval(data, 'mosquitohabitatmapperMeasurementLongitude')

			case 'y':
				# return val(observation, 'latitude')
				return floatval(data, 'mosquitohabitatmapperMeasurementLatitude')

		return ''

	def translate_observation(self, observation):

		"""
		Translate an observation.

		Args:
			observation (dict): The observation data.

		Returns:
			object: The set of values.
		"""

		values = {}
		for column in self.columns:
			values[column] = self.translate_value(column, observation) or ''
		return values

	def translate_observations(self, observations):

		"""
		Translate an array of observations.

		Args:
			observations (array): The array of observations.

		Returns:
			object: array of sets of values.
		"""

		values = []
		if len(observations) > 0:
			columns = observations[0]
			for index in range(1, len(observations)):
				values.append(self.translate_observation( observations[index]))
		return values
