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
				line.replace(',', '').replace('REQUIRED', '').replace('MANDATORY', '').strip()
				if not column.startswith('//'):
					self.columns.append(column)

	#
	# json translating methods
	#

	def get_observation_value(self, key, observation):

		"""
		Get a value with a particular name (key) from an observation.

		Args:
			observation (dict): The observation data.

		Returns:
			object: The value.
		"""

		urls = observation['mosquitohabitatmapperLarvaFullBodyPhotoUrls'] if 'mosquitohabitatmapperLarvaFullBodyPhotoUrls' in observation else None
		photo_count = len(urls.split(',')) if urls else 0
		data = observation['data']

		match key:

			case 'OBJECTID':
				self.count += 1
				return self.count

			case 'title':
				return 'GLOBE Observer Mosquito Habitats'

			case 'dataStreamName':
				return 'Mosquito Habitats ' + str(observation['pid'])

			case 'dataStreamDescription':
				return 'Mosquito Habitats as documented by a photo'

			case 'observationType':
				return 'Sensor'

			case 'unitOfCategory':
				return 'Mosquito Habitat, NA, NC'

			case 'phenomenonTime':
				return data['mosquitohabitatmapperMeasuredAt']

			case 'resultTime':
				return data['mosquitohabitatmapperMeasuredAt']

			case 'result':
				return data['mosquitohabitatmapperWaterSourcePhotoUrls']

			case 'submitTime':
				return data['mosquitohabitatmapperMeasuredAt']

			case 'imageStatus':
				return 1 if data['mosquitohabitatmapperWaterSourcePhotoUrls'] else 0

			case 'parameters':
				return {
					'context': {
						'mhm_elevation': observation['elevation'], 
						'mhm_WaterSource': data['mosquitohabitatmapperWaterSourceType']
					}, 
					'Larva Presence': {
						'mhm_LarvaeCount': data['mosquitohabitatmapperLarvaeCount'],
						'mhm_LarvaeCountMagnitude': '',
						'mhm_LarvaeCountIsRangeFlag': '',
						'LarvaFullBodyResults': 'GLOBE Observer App', 
						'mhm_LocationMethod': data['mosquitohabitatmapperLocationMethod'],
						'mhm_LocationAccuracyM': data['mosquitohabitatmapperLocationAccuracyM']
					},
					'raw context 1': {
						'mhm_protocol': observation['protocol'],
						'mhm_updateDate': observation['updateDate'],
						'mhm_publishDate': observation['publishDate'],
						'mhm_organizationId': observation['organizationId'],
						'mhm_countryName': observation['countryName'],
						'mhm_countryCode': observation['countryCode'],
						'mhm_elevation': observation['elevation'],
						'mhm_pid': observation['pid'],
						'mhm_ExtraData': data['mosquitohabitatmapperExtraData'],
						'mhm_BreedingGroundEliminated': data['mosquitohabitatmapperBreedingGroundEliminated'],
						# 'AbdomenCloseUpResult': observation['AbdomenCloseUpResult'],
						'mhm_MeasurementElevation': data['mosquitohabitatmapperMeasurementElevation'],
						'mhm_MosquitoEggs': data['mosquitohabitatmapperMosquitoEggs'],
						'mhm_Genus': data['mosquitohabitatmapperGenus'],
						'mhm_MosquitoEggCount': data['mosquitohabitatmapperMosquitoEggCount'],
						'mhm_WaterSource': data['mosquitohabitatmapperWaterSource'],
						'mhm_MosquitoAdults': data['mosquitohabitatmapperMosquitoAdults'],
						'mhm_Species': data['mosquitohabitatmapperSpecies'],
						'mhm_Comments': data['mosquitohabitatmapperComments'],
						'mhm_MosquitoPupae': data['mosquitohabitatmapperMosquitoPupae'],
						'mhm_DataSource': data['mosquitohabitatmapperDataSource'],
						'mhm_Latitude': observation['latitude'],
						'mhm_LastIdentifyStage': data['mosquitohabitatmapperLastIdentifyStage'],
						'mhm_Longitude': observation['longitude'],
						'mhm_WaterSourceType': data['mosquitohabitatmapperWaterSourceType'],
						'mhm_MosquitoHabitatMapperId': data['mosquitohabitatmapperMosquitoHabitatMapperId'],
						'mhm_HasGenus': data['mosquitohabitatmapperGenus'],
						'mhm_IsGenusOfInterest': data['mosquitohabitatmapperGenus'], 
						'mhm_IsWaterSourceContainer': data['mosquitohabitatmapperWaterSource'], 
						'mhm_HasWaterSource': data['mosquitohabitatmapperWaterSource'] != ''
					}, 
					'raw context 2': {
						'mhm_PhotoCount': photo_count,  
						'mhm_RejectedCount': '',   
						'mhm_PendingCount': '',  
						'mhm_PhotoBitBinary': '',   
						'mhm_PhotoBitDecimal': '',  
						'mhm_SubCompletenessScore': '', 
						'mhm_CumulativeCompletenessScore': ''
					}
				}

			case 'licenseName':
				return 'NA'

			case 'licenseURI':
				return 'https://www.globe.gov/documents/10157/2592674/GLOBE+Data+User+Guide_v1_final.pdf/863a971d-95c5-4dd9-b75c-46713f019088'

			case 'attributionDataSource':
				return 'User: ' + observation['data']['mosquitohabitatmapperDataSource']

			case 'attributionDataAggregator':
				return "Global Learning and Observations to Benefit the Environment (GLOBE)"

			case 'validationStatus':
				return '1'

			case 'validationMethod':
				return "Our Validation method is as follows: 1) GLOBE Observer App has its own validators to ensure the requested data type matches the received value. 2) GLOBE Observer Team validates the photos to ensure they are useful and match the area where the photographer took the photo. 3) Our pre-processing algorithms ensure values entered are appropriate and reasonable. Our code also creates quality assurance flag to allow Users to better summarize the data."

			case 'validationResult':
				return "FALSE (Entries with their photos undergoing GLOBE's validation process will have a 'pending' code for their photos. NOTE: Some entries' photos will be listed as 'rejected'. Photos that pass our validation process will include GLOBE's URL to that photo)"

			case 'qualityDescription':
				return "GLOBE Observer Data Guide: https://www.globe.gov/documents/10157/2592674/GLOBE+Data+User+Guide_v1_final.pdf/863a971d-95c5-4dd9-b75c-46713f019088 (Page 25)"

			case 'qualityGrade':
				return 'research'

			case 'observedPropertyName':
				return 'Mosquito Habitats'

			case 'observedPropertyDescription':
				return 'Mosquito Habitats as documented by a photo'

			case 'observedPropertyDefinition':
				return 'https://observer.globe.gov/toolkit/mosquito-habitat-mapper-toolkit'

			case 'sensorName':
				return 'NA'

			case 'sensorDescription':
				return 'NA'

			case 'sensorEncodingType':
				return 'NA'

			case 'sensorMetadata':
				return 'NA'

			case 'locationName':
				return observation['siteName']

			case 'locationDescription':
				return observation['siteId']

			case 'locationEncodingType':
				return 'GeoJSON'

			case 'latitude':
				return observation['latitude']

			case 'longitude':
				return observation['longitude']

			case 'volunteerName':
				return observation['organizationId']

			case 'volunteerDescription':
				return observation['organizationName']

			case 'volunteerProperties':
				return ''

			case 'featureName':
				return observation['siteName']

			case 'featureDescription':
				return observation['siteId']

			case 'featureEncodingType':
				return 'GeoJSON'

			case 'featureLocation':
				latitude = observation['latitude']
				longitude = observation['longitude']
				return {
					'location.locationDetails.stationaryProperties.latitude': latitude, 
					'location.locationDetails.stationaryProperties.longitude': longitude
				}

			case 'type':
				return 'Point'

			case 'coordinates':
				latitude = observation['latitude']
				longitude = observation['longitude']
				return [longitude, latitude]

			case 'x':
				return observation['longitude']

			case 'y':
				return observation['latitude']

		return ''

	def get_observation_values(self, observation):

		"""
		Get a set of value from an observation.

		Args:
			observation (dict): The observation data.

		Returns:
			object: The set of values.
		"""

		values = {}
		for column in self.columns:
			value = self.get_observation_value(column, observation)
			values[column] = value
		return values

	def get_observations_values(self, observations):

		"""
		Get array of sets of values from an array of observations.

		Args:
			observation (dict): The observation data.

		Returns:
			object: array of sets of values.
		"""

		values = []
		columns = observations[0]
		for index in range(1, len(observations)):
			observation = observations[index]
			values.append(self.get_observation_values(observation))
		return values
