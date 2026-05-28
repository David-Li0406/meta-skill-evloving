# Jurisdiction Routing in Solano County

## The Mailing Address Problem

**Critical**: A mailing address does NOT determine legal jurisdiction.

The United States Postal Service assigns addresses based on the nearest post office or delivery route, not municipal boundaries. This means:

- An address with "Fairfield, CA 94534" might be in unincorporated Solano County
- An address with "Vacaville, CA" might be in a different city's sphere of influence
- Rural addresses often use the nearest city name despite being unincorporated

**Always verify jurisdiction by checking city boundary layers before routing queries.**

## Incorporated Cities

Solano County contains 7 incorporated cities, each with its own:
- Zoning ordinance
- Planning department
- Building department
- Code enforcement

### City Details

#### Benicia
- Population: ~28,000
- Known for: Historic downtown, industrial waterfront
- Planning Contact: (707) 746-4200
- Zoning Code: Benicia Municipal Code Title 17

#### Dixon
- Population: ~22,000
- Known for: Agricultural heritage, May Fair
- Planning Contact: (707) 678-7000
- Zoning Code: Dixon Municipal Code Title 18

#### Fairfield
- Population: ~120,000 (largest city)
- Known for: County seat, Travis AFB adjacent
- Planning Contact: (707) 428-7461
- Zoning Code: Fairfield Municipal Code Title 25

#### Rio Vista
- Population: ~10,000
- Known for: Delta location, wind farms
- Planning Contact: (707) 374-6451
- Zoning Code: Rio Vista Municipal Code Title 17

#### Suisun City
- Population: ~30,000
- Known for: Waterfront, historic downtown
- Planning Contact: (707) 421-7335
- Zoning Code: Suisun City Municipal Code Title 18

#### Vacaville
- Population: ~105,000
- Known for: Outlet shopping, agriculture transition
- Planning Contact: (707) 449-5140
- Zoning Code: Vacaville Municipal Code Title 14

#### Vallejo
- Population: ~122,000
- Known for: Mare Island, waterfront
- Planning Contact: (707) 648-4326
- Zoning Code: Vallejo Municipal Code Title 16

## Unincorporated Solano County

Areas outside city limits are governed by Solano County directly.

- **Planning**: Resource Management Department (707) 784-6765
- **Building**: Building Division (707) 784-6765
- **Zoning Code**: Solano County Code Chapter 28

### Unincorporated Communities

Named places that are NOT cities (no municipal government):
- Green Valley
- Elmira
- Birds Landing
- Collinsville
- Hartley
- Maine Prairie
- Rockville
- Tolenas

These use county services despite having recognizable place names.

## Spheres of Influence

Cities have "spheres of influence" (SOI) - areas they may eventually annex. Properties in SOIs are:
- Currently under county jurisdiction
- May be subject to city review for certain projects
- May have development agreements with the city

Check both city boundaries AND sphere of influence when answering jurisdiction questions.

## How to Determine Jurisdiction

1. **Get coordinates** for the address/parcel
2. **Query City_Boundaries layer** to check if point is within any city
3. **If inside city boundary** → Use that city's services
4. **If outside all city boundaries** → Use county services
5. **Note the jurisdiction** in your response

## Common Edge Cases

### Travis AFB Area
Federal land - neither city nor county jurisdiction for on-base areas. Off-base housing may be in Fairfield or unincorporated.

### Suisun Marsh
Primarily unincorporated county with special Marsh Protection regulations.

### Industrial Parks
Some straddle city/county boundaries. Check each parcel individually.

### Recent Annexations
City boundaries change. GIS data may lag behind official annexations. When in doubt, contact the affected city.
