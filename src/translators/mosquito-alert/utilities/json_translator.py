################################################################################
#                                                                              #
#                              json_translator.py                              #
#                                                                              #
################################################################################
#                                                                              #
#        This is a class for translating Moquito Alert data.                   #
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

class MosquitoAlertTranslator:
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
	# translation methods
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

		match key:

			case 'OBJECTID':
				self.count += 1
				return self.count

			case 'title':
				return 'Citizen science data on mosquitoes from Mosquito Alert with additional automated ID'

			case 'description':
				return 'Data is generated from the Mosquito Alert database'

			case 'dataStreamName':
				return 'mosquito species occurrence data from user cell phone'

			case 'dataStreamDescription':
				return 'All species occurrence, site, or bite observations from a particular user taken with a sensor'

			case 'dataStreamObsType':
				return 'category observation'

			case 'dataStreamUniCategory':
				return {
					'Type': 'Lifecycle Phase', 
					'Identified by Human': 'Class and genus or species if verified from image', 
					'Identified by Machine': 'Genus and species if mosquito is flagged as a target invasive or vector by ML system'
				}

			case 'observationProObsUID':
				return observation['uuid']

			case 'observationResCatObsPheTime':
				return observation['created_at']

			case 'observationResCatObsResTime':
				return observation['created_at']

			case 'observationResCatObsResult':
				if observation['identification'] and observation['identification']['result'] and observation['identification']['result']['taxon']:
					name =  observation['identification']['result']['taxon']['name']
					source = observation['identification']['result']['source']
					return {
						'Type': '', 
						'Indentified by Human': name if source != 'auto' else '', 
						'Identified by Machine': name if source == 'auto' else ''
					}
				else:
					return {
						'Type': '', 
						'Indentified by Human': '', 
						'Identified by Machine': ''
					}

			case 'obsResCatObsResult_Type':
				return ''

			case 'Identified by Human' | 'Indentified by Human':
				if observation['identification'] and observation['identification']['result'] and observation['identification']['result']['taxon']:
					if observation['identification']['result']['source'] != 'auto':
						return observation['identification']['result']['taxon']['name']

			case 'Identified by Machine' | 'Identified by Machine':
				if observation['identification'] and observation['identification']['result'] and observation['identification']['result']['taxon']:
					if observation['identification']['result']['source'] == 'auto':
						taxon = observation['identification']['result']['taxon']
						return observation['identification']['result']['taxon']['name']

			case 'observationResCatObsSubTime':
				return observation['created_at']

			case 'observationImaImaStatus':
				if observation['identification']:
					return 1
				else:
					return 0

			case 'observationImaImaResult':
				if observation['identification']:
					return observation['identification']['photo']['url']

			case 'observationConParameters':
				return {
					'Aegypti Certainty': '', 
					'Tiger Certainty': '', 
					'site_cat': '', 
					'nuts_3': '', 
					'nuts_2': ''
				}

			case 'Aegypti_Certainty':
				return ''

			case 'Tiger_Certainty':
				return ''

			case 'omProcessLicLicName':
				return 'CC0'

			case 'omProcessLicLicURI':
				return 'http://creativecommons.org/publicdomain/zero/1.0/'

			case 'omProcessLicLicAttSource':
				return 'This data set has been created through the efforts of the Mosquito Alert team and the thousands of citizen scientists who have volunteered their energy and contributed reports on the Mosquito Alert platform. We ask that you give attribution to the Mosquito Alert Community if you use this data in any publications.'

			case 'omProcessLicLicAttAggregator':
				return 'Agustí Escobar Rubies, & Mosquito Alert.  (2021).  Mosquito Alert Data. Zenodo. DOI: 10.5281/zenodo.597466'

			case 'omProcessProType' | 'omPrcoessProType':
				return 'Sensor'

			case 'omProcessProReference':
				return 'http://www.mosquitoalert.com/en/project/what-is-mosquito-alert/'

			case 'omProcessResQuaValStatus' | 'omPrcoessResQuaValStatus':
				return 1

			case 'omProcessResQuaValMethod' | 'omPrcoessResQuaValMethod':
				return 'Human expert validation'

			case 'omProcessResQuaValResult' | 'omPrcoessResQuaValResult':
				return 0

			case 'omProcessResQuaQuaGrade' | 'omPrcoessResQuaQuaGrade':
				return 'Casual'

			case 'observedProName':
				return ''

			case 'observedProDescription':
				return 'Whether a species is observed at a location, a breeding site is documented, or bites are reported'

			case 'observedProDefinition':
				return 'http://www.mosquitoalert.com/en/project/envia-datos/'

			case 'sensorName':
				return observation['uuid']

			case 'sensorDescription':
				return 'Anonymous cell phone user:' + observation['uuid']

			case 'sensorEncType':
				return 'Varies'

			case 'locationName':
				return observation['location']['display_name']

			case 'locationDescription':
				return observation['event_environment']

			case 'locationEncType':
				return 'GeoJSON Point'

			case 'latitude':
				return observation['location']['point']['latitude']

			case 'longitude':
				return observation['location']['point']['longitude']

			case 'thingName':
				return 'sensor.name'

			case 'thingDescription':
				return 'sensor.description'

			case 'featureIntName':
				return 'location.name'

			case 'featureIntDescription':
				return 'location.description'

			case 'featureIntEncType':
				return 'GeoJSON Point'

			case 'featureIntLocation':
				return 'latitude, longitude'

			case 'type':
				return 'FeatureCollection'

			case 'coordinates':
				latitude = observation['location']['point']['latitude']
				longitude = observation['location']['point']['longitude']
				return [longitude, latitude]

			case 'nuts_3':
				return ''

			case 'nuts_2':
				return ''

			case 'Speed':
				return ''

			case 'Direction of travel (°)':
				return ''

			case 'Compass reading (°)':
				return ''

			case 'Position source type':
				return ''

			case 'Receiver Name':
				return ''

			case 'Horizontal Accuracy (m)':
				return ''

			case 'Latitude':
				return observation['location']['point']['latitude']

			case 'Longitude':
				return observation['location']['point']['longitude']

			case 'Altitude':
				return ''

			case 'PDOP':
				return ''

			case 'HDOP':
				return ''

			case 'VDOP':
				return ''

			case 'Fix Type':
				return ''

			case 'Correction Age':
				return ''

			case 'Station ID':
				return ''

			case 'Number of Satellites':
				return ''

			case 'Fix Time':
				return ''

			case 'Average Horizontal Accuracy (m)':
				return ''

			case 'Average Vertical Accuracy (m)':
				return ''

			case 'Averaged Positions':
				return ''

			case 'Standard Deviation (m)':
				return ''

			case 'x':
				return observation['location']['point']['longitude']

			case 'y':
				return observation['location']['point']['latitude']

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
			for observation in observations:
				values.append(self.translate_observation(observation))
		return values