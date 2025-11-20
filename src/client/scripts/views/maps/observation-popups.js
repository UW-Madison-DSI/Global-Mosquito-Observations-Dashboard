/******************************************************************************\
|                                                                              |
|                            observation-popups.js                             |
|                                                                              |
|******************************************************************************|
|                                                                              |
|        This defines a mixin for showing map observation popups.              |
|                                                                              |
|        Author(s): Abe Megahed                                                |
|                                                                              |
|        This file is subject to the terms and conditions defined in           |
|        'LICENSE.txt', which is part of this source code distribution.        |
|                                                                              |
|******************************************************************************|
|     Copyright (C) 2025, Data Science Institute, University of Wisconsin      |
\******************************************************************************/

import QueryString from '../../utilities/web/query-string.js';
import ShareDialogView from '../../views/dialogs/share-dialog-view.js';
import Browser from '../../utilities/web/browser.js';

export default {

	//
	// attributes
	//

	popupTemplate: _.template(`
		<div class="title"><%= title %></div>
		<hr />
		<% let keys = Object.keys(attributes); %>
		<div class="buttons">
			<button class="social share btn"><i class="fa fa-share"></i>Share</button>
		</div>
		<% for (i = 0; i < keys.length; i++) { %>
		<% let key = keys[i]; %>
		<% let label = keys[i].toTitleCase().replace(/_/g, ' '); %>
		<% let value = attributes[key]; %>
		<% if (value && value != 'None' && key != 'photo_urls' && key != 'thumb_urls' && key != 'captions') { %>
		<div class="value">
			<label><%= label %>:</label>
			<%= value %>
		</div>
		<% } %>
		<% } %>
		<% if (attributes.thumb_urls && attributes.photo_urls.length > 0) { %>
		<hr />
		<div class="photos">
			<% for (let i = 0; i < attributes.photo_urls.length; i++) { %>
			<% let photo_url = attributes.photo_urls[i]; %>
			<% let thumb_url = attributes.thumb_urls[i]; %>
			<% let caption = attributes.captions? attributes.captions[i] : null; %>
			<% if (thumb_url) { %>
			<div class="photo">
				<a style="background-image: url('<%= thumb_url %>');" href="<%= photo_url %>" data-fancybox="gallery" class="lightbox"<% if (caption) { %> data-caption="<%= caption %>"<% } %>>
					<!-- <img class="preview" src="<%= thumb_url %>" /> -->
				</a>
				<% if (caption) { %><label><%= caption %></label><% } %>
			</div>
			<% } %>
			<% } %>
		</div>
		<% } %>
	`),

	//
	// formatting methods
	//

	formatName: function(name) {
		if (!name || name.length == 0) {
			return name;
		}

		let terms = name.split(' ');
		for (let i = 0; i < terms.length; i++) {
			let term = terms[i];
			if (term.toLowerCase() != 'insecta' && !term.endsWith('dae')) {
				terms[i] = '<i>' + term + '</i>';
			}
		}

		return terms.join(' ');
	},

	//
	// ajax functions
	//

	fetchObservation: function(source, id, options) {
		fetch(config.server + '/observations/' + source.replace(/_/g, '-') + '/' + id)
		.then(response => response.json())
		.then(data => {
			if (options && options.success) {
				options.success(data);
			}
		});
	},

	//
	// lightbox methods
	//

	addLightBox: function(element) {
		$(element).find('.lightbox').fancybox({

			// options
			//
			padding: 0,
			margin: 20,
			openEffect: 'elastic',
			closeEffect: 'elastic',
			type : "image",
			autoResize  : true,
			fitToView : true,
			loop: true,

			buttons: [
				"zoom",
				"slideShow",
				"fullScreen",
				"download",
				"thumbs",
				"close"
			]
		});
	},

	//
	// popup methods
	//

	hasNonNullObject: function(object) {
		let keys = Object.keys(object);
		for (let i = 0; i < keys.length; i++) {
			let key = keys[i];
			if (object[key] != null) {
				return true;
			}
		}
		return false;
	},

	getHabitatMapperPopupData: function(data) {
		return {
			title: 'Habitat Mapper',
			attributes: {
				date: new Date(data.mhm_measuredDate).toLocaleDateString(),
				time: new Date(data.mhm_measuredDate).toTimeString(),
				site: data.mhm_siteName,
				genus: this.formatName(data.mhm_Genus),
				species: this.formatName(data.mhm_Species),
				location: [data.y, data.x],
				habitat_type: data.mhm_WaterSourceType,
				habitat: data.mhm_WaterSource,
				thumb_urls: data.mhm_LarvaFullBodyPhotoUrls.concat(data.mhm_WaterSourcePhotoUrls),
				photo_urls: data.mhm_LarvaFullBodyPhotoUrls.concat(data.mhm_WaterSourcePhotoUrls)
			}
		};
	},

	getiNaturalistPopupData: function(data) {
		return {
			title: 'iNaturalist',
			attributes: {
				date: new Date(data.observationResCatObsPheTime).toLocaleDateString(),
				time: new Date(data.observationResCatObsPheTime).toTimeString(),
				location: [data.y, data.x],
				genus: this.formatName(data.Indentified_by_Human),
				common_name: data.ObsCPCommonName,
				thumb_urls: data.observationImaImaResult.map((result) => {
					return result.photo.url
				}),
				photo_urls: data.observationImaImaResult.map((result) => {
					return result.photo.url.replace('square', 'original');
				})
			}
		};
	},

	getLandCoverPopupData: function(data) {
		return {
			title: 'Land Cover',
			attributes: {
				date: new Date(data.phenomenonTime).toLocaleDateString(),
				time: new Date(data.phenomenonTime).toTimeString(),
				location: [data.y, data.x],
				thumb_urls: data.imageResult && this.hasNonNullObject(data.imageResult)? [
					data.imageResult.lc_NorthPhotoUrl,
					data.imageResult.lc_SouthPhotoUrl,
					data.imageResult.lc_EastPhotoUrl,
					data.imageResult.lc_WestPhotoUrl,
					data.imageResult.lc_UpwardPhotoUrl,
					data.imageResult.lc_DownwardPhotoUrl
				] : [],
				photo_urls: data.imageResult && this.hasNonNullObject(data.imageResult)? [
					data.imageResult.lc_NorthPhotoUrl,
					data.imageResult.lc_SouthPhotoUrl,
					data.imageResult.lc_EastPhotoUrl,
					data.imageResult.lc_WestPhotoUrl,
					data.imageResult.lc_UpwardPhotoUrl,
					data.imageResult.lc_DownwardPhotoUrl
				] : [],
				captions: [
					"North",
					"South",
					"East",
					"West",
					"Up",
					"Down"
				]
			}
		};
	},

	getMosquitoAlertPopupData: function(data) {
		return {
			title: 'Mosquito Alert',
			attributes: {
				date: new Date(data.observationResCatObsPheTime).toLocaleDateString(),
				time: new Date(data.observationResCatObsPheTime).toTimeString(),
				site: data.locationName,
				location: [data.y, data.x],
				species: this.formatName(data.Indentified_by_Human),
				'adult, bite, or site': data.dataStreamDescription,
				research_grade: data.omPrcoessResQuaQuaGrade,
				thumb_urls: data.observationImaImaResult? [data.observationImaImaResult] : null,
				photo_urls: data.observationImaImaResult? [data.observationImaImaResult] : null
			}
		}
	},

	getPopupData: function(source, data) {
		switch (source) {
			case 'habitat_mapper':
				return this.getHabitatMapperPopupData(data);
			case 'inaturalist':
				return this.getiNaturalistPopupData(data);
			case 'land_cover':
				return this.getLandCoverPopupData(data);
			case 'mosquito_alert':
				return this.getMosquitoAlertPopupData(data);
			default:
				alert("Unknown data source.")
		}
	},

	showMarkerPopup: function(marker, data) {
		let html = this.popupTemplate(this.getPopupData(marker.options.source, data));

		// select marker
		//
		$(marker._path || marker._icon).addClass('selected');

		// save selected item
		//
		QueryString.add('selected', marker.options.id);

		// open popup
		//
		marker.bindPopup(html).openPopup();

		// hide UI toolbars
		//
		if (Browser.is_mobile) {
			$('#user-interface').hide();
		}

		// get popup element
		//
		let popup = marker.getPopup();
		let element = popup.getElement();

		// add share button action
		//
		$(element).find('.share').click(() => {
			application.show(new ShareDialogView({
				link: window.location
			}));
		});

		// add lightbox to popup images
		//
		if (popup && popup.isOpen()) {
			this.addLightBox(element);
		}

		// show UI toolbars on close
		//
		popup.on('remove', () => {
			if (Browser.is_mobile) {
				$('#user-interface').show();
			}

			// deselect marker
			//
			$(marker._path || marker._icon).removeClass('selected');

			// clear selected item
			//
			QueryString.remove('selected');
		});
	},

	addObservationPopup: function(marker) {
		this.fetchObservation(marker.options.source, marker.options.id, {

			// callbacks
			//
			success: (data) => {
				this.showMarkerPopup(marker, data)
			}
		});
	}
}