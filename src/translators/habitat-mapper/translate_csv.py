################################################################################
#                                                                              #
#                               translate_csv.py                               #
#                                                                              #
################################################################################
#                                                                              #
#        This is a utility for parsing Habitat Mapper data.                    #
#                                                                              #
#        Author(s): Abe Megahed                                                #
#                                                                              #
#        This file is subject to the terms and conditions defined in           #
#        'LICENSE.txt', which is part of this source code distribution.        #
#                                                                              #
################################################################################
#        Copyright (C) 2025 - Global Mosquito Observations Dashboard           #
################################################################################

import sys
import json
import csv
import uuid
from csv_translator import HabitatMapperTranslator

#
# globals
#

translator = HabitatMapperTranslator()

#
# utility functions
#

def read_file(filename):
	with open(filename, 'r') as file:
		data = file.read()
	return data

def read_observations_from_rows(rows):
	observations = []
	index = 0
	columns = []
	for row in rows:
		index += 1
		if index == 1:
			columns = row
			print("num columns = ", len(columns))
			print("columns = ", columns)
			exit()
		else:
			values = {}
			for i in range(0, len(row)):
				column = columns[i]
				# print("columns = ", column)
				values[columns[i]] = row[i]
			observations.append(values)
	return observations

def read_observations_from_file(filename):
	observations = []
	with open(filename) as csvfile:
		reader = csv.reader(csvfile)
		index = 0
		columns = []
		for row in reader:
			index += 1
			if index == 1:
				columns = row
			else:
				values = {}
				for i in range(0, len(row)):
					values[columns[i]] = row[i]
				observations.append(values)
	return observations

#
# output functions
#

def write_csv(filename, observations):
	with open(filename, 'w', newline='') as file:
		writer = csv.writer(file)

		# add headers
		#
		writer.writerow(Translator.columns)

		# add columns
		#
		for observation in observations:
			writer.writerow(translator.get_observation_values(observation))

################################################################################
#                                     main                                     #
################################################################################

if __name__ == '__main__':

	# parse arguments
	#
	if (len(sys.argv) < 3):
		print("Usage: python3 parser.py <input-file-name> <output-file-name");
		exit();

	# get command line arguments
	#
	filename = sys.argv[1]
	outfilename = sys.argv[2]

	# parse observations
	#
	observations = read_observations_from_file(filename)

	# write transformed data to csv file
	#
	write_csv(outfilename, observations)