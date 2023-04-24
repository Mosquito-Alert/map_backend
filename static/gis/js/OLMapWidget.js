/* global ol */
'use strict';
function GeometryTypeControl(opt_options) {
    // Map control to switch type when geometry type is unknown
    const options = opt_options || {};

    const element = document.createElement('div');
    element.className = 'switch-type type-' + options.type + ' ol-control ol-unselectable';
    if (options.active) {
        element.classList.add("type-active");
    }

    const self = this;
    const switchType = function(e) {
        e.preventDefault();
        if (options.widget.currentGeometryType !== self) {
            options.widget.map.removeInteraction(options.widget.interactions.draw);
            options.widget.interactions.draw = new ol.interaction.Draw({
                features: options.widget.featureCollection,
                type: options.type
            });
            options.widget.map.addInteraction(options.widget.interactions.draw);
            options.widget.currentGeometryType.element.classList.remove('type-active');
            options.widget.currentGeometryType = self;
            element.classList.add("type-active");
        }
    };

    element.addEventListener('click', switchType, false);
    element.addEventListener('touchstart', switchType, false);

    ol.control.Control.call(this, {
        element: element
    });
};
ol.inherits(GeometryTypeControl, ol.control.Control);

// TODO: allow deleting individual features (#8972)
{
    const jsonFormat = new ol.format.GeoJSON();
    function MapWidget(options) {
        var _this = this;
        this.map = null;
        this.progress = new Progress(document.getElementById('progress')),
        this.layers = null;
        this.interactions = {draw: null};
        this.typeChoices = false;
        this.ready = false;
        this.version = ''
        // this.bbox_layer = new ol.layer.Vector({
        //     source: new ol.source.Vector()
        // });

        // Default options
        this.options = {
            default_lat: 41,
            default_lon: 2.5,
            default_zoom: 4,
            is_collection: options.geom_name.includes('Multi') || options.geom_name.includes('Collection')
        };

        // Altering using user-provided options
        for (const property in options) {
            if (options.hasOwnProperty(property)) {
                this.options[property] = options[property];
            }
        }
        if (!options.base_layer) {
            this.options.base_layer = new ol.layer.Tile({source: new ol.source.OSM()});
        }

        this.map = this.createMap();
        this.map.getView().setCenter(this.defaultCenter());
        this.ready = true;
        this.progress.el.addEventListener('loadEnd', function(e){
            _this.options.wmsLoadedCallback()
        })
    }

    MapWidget.prototype.createMap = function() {
        var _this = this;
        const map = new ol.Map({
            target: this.options.map_id,
            layers: [this.options.base_layer],
            view: new ol.View({
                zoom: this.options.default_zoom,
            }),
            controls: new ol.control.defaults().extend([new ol.control.FullScreen()])
        });
        return map;
    };

    MapWidget.prototype.drawBbox = function() {
        var _this = this;
        this.bbox_layer.getSource().clear();
        this.map.removeInteraction(this.draw);
        this.draw = new ol.interaction.Draw({
            source: _this.bbox_layer.getSource(),
            type: 'Circle',
            geometryFunction: ol.interaction.Draw.createBox(),
        });
        this.map.addInteraction(this.draw);
        // this.map.addLayer(this.bbox_layer);
        this.draw.on('drawend', function (e) {
            _this.map.removeInteraction(_this.draw)
            console.log(e.feature.getGeometry().getCoordinates())
            setBBOX (e.feature.getGeometry().getCoordinates())
        });
    };

    MapWidget.prototype.getLayerExtent = async function(layerName) {
        let myLayer
        let extent3758
        var _this = this
        try {
            _this.layers.forEach(layer => {
                if (layer.Name === layerName) {
                    myLayer = layer
                }
            })
            if (!myLayer) {
                console.log('Layer does not exist')
            }
            const bboxes = myLayer.BoundingBox
            const bboxWGS = bboxes.find(bbox => {
                return (bbox.crs.toUpperCase() === 'CRS:84' || bbox.crs.toUpperCase() === 'EPSG:4326')
            })
            var layerExtent = bboxWGS.extent
            extent3758 = ol.proj.transformExtent(layerExtent, 'EPSG:4326', 'EPSG:3857');
        } catch (err){
            console.log(extent3758)
        }
        return extent3758
    }

    MapWidget.prototype.getLayersName = async function(url) {
        var info = {success: true}
        if (!this.layers) {
            info = await this.getWMSLayers(url)
            if (info.success){
                this.layers = info.response
            }
        }

        if (info.success) {
            var str ='<div class="list-group">'
            this.layers.forEach(l => {
                str += '<a href="#" class="list-group-item" onclick="setLayer(\'' + l.Name + '\')">' + l.Name +'</a>'
            })
            str+='</div>'
            info.response = str
        }
        return info
    }

    MapWidget.prototype.getWMSLayers = async function(url) {
        var _this = this
        var result, res, status, statusText

        const parser = new ol.format.WMSCapabilities();
        try {
            await fetch(url + '?request=GetCapabilities&service=wms&version=1.3.0')
                .then(function (response) {
                    status = response.status
                    statusText = response.statusText
                    return response.text();
                })
                .then(function (text) {
                    if (status == 200){
                        try {
                            result = parser.read(text);
                            _this.version = result.version
                            res = {success: true, response: result.Capability.Layer.Layer}
                        } catch (err){
                            res = {success: false, response: err}
                        }
                    } else {
                        res = {success: false, response: statusText}
                    }
                })
                .catch(function(err){
                    res = {success: false, response: err}
                })
        } catch (e) {
            res = {success:false, response: e}
        }
        return res
    }

    MapWidget.prototype.reloadWms = async function(url, layerName, bbox) {
        const _this = this
        let layerExtent = null
        this.map.removeLayer(this.wmsLayer)
        if (!this.layers) {
            const info = await this.getWMSLayers(url)
            if (info.success) {
                this.layers = info.response
            } else {
                alert('WMS Server not found!')
                return
            }
        }

        var wmsSource = new ol.source.TileWMS({
            projection: 'EPSG:3857',
            url: url,
            params: {
                'LAYERS': layerName,
                'SRS': 'EPSG:3857'
            }
        })

        this.wmsLayer = new ol.layer.Tile({
            source: wmsSource
        })

        wmsSource.on('tileloadstart', function () {
            _this.progress.addLoading();
        });
        wmsSource.on(['tileloadend', 'tileloaderror'], function () {
            _this.progress.addLoaded();
        });

        this.map.addLayer(this.wmsLayer)
        // Cal mirar si s'agafa el bbox del wms o si s'ha dibuixat al mapa
        if (!bbox) {
            // Get bbox from WMS Server
            var wmsExtent = await this.getLayerExtent(layerName)
            if (wmsExtent) {
                // document.getElementById('my-widget-extent').value = wmsExtent.join(',')
                this.map.getView().fit(wmsExtent);
                var feature = featureFromBbox(wmsExtent)
                // _this.bbox_layer.getSource().clear()
                // _this.bbox_layer.getSource().addFeature( feature );
            } //else {
            //     document.getElementById('my-widget-extent').value = ''
            // }
        } else {
            // Get bbox from DDBB
            var feature = featureFromBbox(bbox);
            this.map.getView().fit(bbox);
            // _this.bbox_layer.getSource().clear()
            // _this.bbox_layer.getSource().addFeature( feature );
        }
    }

    function featureFromBbox(coords) {
        var box = new ol.geom.Polygon( [[
            [coords[0],coords[1]],
            [coords[0],coords[3]],
            [coords[2],coords[3]],
            [coords[2],coords[1]]
        ]]);
        var feature = new ol.Feature({
            name: "bbox",
            geometry: box
        });
        return feature;
    }
    MapWidget.prototype.removeBBOX = function() {
        this.bbox_layer.getSource().clear()
    }

    MapWidget.prototype.createInteractions = function() {
        // Initialize the modify interaction
        this.interactions.modify = new ol.interaction.Modify({
            features: this.featureCollection,
            deleteCondition: function(event) {
                return ol.events.condition.shiftKeyOnly(event) &&
                    ol.events.condition.singleClick(event);
            }
        });

        // Initialize the draw interaction
        let geomType = this.options.geom_name;
        if (geomType === "Geometry" || geomType === "GeometryCollection") {
            // Default to Point, but create icons to switch type
            geomType = "Point";
            this.currentGeometryType = new GeometryTypeControl({widget: this, type: "Point", active: true});
            this.map.addControl(this.currentGeometryType);
            this.map.addControl(new GeometryTypeControl({widget: this, type: "LineString", active: false}));
            this.map.addControl(new GeometryTypeControl({widget: this, type: "Polygon", active: false}));
            this.typeChoices = true;
        }
        this.interactions.draw = new ol.interaction.Draw({
            features: this.featureCollection,
            type: geomType
        });

        this.map.addInteraction(this.interactions.draw);
    };

    MapWidget.prototype.defaultCenter = function() {
        const center = [this.options.default_lon, this.options.default_lat];
        if (this.options.map_srid) {
            return ol.proj.transform(center, 'EPSG:4326', this.map.getView().getProjection());
        }
        return center;
    };

    MapWidget.prototype.enableDrawing = function() {
        this.interactions.draw.setActive(true);
        if (this.typeChoices) {
            // Show geometry type icons
            const divs = document.getElementsByClassName("switch-type");
            for (let i = 0; i !== divs.length; i++) {
                divs[i].style.visibility = "visible";
            }
        }
    };

    MapWidget.prototype.disableDrawing = function() {
        if (this.interactions.draw) {
            this.interactions.draw.setActive(false);
            if (this.typeChoices) {
                // Hide geometry type icons
                const divs = document.getElementsByClassName("switch-type");
                for (let i = 0; i !== divs.length; i++) {
                    divs[i].style.visibility = "hidden";
                }
            }
        }
    };

    MapWidget.prototype.clearFeatures = function() {
        this.featureCollection.clear();
        // Empty textarea widget
        document.getElementById(this.options.id).value = '';
        this.enableDrawing();
    };

    MapWidget.prototype.serializeFeatures = function() {
        // Three use cases: GeometryCollection, multigeometries, and single geometry
        let geometry = null;
        const features = this.featureOverlay.getSource().getFeatures();
        if (this.options.is_collection) {
            if (this.options.geom_name === "GeometryCollection") {
                const geometries = [];
                for (let i = 0; i < features.length; i++) {
                    geometries.push(features[i].getGeometry());
                }
                geometry = new ol.geom.GeometryCollection(geometries);
            } else {
                geometry = features[0].getGeometry().clone();
                for (let j = 1; j < features.length; j++) {
                    switch (geometry.getType()) {
                    case "MultiPoint":
                        geometry.appendPoint(features[j].getGeometry().getPoint(0));
                        break;
                    case "MultiLineString":
                        geometry.appendLineString(features[j].getGeometry().getLineString(0));
                        break;
                    case "MultiPolygon":
                        geometry.appendPolygon(features[j].getGeometry().getPolygon(0));
                    }
                }
            }
        } else {
            if (features[0]) {
                geometry = features[0].getGeometry();
            }
        }
        document.getElementById(this.options.id).value = jsonFormat.writeGeometry(geometry);
    };

    window.MapWidget = MapWidget;
}
