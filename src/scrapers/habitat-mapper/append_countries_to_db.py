################################################################################
#                                                                              #
#                          append_countries_to_db.py                           #
#                                                                              #
################################################################################
#                                                                              #
#        This is a script for adding info to the iNaturalist database.         #
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
import config
import mysql.connector
from utilities.inaturalist_observation import iNaturalistObservation

#
# globals
#

db = {
	'host': config.DB_HOST,
	'port': config.DB_PORT,
	'username': config.DB_USERNAME,
	'password': config.DB_PASSWORD,
	'database': config.DB_DATABASE	
}

################################################################################
#                                     main                                     #
################################################################################

if __name__ == '__main__':
	connection = None

	# connect to database
	#
	try:
		connection = mysql.connector.connect(
			host = db['host'],
			port = db['port'],
			username = db['username'],
			password = db['password'],
			database = db['database']
		)
	except Exception as e:
		print("Could not connect to database.")
		logging.exception(str(e))
		print(str(e))

	# parse arguments
	#
	if (len(sys.argv) < 2):
		print("Usage: python3 add_countries_to_db.py");
		exit();
	
