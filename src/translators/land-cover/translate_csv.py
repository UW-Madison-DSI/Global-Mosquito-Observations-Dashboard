################################################################################
#                                                                              #
#                              translate_csv.py                                #
#                                                                              #
################################################################################
#                                                                              #
#        This is a utility for translating Land Cover csv data.                #
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
import sys
import json
import csv
from csv_translator import LandCoverTranslator

#
# globals
#

translator = LandCoverTranslator()

#
# utility functions
#

def read_file(filename):
	with open(filename, 'r') as file:
		data = file.read()
	return data

#
# output functions
#

def write_csv(filename, observations):
	with open(filename, 'w', newline='') as file:
		writer = csv.writer(file)

		# add headers
		#
		writer.writerow(translator.columns)

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

	# parse data from observations
	#
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

	# write transformed data to csv file
	#
	write_csv(outfilename, observations)