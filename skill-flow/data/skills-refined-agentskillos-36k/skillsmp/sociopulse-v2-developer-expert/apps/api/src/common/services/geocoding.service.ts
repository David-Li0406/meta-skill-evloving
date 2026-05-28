import { Injectable, Logger } from '@nestjs/common';

interface GeocodingResult {
    longitude: number;
    latitude: number;
    label: string;
    city: string;
    postalCode: string;
    confidence: number;
}

interface AddressFeature {
    type: string;
    geometry: {
        type: string;
        coordinates: [number, number]; // [longitude, latitude]
    };
    properties: {
        label: string;
        score: number;
        housenumber?: string;
        id: string;
        name: string;
        postcode: string;
        citycode: string;
        city: string;
        context: string;
        type: string;
        importance: number;
        street?: string;
    };
}

interface AddressAPIResponse {
    type: string;
    version: string;
    features: AddressFeature[];
    attribution: string;
    licence: string;
    query: string;
    limit: number;
}

/**
 * GeocodingService
 * Uses the French Government Address API (api-adresse.data.gouv.fr)
 * No API key required - completely free
 */
@Injectable()
export class GeocodingService {
    private readonly logger = new Logger(GeocodingService.name);
    private readonly baseUrl = 'https://api-adresse.data.gouv.fr';

    /**
     * Geocode an address string to coordinates
     * @param address Full address string (e.g., "10 rue de la Paix, Paris")
     * @returns GeocodingResult with lat/lng or null if not found
     */
    async geocodeAddress(address: string): Promise<GeocodingResult | null> {
        if (!address || address.trim().length < 3) {
            this.logger.warn('Address too short for geocoding');
            return null;
        }

        try {
            const encodedAddress = encodeURIComponent(address.trim());
            const url = `${this.baseUrl}/search/?q=${encodedAddress}&limit=1`;

            this.logger.debug(`Geocoding address: ${address}`);

            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                },
            });

            if (!response.ok) {
                this.logger.error(`Geocoding API error: ${response.status}`);
                return null;
            }

            const data: AddressAPIResponse = await response.json();

            if (!data.features || data.features.length === 0) {
                this.logger.warn(`No results for address: ${address}`);
                return null;
            }

            const feature = data.features[0];
            const [longitude, latitude] = feature.geometry.coordinates;

            const result: GeocodingResult = {
                longitude,
                latitude,
                label: feature.properties.label,
                city: feature.properties.city,
                postalCode: feature.properties.postcode,
                confidence: feature.properties.score,
            };

            this.logger.log(
                `Geocoded "${address}" → [${latitude}, ${longitude}] (${result.city})`
            );

            return result;
        } catch (error) {
            this.logger.error(`Geocoding failed for "${address}":`, error);
            return null;
        }
    }

    /**
     * Geocode from city and postal code only
     * @param city City name
     * @param postalCode Postal code
     * @returns GeocodingResult or null
     */
    async geocodeCityPostalCode(
        city: string,
        postalCode: string
    ): Promise<GeocodingResult | null> {
        const address = `${city} ${postalCode}`;
        return this.geocodeAddress(address);
    }

    /**
     * Reverse geocode from coordinates to address
     * @param longitude Longitude
     * @param latitude Latitude
     * @returns Address label or null
     */
    async reverseGeocode(
        longitude: number,
        latitude: number
    ): Promise<string | null> {
        try {
            const url = `${this.baseUrl}/reverse/?lon=${longitude}&lat=${latitude}`;

            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                },
            });

            if (!response.ok) {
                return null;
            }

            const data: AddressAPIResponse = await response.json();

            if (!data.features || data.features.length === 0) {
                return null;
            }

            return data.features[0].properties.label;
        } catch (error) {
            this.logger.error(`Reverse geocoding failed:`, error);
            return null;
        }
    }

    /**
     * Calculate distance between two points using Haversine formula
     * @returns Distance in kilometers
     */
    calculateDistance(
        lat1: number,
        lon1: number,
        lat2: number,
        lon2: number
    ): number {
        const R = 6371; // Earth's radius in km
        const dLat = this.toRad(lat2 - lat1);
        const dLon = this.toRad(lon2 - lon1);

        const a =
            Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(this.toRad(lat1)) *
            Math.cos(this.toRad(lat2)) *
            Math.sin(dLon / 2) *
            Math.sin(dLon / 2);

        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    }

    private toRad(degrees: number): number {
        return degrees * (Math.PI / 180);
    }
}
