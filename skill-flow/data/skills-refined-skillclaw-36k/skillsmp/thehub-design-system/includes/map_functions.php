<?php
/**
 * Map Functions for TheHUB Event Maps
 *
 * Handles GPX parsing, track/segment management, and POI operations.
 *
 * @since 2025-12-09
 */

// Prevent direct access
if (!defined('THEHUB_INIT')) {
    die('Direct access not allowed');
}

// Include POI types configuration
require_once __DIR__ . '/../config/poi_types.php';

// =====================================================
// GPX PARSING
// =====================================================

/**
 * Parse GPX file and extract tracks/segments
 *
 * @param string $filepath Path to GPX file
 * @return array Parsed GPX data with tracks, bounds, and statistics
 * @throws Exception If file not found or invalid GPX
 */
function parseGpxFile($filepath) {
    if (!file_exists($filepath)) {
        throw new Exception("GPX-fil hittades inte: $filepath");
    }

    $xml = @simplexml_load_file($filepath);
    if ($xml === false) {
        throw new Exception("Kunde inte lasa GPX-filen - ogiltigt format");
    }

    // Register namespaces
    $namespaces = $xml->getNamespaces(true);
    $gpx_ns = $namespaces[''] ?? 'http://www.topografix.com/GPX/1/1';
    $xml->registerXPathNamespace('gpx', $gpx_ns);

    $tracks = [];
    $bounds = [
        'north' => -90,
        'south' => 90,
        'east' => -180,
        'west' => 180
    ];

    // Parse tracks (trk elements)
    foreach ($xml->trk as $track) {
        $trackData = [
            'name' => (string)$track->name ?: 'Unnamed Track',
            'segments' => []
        ];

        $segmentIndex = 0;
        foreach ($track->trkseg as $segment) {
            $coordinates = [];
            $elevations = [];
            $totalDistance = 0;
            $elevationGain = 0;
            $elevationLoss = 0;
            $prevPoint = null;

            foreach ($segment->trkpt as $point) {
                $lat = (float)$point['lat'];
                $lng = (float)$point['lon'];
                $ele = isset($point->ele) ? (float)$point->ele : null;

                // Update bounds
                $bounds['north'] = max($bounds['north'], $lat);
                $bounds['south'] = min($bounds['south'], $lat);
                $bounds['east'] = max($bounds['east'], $lng);
                $bounds['west'] = min($bounds['west'], $lng);

                $coord = ['lat' => $lat, 'lng' => $lng];
                if ($ele !== null) {
                    $coord['ele'] = $ele;
                    $elevations[] = $ele;
                }
                $coordinates[] = $coord;

                // Calculate distance and elevation changes
                if ($prevPoint !== null) {
                    $distance = haversineDistance(
                        $prevPoint['lat'], $prevPoint['lng'],
                        $lat, $lng
                    );
                    $totalDistance += $distance;

                    if ($ele !== null && isset($prevPoint['ele'])) {
                        $eleDiff = $ele - $prevPoint['ele'];
                        if ($eleDiff > 0) {
                            $elevationGain += $eleDiff;
                        } else {
                            $elevationLoss += abs($eleDiff);
                        }
                    }
                }

                $prevPoint = ['lat' => $lat, 'lng' => $lng, 'ele' => $ele];
            }

            if (count($coordinates) > 0) {
                $trackData['segments'][] = [
                    'index' => $segmentIndex++,
                    'coordinates' => $coordinates,
                    'elevations' => $elevations,
                    'distance_km' => round($totalDistance, 2),
                    'elevation_gain_m' => round($elevationGain),
                    'elevation_loss_m' => round($elevationLoss),
                    'start' => $coordinates[0],
                    'end' => $coordinates[count($coordinates) - 1]
                ];
            }
        }

        $tracks[] = $trackData;
    }

    return [
        'tracks' => $tracks,
        'bounds' => $bounds,
        'total_segments' => array_sum(array_map(fn($t) => count($t['segments']), $tracks))
    ];
}

/**
 * Haversine distance formula (km)
 *
 * @param float $lat1 Latitude of point 1
 * @param float $lon1 Longitude of point 1
 * @param float $lat2 Latitude of point 2
 * @param float $lon2 Longitude of point 2
 * @return float Distance in kilometers
 */
function haversineDistance($lat1, $lon1, $lat2, $lon2) {
    $earthRadius = 6371; // km

    $dLat = deg2rad($lat2 - $lat1);
    $dLon = deg2rad($lon2 - $lon1);

    $a = sin($dLat/2) * sin($dLat/2) +
         cos(deg2rad($lat1)) * cos(deg2rad($lat2)) *
         sin($dLon/2) * sin($dLon/2);

    $c = 2 * atan2(sqrt($a), sqrt(1-$a));

    return $earthRadius * $c;
}

// =====================================================
// TRACK CRUD OPERATIONS
// =====================================================

/**
 * Save track to database
 *
 * NEW WORKFLOW:
 * - Raw coordinates are stored in the track itself
 * - NO automatic segments created
 * - Full track is shown as "transport/liaison" by default
 * - User manually marks sections as SS (stage) or Lift
 *
 * @param PDO $pdo Database connection
 * @param int $eventId Event ID
 * @param string $name Track name
 * @param string $gpxFile GPX filename
 * @param array $parsedData Parsed GPX data from parseGpxFile()
 * @param array $options Optional: route_type, route_label, color, is_primary
 * @return int Track ID
 */
