/**
 * TheHUB Event Map Handler
 *
 * Interactive map component using Leaflet.js for displaying
 * GPX tracks, segments, and POI markers.
 *
 * @requires Leaflet.js
 * @since 2025-12-09
 */

/**
 * EventMap Class
 * Manages a single event map instance
 */
class EventMap {
    /**
     * Create an EventMap instance
     * @param {string} containerId - The map container element ID
     * @param {Object} mapData - Map data from the server
     */
    constructor(containerId, mapData) {
        this.containerId = containerId;
        this.data = mapData;
        this.map = null;
        this.layers = {
            segments: null,
            pois: null
        };
        this.userLocationMarker = null;
        this.userAccuracyCircle = null;
        this.watchId = null;

        this.init();
    }

    /**
     * Initialize the map
     */
    init() {
        this.createMap();
        this.addSegments();
        this.addPois();
        this.createElevationProfile();
        this.setupInteractions();
    }

    /**
     * Create the Leaflet map instance
     */
    createMap() {
        // Initialize Leaflet map
        this.map = L.map(this.containerId, {
            zoomControl: true,
            scrollWheelZoom: false,
            attributionControl: true
        });

        // Add tile layer (OpenStreetMap)
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
            maxZoom: 19
        }).addTo(this.map);

        // Fit to bounds
        if (this.data.bounds && this.data.bounds.length === 2) {
            this.map.fitBounds(this.data.bounds, { padding: [30, 30] });
        }
    }

    /**
     * Add track segments to the map
     */
    addSegments() {
        const segmentFeatures = this.data.geojson.features.filter(
            f => f.properties.type === 'segment'
        );

        if (segmentFeatures.length === 0) return;

        this.layers.segments = L.geoJSON({
            type: 'FeatureCollection',
            features: segmentFeatures
        }, {
            style: (feature) => ({
                color: feature.properties.color,
                weight: 4,
                opacity: 0.85,
                lineCap: 'round',
                lineJoin: 'round'
            }),
            onEachFeature: (feature, layer) => {
                const props = feature.properties;
                const typeLabel = props.segment_type === 'stage' ? 'Tavlingsstracka' : 'Transport';
                const popupContent = `
                    <div class="event-map-popup">
                        <strong>${props.name || 'Segment ' + props.sequence}</strong>
                        <p>
                            ${typeLabel}<br>
                            ${props.distance_km} km
                            ${props.segment_type === 'stage' ? ` &bull; +${props.elevation_gain}m` : ''}
                        </p>
                    </div>
                `;
                layer.bindPopup(popupContent);

                // Hover effects
                layer.on('mouseover', () => {
                    layer.setStyle({ weight: 6, opacity: 1 });
                    this.highlightSegmentInList(props.id);
                });

                layer.on('mouseout', () => {
                    layer.setStyle({ weight: 4, opacity: 0.85 });
                    this.unhighlightSegmentInList(props.id);
                });
            }
        }).addTo(this.map);

        // Add start/finish markers
        this.addStartFinishMarkers();
    }

    /**
     * Add start and finish markers
     */
    addStartFinishMarkers() {
        const segments = this.data.segments;
        if (!segments || segments.length === 0) return;

        // Start marker
        const firstSegment = segments[0];
        if (firstSegment.coordinates && firstSegment.coordinates.length > 0) {
            const startCoord = firstSegment.coordinates[0];

            const startIcon = L.divIcon({
                className: 'event-map-marker event-map-marker-start',
                html: '<div class="event-map-marker-inner">START</div>',
                iconSize: [60, 24],
                iconAnchor: [30, 12]
            });

            L.marker([startCoord.lat, startCoord.lng], { icon: startIcon })
                .addTo(this.map);
        }

        // Finish marker
        const lastSegment = segments[segments.length - 1];
        if (lastSegment.coordinates && lastSegment.coordinates.length > 0) {
            const finishCoord = lastSegment.coordinates[lastSegment.coordinates.length - 1];

            const finishIcon = L.divIcon({
                className: 'event-map-marker event-map-marker-finish',
                html: '<div class="event-map-marker-inner">MAL</div>',
                iconSize: [50, 24],
                iconAnchor: [25, 12]
            });

            L.marker([finishCoord.lat, finishCoord.lng], { icon: finishIcon })
                .addTo(this.map);
        }
    }

    /**
     * Add POI markers to the map
     */
    addPois() {
        const poiFeatures = this.data.geojson.features.filter(
            f => f.properties.type === 'poi'
        );

        if (poiFeatures.length === 0) return;

        this.layers.pois = L.geoJSON({
            type: 'FeatureCollection',
            features: poiFeatures
        }, {
            pointToLayer: (feature, latlng) => {
                const props = feature.properties;

                const icon = L.divIcon({
                    className: 'event-map-poi-icon',
                    html: `<div class="event-map-poi-pin" style="background: ${props.color}">${props.emoji}</div>`,
                    iconSize: [32, 40],
                    iconAnchor: [16, 40],
                    popupAnchor: [0, -40]
                });

                return L.marker(latlng, { icon: icon });
            },
            onEachFeature: (feature, layer) => {
                const props = feature.properties;
                const popupContent = `
                    <div class="event-map-popup">
                        <strong>${props.emoji} ${props.label}</strong>
                        ${props.description ? `<p>${props.description}</p>` : ''}
                    </div>
                `;
                layer.bindPopup(popupContent);
            }
        }).addTo(this.map);
    }

    /**
     * Create elevation profile canvas
     * Uses full track data with segment positions for correct coloring
     */
    createElevationProfile() {
        const canvas = document.getElementById(this.containerId + '-elevation');
        if (!canvas) return;

        // Prefer new elevation_profile data if available
        if (this.data.elevation_profile && this.data.elevation_profile.waypoints) {
            this.drawElevationFromProfile(canvas, this.data.elevation_profile);
            return;
        }

        // Fallback to old method for backwards compatibility
        if (!this.data.segments) return;

        const elevationPoints = [];
        let cumulativeDistance = 0;

        this.data.segments.forEach((segment) => {
            const coords = segment.coordinates || [];

            coords.forEach((coord, i) => {
                if (i > 0) {
                    const prevCoord = coords[i - 1];
                    const dist = this.haversineDistance(
                        prevCoord.lat, prevCoord.lng,
                        coord.lat, coord.lng
                    );
                    cumulativeDistance += dist;
                }

                const elevation = coord.ele !== undefined ? coord.ele : 0;
                elevationPoints.push({
                    distance: cumulativeDistance,
                    elevation: elevation,
                    segmentType: segment.segment_type,
                    segmentColor: segment.color
                });
            });
        });

        if (elevationPoints.length < 2) return;

        this.drawElevationCanvas(canvas, elevationPoints);
    }

    /**
     * Draw elevation profile using new profile data format
     * @param {HTMLCanvasElement} canvas
     * @param {Object} profile - { waypoints, segments, stats }
     */
    drawElevationFromProfile(canvas, profile) {
        const ctx = canvas.getContext('2d');
        const container = canvas.parentElement;
        const width = container.offsetWidth || 600;
        const height = 100;

        canvas.width = width;
        canvas.height = height;

        const waypoints = profile.waypoints;
        const segments = profile.segments;
        const stats = profile.stats;

        if (!waypoints || waypoints.length < 2) return;

        const maxDist = stats.total_distance_km || waypoints[waypoints.length - 1].dist;
        const minEle = stats.min_elevation_m;
        const maxEle = stats.max_elevation_m;
        const eleRange = (maxEle - minEle) || 1;

        const padding = { top: 10, bottom: 20, left: 40, right: 10 };
        const chartWidth = width - padding.left - padding.right;
        const chartHeight = height - padding.top - padding.bottom;

        ctx.clearRect(0, 0, width, height);

        // Get color for a waypoint index
        const getColorForIndex = (wpIndex) => {
            for (const seg of segments) {
                if (wpIndex >= seg.start && wpIndex <= seg.end) {
                    return seg.color || '#61CE70';
                }
            }
            return '#61CE70';
        };

        // Draw filled segments
        segments.forEach((seg) => {
            const startWp = waypoints[seg.start];
            const endWp = waypoints[seg.end];
            if (!startWp || !endWp) return;

            ctx.beginPath();
            ctx.moveTo(
                padding.left + (startWp.dist / maxDist) * chartWidth,
                height - padding.bottom
            );

            // Draw elevation line for this segment
            for (let i = seg.start; i <= seg.end && i < waypoints.length; i++) {
                const wp = waypoints[i];
                const x = padding.left + (wp.dist / maxDist) * chartWidth;
                const y = padding.top + (1 - (wp.ele - minEle) / eleRange) * chartHeight;
                ctx.lineTo(x, y);
            }

            ctx.lineTo(
                padding.left + (endWp.dist / maxDist) * chartWidth,
                height - padding.bottom
            );
            ctx.closePath();

            // Fill with segment color (semi-transparent)
            const color = seg.color || '#61CE70';
            ctx.fillStyle = this.hexToRgba(color, 0.3);
            ctx.fill();
        });

        // Draw elevation line with segment colors
        segments.forEach((seg) => {
            ctx.beginPath();
            ctx.strokeStyle = seg.color || '#61CE70';
            ctx.lineWidth = 2;

            for (let i = seg.start; i <= seg.end && i < waypoints.length; i++) {
                const wp = waypoints[i];
                const x = padding.left + (wp.dist / maxDist) * chartWidth;
                const y = padding.top + (1 - (wp.ele - minEle) / eleRange) * chartHeight;

                if (i === seg.start) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            }
            ctx.stroke();
        });

        // Draw axis labels
        const textColor = getComputedStyle(document.documentElement)
            .getPropertyValue('--color-text-secondary').trim() || '#6b7280';
        ctx.fillStyle = textColor;
        ctx.font = '10px system-ui, sans-serif';

        // Y-axis labels (elevation)
        ctx.textAlign = 'right';
        ctx.fillText(Math.round(maxEle) + 'm', padding.left - 4, padding.top + 10);
        ctx.fillText(Math.round(minEle) + 'm', padding.left - 4, height - padding.bottom);

        // X-axis labels (distance)
        ctx.textAlign = 'left';
        ctx.fillText('0', padding.left, height - 4);
        ctx.textAlign = 'right';
        ctx.fillText(maxDist.toFixed(1) + ' km', width - padding.right, height - 4);

        // Draw stats summary
        ctx.textAlign = 'center';
        ctx.fillStyle = textColor;
        ctx.font = '11px system-ui, sans-serif';
        const statsText = `${maxDist.toFixed(1)} km  •  ↑${stats.total_climb_m}m  •  ↓${stats.total_descent_m}m`;
        ctx.fillText(statsText, width / 2, height - 4);
    }

    /**
     * Convert hex color to rgba
     */
    hexToRgba(hex, alpha) {
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    }

    /**
     * Draw elevation profile on canvas
     * @param {HTMLCanvasElement} canvas
     * @param {Array} points
     */
    drawElevationCanvas(canvas, points) {
        const ctx = canvas.getContext('2d');
        const container = canvas.parentElement;
        const width = container.offsetWidth || 600;
        const height = 80;

        // Set canvas size
        canvas.width = width;
        canvas.height = height;

        // Calculate ranges
        const maxDist = Math.max(...points.map(p => p.distance));
        const minEle = Math.min(...points.map(p => p.elevation));
        const maxEle = Math.max(...points.map(p => p.elevation));
        const eleRange = maxEle - minEle || 1;

        const padding = { top: 5, bottom: 15, left: 5, right: 5 };
        const chartWidth = width - padding.left - padding.right;
        const chartHeight = height - padding.top - padding.bottom;

        // Clear canvas with transparent background (container CSS handles bg color)
        ctx.clearRect(0, 0, width, height);

        // Draw filled area and line
        let currentColor = points[0].segmentColor;

        // Fill under the line
        ctx.beginPath();
        ctx.moveTo(padding.left, height - padding.bottom);

        points.forEach((point) => {
            const x = padding.left + (point.distance / maxDist) * chartWidth;
            const y = padding.top + (1 - (point.elevation - minEle) / eleRange) * chartHeight;
            ctx.lineTo(x, y);
        });

        ctx.lineTo(width - padding.right, height - padding.bottom);
        ctx.closePath();

        // Gradient fill
        const gradient = ctx.createLinearGradient(0, padding.top, 0, height - padding.bottom);
        gradient.addColorStop(0, 'rgba(97, 206, 112, 0.4)');
        gradient.addColorStop(1, 'rgba(97, 206, 112, 0.05)');
        ctx.fillStyle = gradient;
        ctx.fill();

        // Draw line with segment colors
        currentColor = points[0].segmentColor;
        ctx.beginPath();
        ctx.strokeStyle = currentColor;
        ctx.lineWidth = 2;

        points.forEach((point, i) => {
            const x = padding.left + (point.distance / maxDist) * chartWidth;
            const y = padding.top + (1 - (point.elevation - minEle) / eleRange) * chartHeight;

            if (point.segmentColor !== currentColor && i > 0) {
                ctx.stroke();
                ctx.beginPath();
                ctx.strokeStyle = point.segmentColor;
                currentColor = point.segmentColor;
                ctx.moveTo(x, y);
            } else if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        ctx.stroke();

        // Draw elevation labels
        const textColor = computedStyle.getPropertyValue('--color-text-secondary').trim() || '#6b7280';
        ctx.fillStyle = textColor;
        ctx.font = '10px system-ui, sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText(Math.round(maxEle) + 'm', padding.left + 2, padding.top + 10);
        ctx.fillText(Math.round(minEle) + 'm', padding.left + 2, height - padding.bottom - 2);

        // Draw distance label
        ctx.textAlign = 'right';
        ctx.fillText(maxDist.toFixed(1) + ' km', width - padding.right - 2, height - 2);
    }

    /**
     * Calculate Haversine distance between two points
     * @param {number} lat1
     * @param {number} lon1
     * @param {number} lat2
     * @param {number} lon2
     * @returns {number} Distance in kilometers
     */
    haversineDistance(lat1, lon1, lat2, lon2) {
        const R = 6371;
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    }

    /**
     * Setup interactive elements
     */
    setupInteractions() {
        const container = document.getElementById(this.containerId + '-container');
        if (!container) return;

        // Segment list hover and click
        container.querySelectorAll('.event-map-segment-item').forEach(item => {
            item.addEventListener('mouseenter', () => {
                const segmentId = item.dataset.segmentId;
                this.highlightSegmentOnMap(segmentId);
            });

            item.addEventListener('mouseleave', () => {
                const segmentId = item.dataset.segmentId;
                this.unhighlightSegmentOnMap(segmentId);
            });

            item.addEventListener('click', () => {
                const segmentId = item.dataset.segmentId;
                this.zoomToSegment(segmentId);
            });
        });

        // POI legend click
        container.querySelectorAll('.event-map-poi-item').forEach(item => {
            item.addEventListener('click', () => {
                const poiType = item.dataset.poiType;
                this.zoomToPois(poiType);
            });
        });

        // Toggle map collapse
        const toggleBtn = container.querySelector('.event-map-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                container.classList.toggle('collapsed');
                const isExpanded = !container.classList.contains('collapsed');
                toggleBtn.setAttribute('aria-expanded', isExpanded);

                // Invalidate map size after transition
                if (isExpanded) {
                    setTimeout(() => {
                        this.map.invalidateSize();
                    }, 350);
                }
            });
        }

        // Locate user button
        const locateBtn = container.querySelector('.event-map-locate');
        if (locateBtn) {
            locateBtn.addEventListener('click', () => {
                this.locateUser(locateBtn);
            });
        }

        // Fullscreen button
        const fullscreenBtn = container.querySelector('.event-map-fullscreen');
        if (fullscreenBtn) {
            fullscreenBtn.addEventListener('click', () => {
                this.toggleFullscreen();
            });
        }

        // Menu toggle button (in fullscreen)
        const menuToggleBtn = container.querySelector('.event-map-menu-toggle');
        if (menuToggleBtn) {
            menuToggleBtn.addEventListener('click', () => {
                container.classList.toggle('menu-hidden');
            });
        }

        // Fullscreen menu segment items
        container.querySelectorAll('.event-map-fs-segment-item').forEach(item => {
            item.addEventListener('click', () => {
                const segmentId = item.dataset.segmentId;
                this.zoomToSegment(segmentId);
                // Highlight active
                container.querySelectorAll('.event-map-fs-segment-item').forEach(i => i.classList.remove('active'));
                item.classList.add('active');
            });
        });

        // Fullscreen menu POI items
        container.querySelectorAll('.event-map-fs-poi-item').forEach(item => {
            item.addEventListener('click', () => {
                const poiType = item.dataset.poiType;
                this.zoomToPois(poiType);
                // Highlight active
                container.querySelectorAll('.event-map-fs-poi-item').forEach(i => i.classList.remove('active'));
                item.classList.add('active');
            });
        });

        // Fullscreen locate button
        const fsLocateBtn = container.querySelector('.event-map-fs-locate');
        if (fsLocateBtn) {
            fsLocateBtn.addEventListener('click', () => {
                this.locateUser(fsLocateBtn);
            });
        }

        // ESC key to exit fullscreen
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && container.classList.contains('fullscreen')) {
                this.toggleFullscreen();
            }
        });

        // Enable scroll zoom on focus/click
        this.map.getContainer().addEventListener('click', () => {
            this.map.scrollWheelZoom.enable();
        });

        this.map.getContainer().addEventListener('mouseleave', () => {
            this.map.scrollWheelZoom.disable();
        });
    }

    /**
     * Highlight segment on map
     * @param {number|string} segmentId
     */
    highlightSegmentOnMap(segmentId) {
        if (!this.layers.segments) return;

        this.layers.segments.eachLayer(layer => {
            if (layer.feature && layer.feature.properties.id == segmentId) {
                layer.setStyle({ weight: 6, opacity: 1 });
                layer.bringToFront();
            }
        });
    }

    /**
     * Remove segment highlight on map
     * @param {number|string} segmentId
     */
    unhighlightSegmentOnMap(segmentId) {
        if (!this.layers.segments) return;

        this.layers.segments.eachLayer(layer => {
            if (layer.feature && layer.feature.properties.id == segmentId) {
                layer.setStyle({ weight: 4, opacity: 0.85 });
            }
        });
    }

    /**
     * Highlight segment in list
     * @param {number|string} segmentId
     */
    highlightSegmentInList(segmentId) {
        const container = document.getElementById(this.containerId + '-container');
        if (!container) return;

        const item = container.querySelector(`.event-map-segment-item[data-segment-id="${segmentId}"]`);
        if (item) {
            item.classList.add('highlighted');
        }
    }

    /**
     * Remove segment highlight in list
     * @param {number|string} segmentId
     */
    unhighlightSegmentInList(segmentId) {
        const container = document.getElementById(this.containerId + '-container');
        if (!container) return;

        const item = container.querySelector(`.event-map-segment-item[data-segment-id="${segmentId}"]`);
        if (item) {
            item.classList.remove('highlighted');
        }
    }

    /**
     * Zoom to a specific segment
     * @param {number|string} segmentId
     */
    zoomToSegment(segmentId) {
        if (!this.layers.segments) return;

        this.layers.segments.eachLayer(layer => {
            if (layer.feature && layer.feature.properties.id == segmentId) {
                this.map.fitBounds(layer.getBounds(), { padding: [50, 50] });
            }
        });
    }

    /**
     * Zoom to POIs of a specific type
     * @param {string} poiType
     */
    zoomToPois(poiType) {
        if (!this.layers.pois) return;

        const bounds = L.latLngBounds();
        let found = false;

        this.layers.pois.eachLayer(layer => {
            if (layer.feature && layer.feature.properties.poi_type === poiType) {
                bounds.extend(layer.getLatLng());
                found = true;
            }
        });

        if (found) {
            this.map.fitBounds(bounds, { padding: [50, 50], maxZoom: 16 });
        }
    }

    /**
     * Zoom to a specific segment
     * @param {number|string} segmentId
     */
    zoomToSegment(segmentId) {
        if (!this.layers.segments) return;

        this.layers.segments.eachLayer(layer => {
            if (layer.feature && layer.feature.properties.id == segmentId) {
                this.map.fitBounds(layer.getBounds(), { padding: [50, 50] });
                // Highlight the segment briefly
                layer.setStyle({ weight: 6, opacity: 1 });
                setTimeout(() => {
                    layer.setStyle({ weight: 4, opacity: 0.85 });
                }, 2000);
            }
        });
    }

    /**
     * Toggle fullscreen mode
     */
    toggleFullscreen() {
        const container = document.getElementById(this.containerId + '-container');
        if (!container) return;

        const isFullscreen = container.classList.contains('fullscreen');

        if (isFullscreen) {
            // Exit fullscreen
            container.classList.remove('fullscreen');
            container.classList.remove('menu-hidden');
            document.body.style.overflow = '';

            // Restore map size after transition
            setTimeout(() => {
                this.map.invalidateSize();
            }, 350);
        } else {
            // Enter fullscreen
            container.classList.add('fullscreen');
            document.body.style.overflow = 'hidden';

            // Update map size after transition
            setTimeout(() => {
                this.map.invalidateSize();
            }, 350);
        }
    }

    /**
     * Locate user and center map on their position
     * @param {HTMLElement} button - The locate button element
     */
    locateUser(button) {
        // Check if geolocation is supported
        if (!navigator.geolocation) {
            this.showLocationError(button, 'Geolocation stöds inte av din webbläsare');
            return;
        }

        // Set loading state
        button.classList.add('locating');
        button.classList.remove('error');

        // Get current position
        navigator.geolocation.getCurrentPosition(
            (position) => {
                this.handleLocationSuccess(position, button);
            },
            (error) => {
                this.handleLocationError(error, button);
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 30000
            }
        );
    }

    /**
     * Handle successful geolocation
     * @param {GeolocationPosition} position
     * @param {HTMLElement} button
     */
    handleLocationSuccess(position, button) {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        const accuracy = position.coords.accuracy;

        // Remove loading state
        button.classList.remove('locating');

        // Create user location icon
        const userIcon = L.divIcon({
            className: 'event-map-user-location',
            html: '<div class="event-map-user-dot"></div>',
            iconSize: [16, 16],
            iconAnchor: [8, 8]
        });

        // Update or create user location marker
        if (this.userLocationMarker) {
            this.userLocationMarker.setLatLng([lat, lng]);
        } else {
            this.userLocationMarker = L.marker([lat, lng], {
                icon: userIcon,
                zIndexOffset: 1000
            }).addTo(this.map);

            this.userLocationMarker.bindPopup('<strong>Din position</strong>');
        }

        // Update or create accuracy circle
        if (this.userAccuracyCircle) {
            this.userAccuracyCircle.setLatLng([lat, lng]);
            this.userAccuracyCircle.setRadius(accuracy);
        } else {
            this.userAccuracyCircle = L.circle([lat, lng], {
                radius: accuracy,
                className: 'event-map-user-accuracy',
                weight: 1,
                fillOpacity: 0.15,
                color: '#4285f4',
                fillColor: '#4285f4'
            }).addTo(this.map);
        }

        // Center map on user location
        this.map.setView([lat, lng], 15);
    }

    /**
     * Handle geolocation error
     * @param {GeolocationPositionError} error
     * @param {HTMLElement} button
     */
    handleLocationError(error, button) {
        button.classList.remove('locating');
        button.classList.add('error');

        let message = 'Kunde inte hitta din position';

        switch (error.code) {
            case error.PERMISSION_DENIED:
                message = 'Du nekade åtkomst till din position';
                break;
            case error.POSITION_UNAVAILABLE:
                message = 'Positionsinformation är inte tillgänglig';
                break;
            case error.TIMEOUT:
                message = 'Timeout vid hämtning av position';
                break;
        }

        console.warn('Geolocation error:', message);

        // Reset button state after 3 seconds
        setTimeout(() => {
            button.classList.remove('error');
        }, 3000);
    }

    /**
     * Show location error state
     * @param {HTMLElement} button
     * @param {string} message
     */
    showLocationError(button, message) {
        button.classList.add('error');
        console.warn('Location error:', message);

        setTimeout(() => {
            button.classList.remove('error');
        }, 3000);
    }
}

/**
 * Auto-initialize maps on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    // Find all map containers
    document.querySelectorAll('.event-map-container').forEach(container => {
        const mapDataAttr = container.dataset.mapData;
        if (!mapDataAttr) return;

        try {
            const mapData = JSON.parse(mapDataAttr);
            const mapElement = container.querySelector('.event-map-view');

            if (mapElement && mapElement.id) {
                // Store instance for potential later access
                container._eventMap = new EventMap(mapElement.id, mapData);
            }
        } catch (e) {
            console.error('Error initializing event map:', e);
        }
    });
});

// Export for manual initialization
if (typeof window !== 'undefined') {
    window.EventMap = EventMap;
}
