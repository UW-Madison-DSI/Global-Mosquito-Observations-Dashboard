/******************************************************************************\
|                                                                              |
|                               stats-view.js                                  |
|                                                                              |
|******************************************************************************|
|                                                                              |
|        This defines a sidebar information panel view.                        |
|                                                                              |
|        Author(s): Abe Megahed                                                |
|                                                                              |
|        This file is subject to the terms and conditions defined in           |
|        'LICENSE.txt', which is part of this source code distribution.        |
|                                                                              |
|******************************************************************************|
|     Copyright (C) 2025, Data Science Institute, University of Wisconsin      |
\******************************************************************************/

import BaseView from '../../views/base-view.js';
import QueryString from '../../utilities/web/query-string.js';

export default BaseView.extend({

	//
	// attributes
	//

	template: _.template(`
		<div class="habitat-mapper">
			<div class="swatch"></div>
			Habitat Mapper <span class="count"></span>
		</div>
		<div class="inaturalist">
			<div class="swatch"></div>
			iNaturalist <span class="count"></span>
		</div>
		<div class="land-cover">
			<div class="swatch"></div>
			Land Cover <span class="count"></span>
		</div>
		<div class="mosquito-alert">
			<div class="swatch"></div>
			Mosquito Alert <span class="count"></span>
		</div>
	`),

	//
	// ajax methods
	//

	fetchObservationsCount: function(source, options) {

		// compose url
		//
		let url = config.server + '/observations/' + source.replace(/_/g, '-') + '/num';
		if (options.data) {
			let queryString = QueryString.encode(options.data);
			if (queryString) {
				url += '?' + queryString;
			}
		}

		// fetch data
		//
		fetch(url)
		.then(response => response.text())
		.then(count => {
			if (options && options.success) {
				options.success(parseInt(count));
			}
		});
	},

	showObservationCount: function(source) {
		this.fetchObservationsCount(source, {

			// filter parameters
			//
			data: {
				countries: QueryString.value('countries'),
				before: QueryString.value('before'),
				after: QueryString.value('after'),
				genera: QueryString.value('genera'),
				species: QueryString.value('species')
			},

			// callbacks
			//
			success: (count) => {
				this.$el.find('.' + source.replace(/_/g, '-') + ' .count').text('(' + count.toLocaleString() + ')');
			}
		});
	},

	//
	// rendering methods
	//

	onRender: function() {
		this.showObservationCount('habitat_mapper');
		this.showObservationCount('inaturalist');
		this.showObservationCount('land_cover');
		this.showObservationCount('mosquito_alert');
	}
});