function saveEventTrack($pdo, $eventId, $name, $gpxFile, $parsedData, $options = []) {
    $pdo->beginTransaction();

    try {
        // Collect ALL raw coordinates and elevations from all segments
        $rawCoordinates = [];
        $rawElevations = [];
        $totalDistance = 0;
        $totalElevation = 0;

        foreach ($parsedData['tracks'] as $track) {
            foreach ($track['segments'] as $segment) {
                foreach ($segment['coordinates'] as $coord) {
                    $rawCoordinates[] = $coord;
                }
                foreach ($segment['elevations'] as $ele) {
                    $rawElevations[] = $ele;
                }
                $totalDistance += $segment['distance_km'];
                $totalElevation += $segment['elevation_gain_m'];
            }
        }

        // Get next display order
        $stmt = $pdo->prepare("SELECT COALESCE(MAX(display_order), 0) + 1 FROM event_tracks WHERE event_id = ?");
        $stmt->execute([$eventId]);
        $nextOrder = $stmt->fetchColumn();

        // Check if this should be primary (first track or explicitly set)
        $stmt = $pdo->prepare("SELECT COUNT(*) FROM event_tracks WHERE event_id = ?");
        $stmt->execute([$eventId]);
        $existingCount = $stmt->fetchColumn();
        $isPrimary = ($existingCount == 0) || ($options['is_primary'] ?? false);

        // If setting as primary, unset other primaries
        if ($isPrimary) {
            $pdo->prepare("UPDATE event_tracks SET is_primary = 0 WHERE event_id = ?")->execute([$eventId]);
        }

        // Check if raw_coordinates column exists (for backwards compatibility)
        $hasRawCoords = false;
        try {
            $check = $pdo->query("SHOW COLUMNS FROM event_tracks LIKE 'raw_coordinates'");
            $hasRawCoords = $check->fetch() !== false;
        } catch (Exception $e) {
            $hasRawCoords = false;
        }

        if ($hasRawCoords) {
            // NEW: Insert track with raw coordinates, NO automatic segments
            $stmt = $pdo->prepare("
                INSERT INTO event_tracks
                (event_id, name, route_type, route_label, gpx_file, raw_coordinates, raw_elevation_data,
                 total_distance_km, total_elevation_m,
                 bounds_north, bounds_south, bounds_east, bounds_west, is_primary, display_order, color)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ");
            $stmt->execute([
                $eventId,
                $name,
                $options['route_type'] ?? null,
                $options['route_label'] ?? $name,
                $gpxFile,
                json_encode($rawCoordinates),
                json_encode($rawElevations),
                $totalDistance,
                $totalElevation,
                $parsedData['bounds']['north'],
                $parsedData['bounds']['south'],
                $parsedData['bounds']['east'],
                $parsedData['bounds']['west'],
                $isPrimary ? 1 : 0,
                $options['display_order'] ?? $nextOrder,
                $options['color'] ?? '#3B82F6'
            ]);
        } else {
            // OLD: Without raw_coordinates (pre-migration)
            $stmt = $pdo->prepare("
                INSERT INTO event_tracks
                (event_id, name, route_type, route_label, gpx_file, total_distance_km, total_elevation_m,
                 bounds_north, bounds_south, bounds_east, bounds_west, is_primary, display_order, color)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ");
            $stmt->execute([
                $eventId,
                $name,
                $options['route_type'] ?? null,
                $options['route_label'] ?? $name,
                $gpxFile,
                $totalDistance,
                $totalElevation,
                $parsedData['bounds']['north'],
                $parsedData['bounds']['south'],
                $parsedData['bounds']['east'],
                $parsedData['bounds']['west'],
                $isPrimary ? 1 : 0,
                $options['display_order'] ?? $nextOrder,
                $options['color'] ?? '#3B82F6'
            ]);

            $trackId = $pdo->lastInsertId();

            // OLD workflow: No automatic segments created
            // User will manually mark sections via the segment editor

            $pdo->commit();
            return $trackId;
        }

        $trackId = $pdo->lastInsertId();

        // NEW workflow: NO automatic segments created
        // User will manually mark sections as SS/Lift

        $pdo->commit();
        return $trackId;

    } catch (Exception $e) {
        $pdo->rollBack();
        throw $e;
    }
}

/**
 * Get track with all segments for an event (backwards compatible - returns first/primary track)
 *
 * @param PDO $pdo Database connection
 * @param int $eventId Event ID
 * @return array|null Track data with segments or null if not found
 */
function getEventTrack($pdo, $eventId) {
    $stmt = $pdo->prepare("
        SELECT * FROM event_tracks WHERE event_id = ? ORDER BY is_primary DESC, display_order ASC LIMIT 1
    ");
    $stmt->execute([$eventId]);
    $track = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$track) {
        return null;
    }

    // Get segments
    $stmt = $pdo->prepare("
        SELECT * FROM event_track_segments
        WHERE track_id = ?
        ORDER BY sequence_number ASC
    ");
    $stmt->execute([$track['id']]);
    $track['segments'] = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Decode JSON fields
    foreach ($track['segments'] as &$segment) {
        $segment['coordinates'] = json_decode($segment['coordinates'], true);
        $segment['elevation_data'] = json_decode($segment['elevation_data'], true);
    }

    return $track;
}

/**
 * Get ALL tracks for an event (for multi-track support)
 *
 * @param PDO $pdo Database connection
 * @param int $eventId Event ID
 * @return array Array of tracks with segments
 */
function getEventTracks($pdo, $eventId) {
    // Check if raw_coordinates column exists
    $hasRawCoords = false;
    try {
        $check = $pdo->query("SHOW COLUMNS FROM event_tracks LIKE 'raw_coordinates'");
        $hasRawCoords = $check->fetch() !== false;
    } catch (Exception $e) {
        $hasRawCoords = false;
    }

    $stmt = $pdo->prepare("
        SELECT * FROM event_tracks
        WHERE event_id = ?
        ORDER BY is_primary DESC, display_order ASC
    ");
    $stmt->execute([$eventId]);
    $tracks = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Check if sponsor_id column exists AND sponsors table exists with required columns
    $hasSponsorColumn = false;
    $hasSponsorsTable = false;
    $sponsorColumns = [];
    try {
        $check = $pdo->query("SHOW COLUMNS FROM event_track_segments LIKE 'sponsor_id'");
        $hasSponsorColumn = $check->fetch() !== false;
        if ($hasSponsorColumn) {
            // Check if sponsors table exists and get its columns
            $check = $pdo->query("SHOW TABLES LIKE 'sponsors'");
            $hasSponsorsTable = $check->fetch() !== false;
            if ($hasSponsorsTable) {
                // Get actual columns in sponsors table
                $cols = $pdo->query("SHOW COLUMNS FROM sponsors");
                while ($col = $cols->fetch(PDO::FETCH_ASSOC)) {
                    $sponsorColumns[] = $col['Field'];
                }
            }
        }
    } catch (Exception $e) {
        $hasSponsorColumn = false;
        $hasSponsorsTable = false;
    }

    foreach ($tracks as &$track) {
        // Fetch segments with optional sponsor info (only if both column and table exist)
        if ($hasSponsorColumn && $hasSponsorsTable && in_array('name', $sponsorColumns)) {
            // Build SELECT dynamically based on available columns
            // Prefer media library logos (logo_small_id) over legacy logo field
            $sponsorFields = ['sp.name as sponsor_name'];
            if (in_array('logo_small_id', $sponsorColumns)) {
                // Use media library logo if available
                $sponsorFields[] = 'COALESCE(m_small.filepath, sp.logo) as sponsor_logo';
            } elseif (in_array('logo', $sponsorColumns)) {
                $sponsorFields[] = 'sp.logo as sponsor_logo';
            }
            if (in_array('website', $sponsorColumns)) {
                $sponsorFields[] = 'sp.website as sponsor_website';
            }

            $hasMediaJoin = in_array('logo_small_id', $sponsorColumns);
            $mediaJoin = $hasMediaJoin ? 'LEFT JOIN media m_small ON sp.logo_small_id = m_small.id' : '';

            $stmt = $pdo->prepare("
                SELECT s.*, " . implode(', ', $sponsorFields) . "
                FROM event_track_segments s
                LEFT JOIN sponsors sp ON s.sponsor_id = sp.id
                $mediaJoin
                WHERE s.track_id = ?
                ORDER BY s.sequence_number ASC
            ");
        } else {
            $stmt = $pdo->prepare("
                SELECT * FROM event_track_segments
                WHERE track_id = ?
                ORDER BY sequence_number ASC
            ");
        }
        $stmt->execute([$track['id']]);
        $track['segments'] = $stmt->fetchAll(PDO::FETCH_ASSOC);

        foreach ($track['segments'] as &$segment) {
            $segment['coordinates'] = json_decode($segment['coordinates'], true);
            $segment['elevation_data'] = json_decode($segment['elevation_data'], true);
        }

        // Don't decode raw_coordinates here (too large), just mark if present
        $track['has_raw_coords'] = $hasRawCoords && !empty($track['raw_coordinates']);
    }

    return $tracks;
}

/**
 * Get a specific track by ID
 *
 * @param PDO $pdo Database connection
 * @param int $trackId Track ID
 * @return array|null Track data with segments
 */
function getTrackById($pdo, $trackId) {
    $stmt = $pdo->prepare("SELECT * FROM event_tracks WHERE id = ?");
    $stmt->execute([$trackId]);
    $track = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$track) {
        return null;
    }

    $stmt = $pdo->prepare("
        SELECT * FROM event_track_segments
        WHERE track_id = ?
        ORDER BY sequence_number ASC
    ");
    $stmt->execute([$track['id']]);
    $track['segments'] = $stmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($track['segments'] as &$segment) {
        $segment['coordinates'] = json_decode($segment['coordinates'], true);
        $segment['elevation_data'] = json_decode($segment['elevation_data'], true);
    }

    return $track;
}

/**
 * Update track metadata
 *
 * @param PDO $pdo Database connection
 * @param int $trackId Track ID
 * @param array $data Data to update (name, route_type, route_label, color, is_primary)
 * @return bool Success
 */
function updateTrack($pdo, $trackId, $data) {
    // If setting as primary, unset others first
    if (!empty($data['is_primary'])) {
        $stmt = $pdo->prepare("SELECT event_id FROM event_tracks WHERE id = ?");
        $stmt->execute([$trackId]);
        $eventId = $stmt->fetchColumn();
        if ($eventId) {
            $pdo->prepare("UPDATE event_tracks SET is_primary = 0 WHERE event_id = ?")->execute([$eventId]);
        }
    }

    $fields = [];
    $values = [];
    foreach (['name', 'route_type', 'route_label', 'color', 'is_primary', 'display_order'] as $field) {
        if (array_key_exists($field, $data)) {
            $fields[] = "$field = ?";
            $values[] = $data[$field];
        }
    }

    if (empty($fields)) {
        return false;
    }

    $values[] = $trackId;
    $stmt = $pdo->prepare("UPDATE event_tracks SET " . implode(', ', $fields) . " WHERE id = ?");
    return $stmt->execute($values);
}

/**
 * Delete event track and all related data
 *
 * @param PDO $pdo Database connection
 * @param int $trackId Track ID
 * @return bool Success
 */
function deleteEventTrack($pdo, $trackId) {
    // Get track info for file deletion
    $stmt = $pdo->prepare("SELECT gpx_file FROM event_tracks WHERE id = ?");
    $stmt->execute([$trackId]);
    $track = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($track) {
        // Delete GPX file
        $gpxPath = UPLOADS_PATH . '/gpx/' . $track['gpx_file'];
        if (file_exists($gpxPath)) {
            @unlink($gpxPath);
        }
    }

    // Delete track (segments cascade)
    $stmt = $pdo->prepare("DELETE FROM event_tracks WHERE id = ?");
    return $stmt->execute([$trackId]);
}

/**
 * Update segment classification
 *
 * @param PDO $pdo Database connection
 * @param int $segmentId Segment ID
 * @param string $type 'stage' or 'liaison'
 * @param string $name Segment name
 * @param string|null $timingId Optional timing ID
 * @return bool Success
 */
function updateSegmentClassification($pdo, $segmentId, $type, $name, $timingId = null) {
    $color = getSegmentColor($type);

    $stmt = $pdo->prepare("
        UPDATE event_track_segments
        SET segment_type = ?, segment_name = ?, timing_id = ?, color = ?
        WHERE id = ?
    ");
    return $stmt->execute([$type, $name, $timingId, $color, $segmentId]);
}

/**
 * Reorder segments
 *
 * @param PDO $pdo Database connection
 * @param int $trackId Track ID
 * @param array $segmentOrder Array of segment IDs in desired order
 * @return bool Success
 */
function reorderSegments($pdo, $trackId, $segmentOrder) {
    $pdo->beginTransaction();
    try {
        foreach ($segmentOrder as $sequence => $segmentId) {
            $stmt = $pdo->prepare("
                UPDATE event_track_segments
                SET sequence_number = ?
                WHERE id = ? AND track_id = ?
            ");
            $stmt->execute([$sequence + 1, $segmentId, $trackId]);
        }
        $pdo->commit();
        return true;
    } catch (Exception $e) {
        $pdo->rollBack();
        throw $e;
    }
}

// =====================================================
// POI CRUD OPERATIONS
// =====================================================

/**
 * Get all POIs for an event
 *
 * @param PDO $pdo Database connection
 * @param int $eventId Event ID
 * @param bool $visibleOnly Only return visible POIs
 * @return array POIs with type info
 */
function getEventPois($pdo, $eventId, $visibleOnly = true) {
    $sql = "SELECT * FROM event_pois WHERE event_id = ?";
    if ($visibleOnly) {
        $sql .= " AND is_visible = 1";
    }
    $sql .= " ORDER BY poi_type, sequence_number";

    $stmt = $pdo->prepare($sql);
    $stmt->execute([$eventId]);
    $pois = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Enrich with type info
    foreach ($pois as &$poi) {
        $typeInfo = getPoiType($poi['poi_type']);
        if ($typeInfo) {
            $poi['type_label'] = $typeInfo['label'];
            $poi['type_icon'] = $typeInfo['icon'];
            $poi['type_emoji'] = $typeInfo['emoji'];
            $poi['type_color'] = $typeInfo['color'];
        }
    }

    return $pois;
}

/**
 * Add POI
 *
 * @param PDO $pdo Database connection
 * @param int $eventId Event ID
 * @param array $data POI data (poi_type, lat, lng, label, description, sequence_number)
 * @return int POI ID
 */
function addEventPoi($pdo, $eventId, $data) {
    $stmt = $pdo->prepare("
        INSERT INTO event_pois
        (event_id, poi_type, label, description, lat, lng, sequence_number)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ");
    $stmt->execute([
        $eventId,
        $data['poi_type'],
        $data['label'] ?? null,
        $data['description'] ?? null,
        $data['lat'],
        $data['lng'],
        $data['sequence_number'] ?? null
    ]);

    return $pdo->lastInsertId();
}

/**
 * Update POI
 *
 * @param PDO $pdo Database connection
 * @param int $poiId POI ID
 * @param array $data POI data
 * @return bool Success
 */
function updateEventPoi($pdo, $poiId, $data) {
    $stmt = $pdo->prepare("
        UPDATE event_pois
        SET poi_type = ?, label = ?, description = ?, lat = ?, lng = ?
        WHERE id = ?
    ");
    return $stmt->execute([
        $data['poi_type'],
        $data['label'] ?? null,
        $data['description'] ?? null,
        $data['lat'],
        $data['lng'],
        $poiId
    ]);
}

/**
 * Delete POI
 *
 * @param PDO $pdo Database connection
 * @param int $poiId POI ID
 * @return bool Success
 */
function deleteEventPoi($pdo, $poiId) {
    $stmt = $pdo->prepare("DELETE FROM event_pois WHERE id = ?");
    return $stmt->execute([$poiId]);
}

/**
 * Toggle POI visibility
 *
 * @param PDO $pdo Database connection
 * @param int $poiId POI ID
 * @return bool Success
 */
function togglePoiVisibility($pdo, $poiId) {
    $stmt = $pdo->prepare("
        UPDATE event_pois SET is_visible = NOT is_visible WHERE id = ?
    ");
    return $stmt->execute([$poiId]);
}

/**
 * Bulk add POIs (for import)
 *
 * @param PDO $pdo Database connection
 * @param int $eventId Event ID
 * @param array $poisData Array of POI data
 * @return int Number of POIs added
 */
function bulkAddPois($pdo, $eventId, $poisData) {
    $pdo->beginTransaction();
    try {
        $count = 0;
        foreach ($poisData as $poi) {
            addEventPoi($pdo, $eventId, $poi);
            $count++;
        }
        $pdo->commit();
        return $count;
    } catch (Exception $e) {
        $pdo->rollBack();
        throw $e;
    }
}

// =====================================================
// MAP DATA API
// =====================================================

/**
 * Get complete map data for frontend (single primary track - backwards compatible)
 *
 * @param PDO $pdo Database connection
 * @param int $eventId Event ID
 * @return array|null Map data or null if no track exists
 */
function getEventMapData($pdo, $eventId) {
    $track = getEventTrack($pdo, $eventId);
    $pois = getEventPois($pdo, $eventId);

    if (!$track) {
        return null;
    }

    // Build GeoJSON for segments
    $features = [];

    // Add segment lines
    foreach ($track['segments'] as $segment) {
        $coordinates = array_map(function($coord) {
            return [$coord['lng'], $coord['lat']];
        }, $segment['coordinates']);

        $features[] = [
            'type' => 'Feature',
            'geometry' => [
                'type' => 'LineString',
                'coordinates' => $coordinates
            ],
            'properties' => [
                'id' => (int)$segment['id'],
                'type' => 'segment',
                'segment_type' => $segment['segment_type'],
                'name' => $segment['segment_name'],
                'sequence' => (int)$segment['sequence_number'],
                'distance_km' => (float)$segment['distance_km'],
                'elevation_gain' => (int)$segment['elevation_gain_m'],
                'color' => $segment['color'],
                'timing_id' => $segment['timing_id'] ?? null
            ]
        ];
    }

    // Add POI points
    foreach ($pois as $poi) {
        $features[] = [
            'type' => 'Feature',
            'geometry' => [
                'type' => 'Point',
                'coordinates' => [(float)$poi['lng'], (float)$poi['lat']]
            ],
            'properties' => [
                'id' => (int)$poi['id'],
                'type' => 'poi',
                'poi_type' => $poi['poi_type'],
                'label' => $poi['label'] ?: $poi['type_label'],
                'description' => $poi['description'],
                'icon' => $poi['type_icon'],
                'emoji' => $poi['type_emoji'],
                'color' => $poi['type_color']
            ]
        ];
    }

    // Get elevation profile data (full track with segment positions)
    $elevationProfile = getElevationProfileData($pdo, $track['id']);

    return [
        'track' => [
            'id' => (int)$track['id'],
            'name' => $track['name'],
            'total_distance_km' => (float)$track['total_distance_km'],
            'total_elevation_m' => (int)$track['total_elevation_m']
        ],
        'bounds' => [
            [(float)$track['bounds_south'], (float)$track['bounds_west']],
            [(float)$track['bounds_north'], (float)$track['bounds_east']]
        ],
        'geojson' => [
            'type' => 'FeatureCollection',
            'features' => $features
        ],
        'segments' => $track['segments'],
        'elevation_profile' => $elevationProfile,
        'pois' => $pois,
        'poi_types' => POI_TYPES
    ];
}

/**
 * Get complete map data for ALL tracks (multi-track version)
 *
 * @param PDO $pdo Database connection
 * @param int $eventId Event ID
 * @return array Map data with all tracks
 */
function getEventMapDataMultiTrack($pdo, $eventId) {
    $tracks = getEventTracks($pdo, $eventId);
    $pois = getEventPois($pdo, $eventId);

    if (empty($tracks)) {
        return null;
    }

    // Calculate combined bounds
    $bounds = [
        'north' => -90, 'south' => 90,
        'east' => -180, 'west' => 180
    ];

    $tracksData = [];
    $allFeatures = [];

    foreach ($tracks as $track) {
        // Update combined bounds
        if ($track['bounds_north']) $bounds['north'] = max($bounds['north'], (float)$track['bounds_north']);
        if ($track['bounds_south']) $bounds['south'] = min($bounds['south'], (float)$track['bounds_south']);
        if ($track['bounds_east']) $bounds['east'] = max($bounds['east'], (float)$track['bounds_east']);
        if ($track['bounds_west']) $bounds['west'] = min($bounds['west'], (float)$track['bounds_west']);

        $trackFeatures = [];

        // Check if track has raw coordinates (new workflow)
        // Use the flag set in getEventTracks() for consistency
        $hasRawCoords = $track['has_raw_coords'] ?? false;

        if ($hasRawCoords) {
            // NEW WORKFLOW: Build connected segments from raw coordinates
            // Get all waypoints
            $waypoints = getTrackWaypointsForEditor($pdo, $track['id']);

            if (!empty($waypoints)) {
                // Get segment index ranges
                $segmentRanges = getSegmentIndexRanges($pdo, $track['id'], count($waypoints));

                // Build features for each range (transport + marked segments)
                foreach ($segmentRanges as $range) {
                    $rangeCoords = array_slice($waypoints, $range['start'], $range['end'] - $range['start'] + 1);
                    $coordinates = array_map(function($wp) {
                        return [$wp['lng'], $wp['lat']];
                    }, $rangeCoords);

                    if (count($coordinates) < 2) continue;

                    $feature = [
                        'type' => 'Feature',
                        'geometry' => [
                            'type' => 'LineString',
                            'coordinates' => $coordinates
                        ],
                        'properties' => [
                            'id' => $range['segment_id'] ?? 0,
                            'type' => 'segment',
                            'track_id' => (int)$track['id'],
                            'segment_type' => $range['type'],
                            'name' => $range['name'],
                            'distance_km' => $range['distance_km'],
                            'color' => $range['color']
                        ]
                    ];
                    $trackFeatures[] = $feature;
                    $allFeatures[] = $feature;
                }
            }
        } else {
            // OLD WORKFLOW: ALWAYS draw base track first, then segments on top
            // This ensures the full track is visible even with partial segments
            $waypoints = getTrackWaypointsForEditor($pdo, $track['id']);
            if (!empty($waypoints)) {
                $baseCoordinates = array_map(function($wp) {
                    return [$wp['lng'], $wp['lat']];
                }, $waypoints);

                // Draw base track (gray, underneath segments)
                $baseFeature = [
                    'type' => 'Feature',
                    'geometry' => [
                        'type' => 'LineString',
                        'coordinates' => $baseCoordinates
                    ],
                    'properties' => [
                        'id' => 0,
                        'type' => 'base_track',
                        'track_id' => (int)$track['id'],
                        'segment_type' => 'liaison',
                        'name' => 'Hela banan',
                        'distance_km' => (float)$track['total_distance_km'],
                        'color' => '#9CA3AF' // Gray base track
                    ]
                ];
                $trackFeatures[] = $baseFeature;
                $allFeatures[] = $baseFeature;
            }

            // Draw segments on top of base track
            if (!empty($track['segments'])) {
                foreach ($track['segments'] as $segment) {
                    $coordinates = array_map(function($coord) {
                        return [$coord['lng'], $coord['lat']];
                    }, $segment['coordinates'] ?? []);

                    $feature = [
                        'type' => 'Feature',
                        'geometry' => [
                            'type' => 'LineString',
                            'coordinates' => $coordinates
                        ],
                        'properties' => [
                            'id' => (int)$segment['id'],
                            'type' => 'segment',
                            'track_id' => (int)$track['id'],
                            'segment_type' => $segment['segment_type'],
                            'name' => $segment['segment_name'],
                            'sequence' => (int)$segment['sequence_number'],
                            'distance_km' => (float)$segment['distance_km'],
                            'elevation_gain' => (int)$segment['elevation_gain_m'],
                            'color' => $segment['color'],
                            'timing_id' => $segment['timing_id'] ?? null,
                            'sponsor_id' => $segment['sponsor_id'] ?? null,
                            'sponsor_name' => $segment['sponsor_name'] ?? null,
                            'sponsor_logo' => $segment['sponsor_logo'] ?? null,
                            'sponsor_website' => $segment['sponsor_website'] ?? null
                        ]
                    ];
                    $trackFeatures[] = $feature;
                    $allFeatures[] = $feature;
                }
            }
        }

        $tracksData[] = [
            'id' => (int)$track['id'],
            'name' => $track['name'],
            'route_type' => $track['route_type'] ?? null,
            'route_label' => $track['route_label'] ?? $track['name'],
            'color' => $track['color'] ?? '#3B82F6',
            'is_primary' => (bool)($track['is_primary'] ?? false),
            'total_distance_km' => (float)$track['total_distance_km'],
            'total_elevation_m' => (int)$track['total_elevation_m'],
            'segments' => $track['segments'],
            'has_raw_coords' => $hasRawCoords,
            'geojson' => [
                'type' => 'FeatureCollection',
                'features' => $trackFeatures
            ]
        ];
    }

    // Add POI points
    foreach ($pois as $poi) {
        $allFeatures[] = [
            'type' => 'Feature',
            'geometry' => [
                'type' => 'Point',
                'coordinates' => [(float)$poi['lng'], (float)$poi['lat']]
            ],
            'properties' => [
                'id' => (int)$poi['id'],
                'type' => 'poi',
                'poi_type' => $poi['poi_type'],
                'label' => $poi['label'] ?: $poi['type_label'],
                'description' => $poi['description'],
                'icon' => $poi['type_icon'],
                'emoji' => $poi['type_emoji'],
                'color' => $poi['type_color']
            ]
        ];
    }

    return [
        'tracks' => $tracksData,
        'primary_track_id' => $tracksData[0]['id'] ?? null,
        'bounds' => [
            [(float)$bounds['south'], (float)$bounds['west']],
            [(float)$bounds['north'], (float)$bounds['east']]
        ],
        'geojson' => [
            'type' => 'FeatureCollection',
            'features' => $allFeatures
        ],
        'pois' => $pois,
        'poi_types' => POI_TYPES
    ];
}

/**
 * Check if event has map data
 *
 * @param PDO $pdo Database connection
 * @param int $eventId Event ID
 * @return bool
 */
function eventHasMap($pdo, $eventId) {
    $stmt = $pdo->prepare("SELECT 1 FROM event_tracks WHERE event_id = ? LIMIT 1");
    $stmt->execute([$eventId]);
    return $stmt->fetch() !== false;
}

/**
 * Get upload path for GPX files
 *
 * @return string Path to GPX upload directory
 */
function getGpxUploadPath() {
    $path = UPLOADS_PATH . '/gpx';
    if (!is_dir($path)) {
        mkdir($path, 0755, true);
    }
    return $path;
}

// =====================================================
// SEGMENT DEFINITION BY DISTANCE
// =====================================================

/**
 * Get all coordinates with cumulative distance for a track
 *
 * @param PDO $pdo Database connection
 * @param int $trackId Track ID
 * @return array Array of points with lat, lng, ele, cumulative_km
 */
function getTrackCoordinatesWithDistance($pdo, $trackId) {
    // Get all segments ordered by sequence
    $stmt = $pdo->prepare("
        SELECT coordinates, elevation_data
        FROM event_track_segments
        WHERE track_id = ?
        ORDER BY sequence_number ASC
    ");
    $stmt->execute([$trackId]);
    $segments = $stmt->fetchAll(PDO::FETCH_ASSOC);

    $allPoints = [];
    $cumulativeDistance = 0;
    $prevPoint = null;

    foreach ($segments as $segment) {
        $coords = json_decode($segment['coordinates'], true) ?: [];
        $elevations = json_decode($segment['elevation_data'], true) ?: [];

        foreach ($coords as $i => $coord) {
            $point = [
                'lat' => $coord['lat'],
                'lng' => $coord['lng'],
                'ele' => $elevations[$i] ?? ($coord['ele'] ?? null)
            ];

            if ($prevPoint !== null) {
                $distance = haversineDistance(
                    $prevPoint['lat'], $prevPoint['lng'],
                    $point['lat'], $point['lng']
                );
                $cumulativeDistance += $distance;
            }

            $point['cumulative_km'] = $cumulativeDistance;
            $allPoints[] = $point;
            $prevPoint = $point;
        }
    }

    return $allPoints;
}

/**
 * Define track segments based on distance intervals
 *
 * @param PDO $pdo Database connection
 * @param int $trackId Track ID
 * @param array $segmentDefs Array of segment definitions:
 *        [['name' => 'SS1', 'type' => 'stage', 'start_km' => 0, 'end_km' => 5.2], ...]
 * @return bool Success
 * @throws Exception On error
 */
function defineTrackSegmentsFromDistances($pdo, $trackId, $segmentDefs) {
    // Get all coordinates with distances
    $allPoints = getTrackCoordinatesWithDistance($pdo, $trackId);

    if (empty($allPoints)) {
        throw new Exception("Inga koordinater hittades för banan");
    }

    $totalDistance = end($allPoints)['cumulative_km'];

    // Validate segment definitions
    foreach ($segmentDefs as $def) {
        if ($def['end_km'] > $totalDistance + 0.1) {
            throw new Exception("Segmentet '{$def['name']}' slutar vid {$def['end_km']} km men banan är bara {$totalDistance} km");
        }
    }

    $pdo->beginTransaction();

    try {
        // Delete existing segments
        $stmt = $pdo->prepare("DELETE FROM event_track_segments WHERE track_id = ?");
        $stmt->execute([$trackId]);

        // Create new segments
        $sequenceNumber = 1;

        foreach ($segmentDefs as $def) {
            $startKm = floatval($def['start_km']);
            $endKm = floatval($def['end_km']);
            $segmentType = $def['type'] ?? 'stage';
            $segmentName = $def['name'] ?? "Segment $sequenceNumber";

            // Find points within this range
            $segmentCoords = [];
            $segmentElevations = [];
            $elevationGain = 0;
            $elevationLoss = 0;
            $prevEle = null;

            foreach ($allPoints as $point) {
                if ($point['cumulative_km'] >= $startKm && $point['cumulative_km'] <= $endKm) {
                    $segmentCoords[] = ['lat' => $point['lat'], 'lng' => $point['lng']];
                    if ($point['ele'] !== null) {
                        $segmentElevations[] = $point['ele'];

                        if ($prevEle !== null) {
                            $diff = $point['ele'] - $prevEle;
                            if ($diff > 0) {
                                $elevationGain += $diff;
                            } else {
                                $elevationLoss += abs($diff);
                            }
                        }
                        $prevEle = $point['ele'];
                    }
                }
            }

            if (empty($segmentCoords)) {
                // Try to find at least the closest point to start
                $closestPoint = null;
                $closestDist = PHP_INT_MAX;
                foreach ($allPoints as $point) {
                    $dist = abs($point['cumulative_km'] - $startKm);
                    if ($dist < $closestDist) {
                        $closestDist = $dist;
                        $closestPoint = $point;
                    }
                }
                if ($closestPoint) {
                    $segmentCoords[] = ['lat' => $closestPoint['lat'], 'lng' => $closestPoint['lng']];
                }
            }

            if (empty($segmentCoords)) {
                continue; // Skip empty segments
            }

            $startCoord = $segmentCoords[0];
            $endCoord = end($segmentCoords);
            $segmentDistance = $endKm - $startKm;

            // Insert segment
            $stmt = $pdo->prepare("
                INSERT INTO event_track_segments
                (track_id, segment_type, segment_name, sequence_number,
                 distance_km, elevation_gain_m, elevation_loss_m,
                 start_lat, start_lng, end_lat, end_lng,
                 coordinates, elevation_data, color)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ");
            $stmt->execute([
                $trackId,
                $segmentType,
                $segmentName,
                $sequenceNumber,
                $segmentDistance,
                round($elevationGain),
                round($elevationLoss),
                $startCoord['lat'],
                $startCoord['lng'],
                $endCoord['lat'],
                $endCoord['lng'],
                json_encode($segmentCoords),
                json_encode($segmentElevations),
                getSegmentColor($segmentType)
            ]);

            $sequenceNumber++;
        }

        // Update track totals
        $stmt = $pdo->prepare("
            SELECT SUM(distance_km) as total_dist, SUM(elevation_gain_m) as total_ele
            FROM event_track_segments WHERE track_id = ?
        ");
        $stmt->execute([$trackId]);
        $totals = $stmt->fetch(PDO::FETCH_ASSOC);

        $stmt = $pdo->prepare("
            UPDATE event_tracks
            SET total_distance_km = ?, total_elevation_m = ?
            WHERE id = ?
        ");
        $stmt->execute([
            $totals['total_dist'] ?? 0,
            $totals['total_ele'] ?? 0,
            $trackId
        ]);

        $pdo->commit();
        return true;

    } catch (Exception $e) {
        $pdo->rollBack();
        throw $e;
    }
}

/**
 * Add a single segment by distance
 *
 * @param PDO $pdo Database connection
 * @param int $trackId Track ID
 * @param array $segmentDef Segment definition (name, type, start_km, end_km)
 * @return int New segment ID
 */
function addSegmentByDistance($pdo, $trackId, $segmentDef) {
    // Get current segments
    $stmt = $pdo->prepare("
        SELECT id, segment_type, segment_name, distance_km,
               (SELECT SUM(distance_km) FROM event_track_segments WHERE track_id = ? AND sequence_number <= s.sequence_number) as end_km
        FROM event_track_segments s
        WHERE track_id = ?
        ORDER BY sequence_number
    ");
    $stmt->execute([$trackId, $trackId]);
    $existingSegments = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Rebuild segment definitions including the new one
    $segmentDefs = [];
    $startKm = 0;
    foreach ($existingSegments as $seg) {
        $segmentDefs[] = [
            'name' => $seg['segment_name'],
            'type' => $seg['segment_type'],
            'start_km' => $startKm,
            'end_km' => $startKm + $seg['distance_km']
        ];
        $startKm += $seg['distance_km'];
    }

    // Add the new segment (will be inserted at the right position)
    $segmentDefs[] = $segmentDef;

    // Sort by start_km
    usort($segmentDefs, fn($a, $b) => $a['start_km'] <=> $b['start_km']);

    // Redefine all segments
    defineTrackSegmentsFromDistances($pdo, $trackId, $segmentDefs);

    // Return the ID of the newly added segment
    $stmt = $pdo->prepare("
        SELECT id FROM event_track_segments
        WHERE track_id = ? AND segment_name = ?
        ORDER BY id DESC LIMIT 1
    ");
    $stmt->execute([$trackId, $segmentDef['name']]);
    $result = $stmt->fetch(PDO::FETCH_ASSOC);

    return $result ? $result['id'] : 0;
}

/**
 * Add a segment by waypoint indices (for visual map-based definition)
 * Uses the unified waypoint list from getTrackWaypointsForEditor
 *
 * @param PDO $pdo
 * @param int $trackId
 * @param array $segmentDef ['name', 'type', 'start_index', 'end_index']
 * @return int New segment ID
 */
function addSegmentByWaypointIndex($pdo, $trackId, $segmentDef) {
    $startIdx = intval($segmentDef['start_index']);
    $endIdx = intval($segmentDef['end_index']);

    // Get all waypoints using the editor function
    $allWaypoints = getTrackWaypointsForEditor($pdo, $trackId);

    if (empty($allWaypoints)) {
        throw new Exception('Inga waypoints hittades för denna bana');
    }

    // Validate indices
    $maxIndex = count($allWaypoints) - 1;
    if ($startIdx < 0 || $startIdx > $maxIndex || $endIdx < 0 || $endIdx > $maxIndex) {
        throw new Exception('Ogiltiga waypoint-index');
    }
    if ($endIdx <= $startIdx) {
        throw new Exception('Slutpunkten måste vara efter startpunkten');
    }

    // Get waypoints for this segment
    $segmentWaypoints = array_slice($allWaypoints, $startIdx, $endIdx - $startIdx + 1);

    // Calculate distance and elevation
    $totalDistance = 0;
    $elevationGain = 0;
    $elevationLoss = 0;
    $prevWp = null;
    $coordinates = [];
    $elevations = [];

    foreach ($segmentWaypoints as $wp) {
        $coordinates[] = ['lat' => $wp['lat'], 'lng' => $wp['lng']];
        if ($wp['elevation'] !== null) {
            $elevations[] = $wp['elevation'];
        }

        if ($prevWp !== null) {
            $distance = haversineDistance(
                $prevWp['lat'], $prevWp['lng'],
                $wp['lat'], $wp['lng']
            );
            $totalDistance += $distance;

            if ($wp['elevation'] !== null && $prevWp['elevation'] !== null) {
                $eleDiff = $wp['elevation'] - $prevWp['elevation'];
                if ($eleDiff > 0) {
                    $elevationGain += $eleDiff;
                } else {
                    $elevationLoss += abs($eleDiff);
                }
            }
        }
        $prevWp = $wp;
    }

    // Get highest sequence number for segments
    $stmt = $pdo->prepare("
        SELECT COALESCE(MAX(sequence_number), 0) as max_seq
        FROM event_track_segments WHERE track_id = ?
    ");
    $stmt->execute([$trackId]);
    $maxSeq = $stmt->fetch(PDO::FETCH_ASSOC)['max_seq'];
    $newSeqNum = $maxSeq + 1;

    // Determine color based on type
    $segmentColors = [
        'stage' => '#EF4444',   // Red for SS/tävling
        'liaison' => '#61CE70', // Green for transport
        'lift' => '#F59E0B'     // Orange for lift
    ];
    $color = $segmentColors[$segmentDef['type']] ?? '#61CE70';

    // Check if start_index column exists
    $hasIndexCols = false;
    try {
        $check = $pdo->query("SHOW COLUMNS FROM event_track_segments LIKE 'start_index'");
        $hasIndexCols = $check->fetch() !== false;
    } catch (Exception $e) {
        $hasIndexCols = false;
    }

    if ($hasIndexCols) {
        // NEW: Store with index references
        $stmt = $pdo->prepare("
            INSERT INTO event_track_segments
            (track_id, sequence_number, segment_type, segment_name, color, distance_km, elevation_gain_m, elevation_loss_m, start_index, end_index, coordinates, elevation_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ");
        $stmt->execute([
            $trackId,
            $newSeqNum,
            $segmentDef['type'],
            $segmentDef['name'],
            $color,
            round($totalDistance, 2),
            round($elevationGain),
            round($elevationLoss),
            $startIdx,
            $endIdx,
            json_encode($coordinates),
            json_encode($elevations)
        ]);
    } else {
        // OLD: Without index columns
        $stmt = $pdo->prepare("
            INSERT INTO event_track_segments
            (track_id, sequence_number, segment_type, segment_name, color, distance_km, elevation_gain_m, elevation_loss_m, coordinates, elevation_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ");
        $stmt->execute([
            $trackId,
            $newSeqNum,
            $segmentDef['type'],
            $segmentDef['name'],
            $color,
            round($totalDistance, 2),
            round($elevationGain),
            round($elevationLoss),
            json_encode($coordinates),
            json_encode($elevations)
        ]);
    }

    return $pdo->lastInsertId();
}

/**
 * Get all waypoints for a track (for visual segment editor)
 * Uses raw_coordinates if available, otherwise falls back to segment coordinates
 *
 * @param PDO $pdo
 * @param int $trackId
 * @return array Array of waypoints with index, lat, lng, cumulative distance
 */
function getTrackWaypointsForEditor($pdo, $trackId) {
    $coordinates = [];
    $elevations = [];

    // Check if raw_coordinates column exists and try to use it
    $hasRawCoords = false;
    try {
        $check = $pdo->query("SHOW COLUMNS FROM event_tracks LIKE 'raw_coordinates'");
        $hasRawCoords = $check->fetch() !== false;
    } catch (Exception $e) {
        $hasRawCoords = false;
    }

    if ($hasRawCoords) {
        // Try to get raw_coordinates from track (new workflow)
        $stmt = $pdo->prepare("SELECT raw_coordinates, raw_elevation_data FROM event_tracks WHERE id = ?");
        $stmt->execute([$trackId]);
        $track = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($track && !empty($track['raw_coordinates'])) {
            // NEW workflow: Use raw coordinates from track
            $coordinates = json_decode($track['raw_coordinates'], true) ?: [];
            $elevations = json_decode($track['raw_elevation_data'], true) ?: [];
        }
    }

    // Fall back to GPX file FIRST (has complete track data)
    // This is preferred over segments because segments might only cover part of the track
    if (empty($coordinates)) {
        $stmt = $pdo->prepare("SELECT gpx_file FROM event_tracks WHERE id = ?");
        $stmt->execute([$trackId]);
        $track = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($track && !empty($track['gpx_file'])) {
            $gpxPath = getGpxUploadPath() . '/' . $track['gpx_file'];
            if (file_exists($gpxPath)) {
                try {
                    $parsedData = parseGpxFile($gpxPath);
                    // Extract coordinates from tracks -> segments -> coordinates structure
                    if (!empty($parsedData['tracks'])) {
                        foreach ($parsedData['tracks'] as $gpxTrack) {
                            foreach ($gpxTrack['segments'] as $segment) {
                                foreach ($segment['coordinates'] as $coord) {
                                    $coordinates[] = [
                                        'lat' => $coord['lat'],
                                        'lng' => $coord['lng']
                                    ];
                                    if (isset($coord['ele'])) {
                                        $elevations[] = $coord['ele'];
                                    }
                                }
                            }
                        }
                    }
                } catch (Exception $e) {
                    // GPX parsing failed, continue with empty array
                }
            }
        }
    }

    // Last resort: Extract from segments (might be incomplete if not all track is segmented)
    if (empty($coordinates)) {
        $stmt = $pdo->prepare("
            SELECT id, sequence_number, coordinates, elevation_data
            FROM event_track_segments
            WHERE track_id = ?
            ORDER BY sequence_number
        ");
        $stmt->execute([$trackId]);
        $segments = $stmt->fetchAll(PDO::FETCH_ASSOC);

        foreach ($segments as $segment) {
            $segCoords = json_decode($segment['coordinates'], true) ?: [];
            $segEles = json_decode($segment['elevation_data'], true) ?: [];

            foreach ($segCoords as $i => $coord) {
                $coordinates[] = $coord;
                if (isset($segEles[$i])) {
                    $elevations[] = $segEles[$i];
                }
            }
        }
    }

    // Build waypoint list with cumulative distance
    $result = [];
    $cumulativeDistance = 0;
    $prevWp = null;

    foreach ($coordinates as $i => $coord) {
        if ($prevWp !== null) {
            $distance = haversineDistance(
                $prevWp['lat'], $prevWp['lng'],
                $coord['lat'], $coord['lng']
            );
            $cumulativeDistance += $distance;
        }

        $result[] = [
            'index' => $i,
            'lat' => floatval($coord['lat']),
            'lng' => floatval($coord['lng']),
            'elevation' => isset($elevations[$i]) ? floatval($elevations[$i]) : (isset($coord['ele']) ? floatval($coord['ele']) : null),
            'distance_km' => round($cumulativeDistance, 3)
        ];

        $prevWp = $coord;
    }

    return $result;
}

/**
 * Get raw track polyline for display (the full track as base layer)
 *
 * @param PDO $pdo
 * @param int $trackId
 * @return array GeoJSON LineString feature
 */
function getTrackBasePolyline($pdo, $trackId) {
    $waypoints = getTrackWaypointsForEditor($pdo, $trackId);

    if (empty($waypoints)) {
        return null;
    }

    $coordinates = array_map(function($wp) {
        return [$wp['lng'], $wp['lat']];
    }, $waypoints);

    return [
        'type' => 'Feature',
        'geometry' => [
            'type' => 'LineString',
            'coordinates' => $coordinates
        ],
        'properties' => [
            'type' => 'base_track',
            'color' => '#61CE70', // Green for transport/liaison
            'weight' => 4,
            'opacity' => 0.8
        ]
    ];
}

/**
 * Get segment index ranges for a track
 *
 * Returns a list of ranges covering the entire track, where marked
 * segments have their type (stage/lift) and unmarked portions are transport.
 *
 * @param PDO $pdo
 * @param int $trackId
 * @param int $totalWaypoints Total number of waypoints in track
 * @return array Array of ranges with start, end, type, name, color, distance_km
 */
function getSegmentIndexRanges($pdo, $trackId, $totalWaypoints) {
    $segmentColors = [
        'stage' => '#EF4444',   // Red
        'liaison' => '#61CE70', // Green
        'lift' => '#F59E0B'     // Orange
    ];

    // Check if start_index column exists
    $hasIndexCols = false;
    try {
        $check = $pdo->query("SHOW COLUMNS FROM event_track_segments LIKE 'start_index'");
        $hasIndexCols = $check->fetch() !== false;
    } catch (Exception $e) {
        $hasIndexCols = false;
    }

    // Get all segments with their index ranges
    $markedSegments = [];

    if ($hasIndexCols) {
        $stmt = $pdo->prepare("
            SELECT id, segment_type, segment_name, start_index, end_index, distance_km, color
            FROM event_track_segments
            WHERE track_id = ? AND start_index IS NOT NULL AND end_index IS NOT NULL
            ORDER BY start_index ASC
        ");
        $stmt->execute([$trackId]);
        $markedSegments = $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    // If no segments with indices, return whole track as transport
    if (empty($markedSegments)) {
        // Get waypoints to calculate distance
        $waypoints = getTrackWaypointsForEditor($pdo, $trackId);
        $totalDist = !empty($waypoints) ? end($waypoints)['distance_km'] : 0;

        return [[
            'start' => 0,
            'end' => $totalWaypoints - 1,
            'type' => 'liaison',
            'name' => 'Transport',
            'color' => $segmentColors['liaison'],
            'distance_km' => round($totalDist, 2),
            'segment_id' => null
        ]];
    }

    // Build ranges including gaps (transport sections)
    $ranges = [];
    $currentPos = 0;
    $waypoints = getTrackWaypointsForEditor($pdo, $trackId);

    foreach ($markedSegments as $seg) {
        $segStart = (int)$seg['start_index'];
        $segEnd = (int)$seg['end_index'];

        // Add transport section before this segment if there's a gap
        if ($segStart > $currentPos) {
            $transportDist = 0;
            if (isset($waypoints[$segStart]) && isset($waypoints[$currentPos])) {
                $transportDist = $waypoints[$segStart]['distance_km'] - $waypoints[$currentPos]['distance_km'];
            }
            $ranges[] = [
                'start' => $currentPos,
                'end' => $segStart,
                'type' => 'liaison',
                'name' => 'Transport',
                'color' => $segmentColors['liaison'],
                'distance_km' => round($transportDist, 2),
                'segment_id' => null
            ];
        }

        // Add the marked segment
        $ranges[] = [
            'start' => $segStart,
            'end' => $segEnd,
            'type' => $seg['segment_type'],
            'name' => $seg['segment_name'],
            'color' => $seg['color'] ?? $segmentColors[$seg['segment_type']] ?? $segmentColors['liaison'],
            'distance_km' => (float)$seg['distance_km'],
            'segment_id' => (int)$seg['id']
        ];

        $currentPos = $segEnd;
    }

    // Add transport section after last segment if needed
    if ($currentPos < $totalWaypoints - 1) {
        $transportDist = 0;
        if (isset($waypoints[$totalWaypoints - 1]) && isset($waypoints[$currentPos])) {
            $transportDist = $waypoints[$totalWaypoints - 1]['distance_km'] - $waypoints[$currentPos]['distance_km'];
        }
        $ranges[] = [
            'start' => $currentPos,
            'end' => $totalWaypoints - 1,
            'type' => 'liaison',
            'name' => 'Transport',
            'color' => $segmentColors['liaison'],
            'distance_km' => round($transportDist, 2),
            'segment_id' => null
        ];
    }

    return $ranges;
}

/**
 * Get complete elevation profile data for a track
 * Returns full track waypoints with elevation + segment ranges for coloring
 *
 * @param PDO $pdo
 * @param int $trackId
 * @return array ['waypoints' => [...], 'segments' => [...], 'stats' => [...]]
 */
function getElevationProfileData($pdo, $trackId) {
    $waypoints = getTrackWaypointsForEditor($pdo, $trackId);

    if (empty($waypoints)) {
        return null;
    }

    $totalWaypoints = count($waypoints);
    $segmentRanges = getSegmentIndexRanges($pdo, $trackId, $totalWaypoints);

    // Calculate stats
    $elevations = array_filter(array_column($waypoints, 'elevation'), fn($e) => $e !== null);
    $minEle = !empty($elevations) ? min($elevations) : 0;
    $maxEle = !empty($elevations) ? max($elevations) : 0;
    $totalDistance = end($waypoints)['distance_km'] ?? 0;

    // Calculate total climb (excluding lifts)
    $totalClimb = 0;
    $totalDescent = 0;
    $prevEle = null;

    foreach ($waypoints as $i => $wp) {
        $ele = $wp['elevation'];
        if ($ele === null || $prevEle === null) {
            $prevEle = $ele;
            continue;
        }

        // Check if this point is within a lift segment
        $isLift = false;
        foreach ($segmentRanges as $seg) {
            if ($seg['type'] === 'lift' && $i >= $seg['start'] && $i <= $seg['end']) {
                $isLift = true;
                break;
            }
        }

        if (!$isLift) {
            $diff = $ele - $prevEle;
            if ($diff > 0) {
                $totalClimb += $diff;
            } else {
                $totalDescent += abs($diff);
            }
        }

        $prevEle = $ele;
    }

    // Simplify waypoints for transmission (every Nth point for large tracks)
    $simplifiedWaypoints = $waypoints;
    if ($totalWaypoints > 500) {
        $step = ceil($totalWaypoints / 500);
        $simplifiedWaypoints = [];
        for ($i = 0; $i < $totalWaypoints; $i += $step) {
            $simplifiedWaypoints[] = $waypoints[$i];
        }
        // Always include last point
        if (end($simplifiedWaypoints)['index'] !== $waypoints[$totalWaypoints - 1]['index']) {
            $simplifiedWaypoints[] = $waypoints[$totalWaypoints - 1];
        }

        // Recalculate segment ranges for simplified indices
        $indexMap = [];
        foreach ($simplifiedWaypoints as $newIdx => $wp) {
            $indexMap[$wp['index']] = $newIdx;
        }

        // Map segment ranges to simplified indices
        foreach ($segmentRanges as &$seg) {
            // Find closest simplified index for start
            $closestStart = 0;
            foreach ($simplifiedWaypoints as $newIdx => $wp) {
                if ($wp['index'] <= $seg['start']) {
                    $closestStart = $newIdx;
                }
            }
            // Find closest simplified index for end
            $closestEnd = count($simplifiedWaypoints) - 1;
            foreach ($simplifiedWaypoints as $newIdx => $wp) {
                if ($wp['index'] >= $seg['end']) {
                    $closestEnd = $newIdx;
                    break;
                }
            }
            $seg['start'] = $closestStart;
            $seg['end'] = $closestEnd;
        }
    }

    return [
        'waypoints' => array_map(function($wp) {
            return [
                'idx' => $wp['index'],
                'dist' => $wp['distance_km'],
                'ele' => $wp['elevation']
            ];
        }, $simplifiedWaypoints),
        'segments' => $segmentRanges,
        'stats' => [
            'total_distance_km' => round($totalDistance, 2),
            'min_elevation_m' => round($minEle),
            'max_elevation_m' => round($maxEle),
            'total_climb_m' => round($totalClimb),
            'total_descent_m' => round($totalDescent)
        ]
    ];
}
