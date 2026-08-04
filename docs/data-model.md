# Canonical Rental Data Model

## Purpose
Define the normalized structure used for every apartment, regardless of source.

## Phase 1 Implementation Scope

The first Python model will implement the following subset of fields from the complete canonical model defined below.

### Required Fields

- source
- source_listing_id
- listing_url
- raw_title
- extraction_timestamp

### Optional Fields

- raw_description
- monthly_rent
- currency
- city
- neighborhood
- street
- rooms
- area_sqm
- floor
- available_from
- publisher_type
- publication_date

Fields not included in Phase 1 remain part of the planned canonical model and will be added incrementally.

## Core Listing Fields

### Identity
- internal_id
- source
- source_listing_id
- listing_url
- canonical_url
- first_seen
- last_seen
- publication_date
- last_updated
- listing_status

### Location
- city
- neighborhood
- street
- house_number
- approximate_address
- latitude
- longitude
- location_precision
- location_confidence

### Price
- monthly_rent
- currency
- arnona
- arnona_period
- vaad_bayit
- management_fee
- parking_fee
- broker_fee
- other_mandatory_fees
- estimated_utilities
- estimated_total_monthly_cost
- deposit
- guarantees_required

### Apartment
- rooms
- bedrooms
- bathrooms
- toilets
- area_sqm
- floor
- building_floors
- elevator
- parking
- parking_type
- balcony
- balcony_area_sqm
- mamad
- shelter
- storage
- furnished
- furniture_details
- air_conditioning
- accessibility
- renovated
- apartment_condition
- building_condition
- orientation
- natural_light
- noise_indicators

### Rental Conditions
- available_from
- flexible_entry
- contract_duration
- long_term_possible
- pets_allowed
- smokers_policy
- publisher_type

### Listing Metadata
- raw_title
- raw_description
- raw_price_text
- raw_location
- raw_payload
- extraction_timestamp
- extraction_confidence
- number_of_photos
- completeness_score

## Data Quality States

Each important field may have a confidence/state:

- CONFIRMED
- HIGH_CONFIDENCE
- MEDIUM_CONFIDENCE
- LOW_CONFIDENCE
- UNKNOWN
- CONFLICTING
- INFERRED

## Important Rules

1. UNKNOWN is not the same as NO.
2. Missing numeric values must not become zero.
3. Preserve raw values before normalization.
4. Every normalized field must retain source provenance.
5. Conflicting values from different sources must be preserved.
6. Duplicate listings must point to one canonical property where possible.
7. Do not invent exact addresses from approximate locations.

## Duplicate Matching Signals

Possible duplicate signals:
- normalized address
- coordinates
- rent
- rooms
- area
- floor
- phone/contact data
- title similarity
- description similarity
- image similarity

## Change History

Track:
- price changes
- description changes
- availability changes
- listing removal
- reposting
- status changes