################################################################################
#                                                                              #
#                              csv_translator.py                               #
#                                                                              #
################################################################################
#                                                                              #
#        This is a class for translating Habitat Mapper data.                  #
#                                                                              #
#        Author(s): Abe Megahed                                                #
#                                                                              #
#        This file is subject to the terms and conditions defined in           #
#        'LICENSE.txt', which is part of this source code distribution.        #
#                                                                              #
################################################################################
#        Copyright (C) 2025 - Global Mosquito Observations Dashboard           #
################################################################################

#
# globals
#

schema = 'output_schema.txt'

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
				self.columns.append(line.replace(',', '').replace('REQUIRED', '').replace('MANDATORY', '').strip())

	#
	# csv translating methods
	#

	def get_observation_value(self, key, observation):

		"""
		Get a value with a particular name (key) from an observation.

		Args:
			observation (dict): The observation data.

		Returns:
			object: The value.
		"""

		match key:

			case 'OBJECTID':
				self.count += 1
				return self.count

			case 'title':
				return 'GLOBE Observer Mosquito Habitats'

			case 'dataStreamName':
				return 'Mosquito Habitats ' + observation['mhm_Userid']

			case 'dataStreamDescription':
				return 'Mosquito Habitats as documented by a photo'

			case 'observationType':
				return 'Sensor'

			case 'unitOfCategory':
				return 'Mosquito Habitat, NA, NC'

			case 'phenomenonTime':
				return observation['mhm_MeasuredAt']

			case 'resultTime':
				return observation['mhm_measuredDate']

			case 'result':
				return observation['mhm_WaterSourcePhotoUrls']

			case 'submitTime':
				return observation['mhm_createDate']

			case 'imageStatus':
				return 1 if observation['mhm_WaterSourcePhotoUrls'] else 0

			case 'parameters':
				# return observation['mhm_WaterSourcePhotoUrls']
				return {
					'context': {
						'mhm_elevation': observation['mhm_elevation'], 
						'mhm_WaterSource': observation['mhm_WaterSource']
					}, 
					'Larva Presence': {
						'mhm_LarvaeCount': observation['mhm_LarvaeCount'],
						'mhm_LarvaeCountMagnitude': observation['mhm_LarvaeCountMagnitude'],
						'mhm_LarvaeCountIsRangeFlag': observation['mhm_LarvaeCountIsRangeFlag'],
						'LarvaFullBodyResults': 'GLOBE Observer App', 
						'mhm_LocationMethod': observation['mhm_LocationMethod'],
						'mhm_LocationAccuracyM': observation['mhm_LocationAccuracyM']
					},
					'raw context 1': {
						'mhm_protocol': observation['mhm_protocol'],
						'mhm_updateDate': observation['mhm_updateDate'],
						'mhm_publishDate': observation['mhm_publishDate'],
						'mhm_organizationId': observation['mhm_organizationId'],
						'mhm_countryName': observation['mhm_countryName'],
						'mhm_countryCode': observation['mhm_countryCode'],
						'mhm_elevation': observation['mhm_elevation'],
						'mhm_pid': observation['mhm_pid'],
						'mhm_ExtraData': observation['mhm_ExtraData'],
						'mhm_BreedingGroundEliminated': observation['mhm_BreedingGroundEliminated'],
						# 'AbdomenCloseUpResult': observation['AbdomenCloseUpResult'],
						'mhm_MeasurementElevation': observation['mhm_MeasurementElevation'],
						'mhm_MosquitoEggs': observation['mhm_MosquitoEggs'],
						'mhm_Genus': observation['mhm_Genus'],
						'mhm_MosquitoEggCount': observation['mhm_MosquitoEggCount'],
						'mhm_WaterSource': observation['mhm_WaterSource'],
						'mhm_MosquitoAdults': observation['mhm_MosquitoAdults'],
						'mhm_Species': observation['mhm_Species'],
						'mhm_Comments': observation['mhm_Comments'],
						'mhm_MosquitoPupae': observation['mhm_MosquitoPupae'],
						'mhm_DataSource': observation['mhm_DataSource'],
						'mhm_Latitude': observation['mhm_Latitude'],
						'mhm_LastIdentifyStage': observation['mhm_LastIdentifyStage'],
						'mhm_Longitude': observation['mhm_Longitude'],
						'mhm_WaterSourceType': observation['mhm_WaterSourceType'],
						'mhm_MosquitoHabitatMapperId': observation['mhm_MosquitoHabitatMapperId'],
						'mhm_HasGenus': observation['mhm_HasGenus'],
						'mhm_IsGenusOfInterest': observation['mhm_IsGenusOfInterest'], 
						'mhm_IsWaterSourceContainer': observation['mhm_IsWaterSourceContainer'], 
						'mhm_HasWaterSource': observation['mhm_HasWaterSource']
					}, 
					'raw context 2': {
						'mhm_PhotoCount': observation['mhm_PhotoCount'],  
						'mhm_RejectedCount': observation['mhm_RejectedCount'],   
						'mhm_PendingCount': observation['mhm_PendingCount'],  
						'mhm_PhotoBitBinary': observation['mhm_PhotoBitBinary'],   
						'mhm_PhotoBitDecimal': observation['mhm_PhotoBitDecimal'],  
						'mhm_SubCompletenessScore': observation['mhm_SubCompletenessScore'], 
						'mhm_CumulativeCompletenessScore': observation['mhm_CumulativeCompletenessScore']
					}
				}

			case 'licenseName':
				return 'NA'

			case 'licenseURI':
				return 'https://www.globe.gov/documents/10157/2592674/GLOBE+Data+User+Guide_v1_final.pdf/863a971d-95c5-4dd9-b75c-46713f019088'

			case 'attributionDataSource':
				return 'User: ' + observation['mhm_Userid']

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
				return observation['mhm_siteName']

			case 'locationDescription':
				return observation['mhm_siteId']

			case 'locationEncodingType':
				return 'GeoJSON'

			case 'latitude':
				return observation['mhm_MGRSLatitude']

			case 'longitude':
				return observation['mhm_MGRSLongitude']

			case 'volunteerName':
				return 'User: ' + observation['mhm_Userid']

			case 'volunteerDescription':
				return observation['mhm_organizationName']

			case 'volunteerProperties':
				return observation['mhm_GlobeTeams']

			case 'featureName':
				return observation['mhm_siteName']

			case 'featureDescription':
				return observation['mhm_siteId']

			case 'featureEncodingType':
				return 'GeoJSON'

			case 'featureLocation':
				latitude = observation['mhm_MGRSLatitude']
				longitude = observation['mhm_MGRSLongitude']
				return {
					'location.locationDetails.stationaryProperties.latitude': latitude, 
					'location.locationDetails.stationaryProperties.longitude': longitude
				}

			case 'type':
				return 'Point'

			case 'coordinates':
				latitude = observation['mhm_MGRSLatitude']
				longitude = observation['mhm_MGRSLongitude']
				return [longitude, latitude]

			case 'x':
				return observation['mhm_MGRSLongitude']

			case 'y':
				return observation['mhm_MGRSLatitude']

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