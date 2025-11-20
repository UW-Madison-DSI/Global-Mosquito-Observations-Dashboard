/******************************************************************************\
|                                                                              |
|                             mosquito-map-view.js                             |
|                                                                              |
|******************************************************************************|
|                                                                              |
|        This defines a map view of mosquito observations.                     |
|                                                                              |
|        Author(s): Abe Megahed                                                |
|                                                                              |
|        This file is subject to the terms and conditions defined in           |
|        'LICENSE.txt', which is part of this source code distribution.        |
|                                                                              |
|******************************************************************************|
|     Copyright (C) 2025, Data Science Institute, University of Wisconsin      |
\******************************************************************************/

import BaseMapView from '../../views/maps/base-map-view.js';
import DataBarView from '../../views/toolbars/data-bar-view.js';
import ViewBarView from '../../views/toolbars/view-bar-view.js';
import ObservationPopups from '../../views/maps/observation-popups.js';
import Browser from '../../utilities/web/browser.js';
import QueryString from '../../utilities/web/query-string.js';
import '../../utilities/scripting/string-utils.js';

export default BaseMapView.extend(_.extend({}, ObservationPopups, {

	//
	// attributes
	//

	icons: {},

	template: _.template(`
		<div id="map"></div>

		<div id="user-interface" class="full-screen overlay">
			<div id="map-bar"></div>
			<div id="zoom-bar"></div>
			<div id="data-bar"></div>
			<div id="view-bar"></div>
		</div>
	`),

	regions: {
		map: {
			el: '#map-bar',
			replaceElement: true
		},
		zoom: {
			el: '#zoom-bar',
			replaceElement: true
		},
		data: {
			el: '#data-bar',
			replaceElement: true
		},
		view: {
			el: '#view-bar',
			replaceElement: true
		}
	},

	sources: [
		'habitat_mapper',
		'land_cover',
		'inaturalist',
		'mosquito_alert'
	],

	//
	// ajax methods
	//

	fetchObservations: function(source, options) {

		// compose url
		//
		let url = config.server + '/observations/' + source.replace(/_/g, '-');
		if (options.data) {
			let queryString = QueryString.encode(options.data);
			if (queryString) {
				url += '?' + queryString;
			}
		}

		// fetch data
		//
		fetch(url)
		.then(response => response.json())
		.then(data => {
			if (options && options.success) {
				options.success(data);
			}
		});
	},

	//
	// mapping functions
	//

	getClusterGroup: function(source) {
		return L.markerClusterGroup({
			options: Object.assign(L.MarkerClusterGroup.prototype.options, defaults.clustering),

			iconCreateFunction: function (cluster) {
				const markers = cluster.getAllChildMarkers();
				const numMarkers = markers.length;
				const iconSize = Math.trunc(15 + Math.log10(numMarkers) * 6);

				return new L.DivIcon({
					html: `<div>${numMarkers}</div>`,
					className: source.replace(/_/g, '-') + ' cluster',
					iconSize: new L.Point(iconSize, iconSize)
				});
			}
		});
	},

	getClusterGroups: function(sources) {
		let clusterGroups = {};
		for (let i = 0; i < sources.length; i++) {
			let source = sources[i];
			clusterGroups[source] = this.getClusterGroup(source);
		}
		return clusterGroups;
	},

	addMapMarkers: function(map, source, observations, selected) {

		// store markers
		//
		this.markers = {};

		for (let i = 0; i < observations.length; i++) {
			let observation = observations[i];

			// get marker icon
			//
			if (!this.icons[source]) {
				this.icons[source] = new L.DivIcon({
					html: `<div></div>`,
					className: source.replace(/_/g, '-') + ' marker',
					iconSize: Browser.is_mobile? defaults.map.markerSize.mobile : defaults.map.markerSize.desktop
				});
			}
			let icon = this.icons[source];

			// create marker
			//
			let marker = L.marker([observation.y, observation.x], {
				icon: icon,
				source: source,
				id: observation.id
			});

			// save reference to marker
			//
			this.markers[observation.id] = marker;

			// add marker popup on click
			//
			marker.on('click', () => {
				this.addObservationPopup(marker);
			});

			// show selected marker
			//
			if (observation.id == selected) {
				this.addObservationPopup(marker);
			}

			// add marker to map
			//
			marker.addTo(map);
		}
	},

	addClusteredMarkers: function(clusterGroup, source, observations, selected) {

		// store markers
		//
		if (!this.markers) {
			this.markers = {};
		}

		for (let i = 0; i < observations.length; i++) {
			let observation = observations[i];
			if (observation.x && observation.y) {

				let marker = L.circleMarker([observation.y, observation.x], {
					source: source,
					id: observation.id,
					radius: Browser.is_mobile? defaults.map.markerSize.mobile / 2: defaults.map.markerSize.desktop / 2,
					className: source.replace(/_/g, '-') + ' marker',
				});

				/*
				// get marker icon
				//
				if (!this.icons[source]) {
					this.icons[source] = new L.DivIcon({
						html: `<div></div>`,
						className: source.replace(/_/g, '-') + ' marker',
						iconSize: Browser.is_mobile? defaults.map.markerSize.mobile : defaults.map.markerSize.desktop
					});
				}
				let icon = this.icons[source];

				// create marker
				//
				let marker = L.marker([observation.y, observation.x], {
					icon: icon,
					source: source,
					id: observation.id
				});
				*/

				// save reference to marker
				//
				this.markers[observation.id] = marker;

				// add marker popup on click
				//
				marker.on('click', () => {
					this.addObservationPopup(marker);
				});

				// show selected marker
				//
				if (observation.id == selected) {
					this.addObservationPopup(marker);
				}

				// add marker to cluster
				//
				clusterGroup.addLayer(marker);
			}
		}
	},

	removeMarkers: function() {
		if (this.clusterGroups) {
			for (const source in this.clusterGroups) {
				let clusterGroup = this.clusterGroups[source];
				clusterGroup.clearLayers();
				this.map.removeLayer(clusterGroup);
			}
		}
	},

	showDataSource: function(dataSource) {
		this.$el.find('#map').removeClass('hide-' + dataSource);
	},

	hideDataSource: function(dataSource) {
		this.$el.find('#map').addClass('hide-' + dataSource);
	},

	//
	// rendering functions
	//

	addObservationMarkers: function(clusterGroup, source) {
		let selected = QueryString.value('selected');

		this.fetchObservations(source, {

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
			success: (observations) => {
				// this.addMarkers(map, source, observations, selected);
				this.addClusteredMarkers(clusterGroup, source, observations, selected);
			}
		});
	},

	showClusteredMarkers: function() {

		// create new cluster group, if necessary
		//
		if (!this.clusterGroups) {
			this.clusterGroups = this.getClusterGroups(this.sources);
		}

		// add cluster to map
		//

		for (let i = 0; i < this.sources.length; i++) {
			let source = this.sources[i];
			let clusterGroup = this.clusterGroups[source];
			this.map.addLayer(clusterGroup);
			this.addObservationMarkers(clusterGroup, source);
		}
	},

	onAttach: function() {

		// call superclass method
		//
		BaseMapView.prototype.onAttach.call(this);

		// add markers
		//
		this.update();
	},

	update: function() {
		this.removeMarkers();
		this.showClusteredMarkers();
	},

	//
	// toolbar rendering methods
	//

	showToolbar: function(kind) {
		switch (kind) {
			case 'map':
				this.showMapBar();
				break;
			case 'zoom':
				this.showZoomBar();
				break;
			case 'data':
				this.showDataBar();
				break;
			case 'view':
				this.showViewBar();
				break;
		}
	},

	showDataBar: function() {
		this.showChildView('data', new DataBarView({
			parent: this
		}));
	},

	showViewBar: function() {
		this.showChildView('view', new ViewBarView({
			parent: this
		}));
	}
}));