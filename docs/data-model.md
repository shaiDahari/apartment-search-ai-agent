# Canonical Rental Data Model

## Purpose
Define the normalized structure used for every apartment, regardless of source.

## Phase 1 Domain Implementation Scope

The current Python `ApartmentListing` model implements the following subset
of fields from the complete canonical model defined below.

### Required Fields

- source
- source_listing_id
- listing_url
- raw_title
- extraction_timestamp

### Optional Nullable Fields

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
- publication_date

### Explicit Unknown-Default Fields

- publisher_type

`publisher_type` uses the canonical values `owner`, `broker`, and `unknown`.
Missing publisher information is represented as `unknown`, not NULL.

Fields not included in the current Python model remain part of the planned
canonical model and will be added incrementally when approved.

## Phase 1 Persistence Design

Phase 1 persistence is documented in
[`docs/persistence-design.md`](persistence-design.md).

The persistence design uses exactly one entity, `apartment_listings`, with
`listing_id` as the internal persistence primary key and
`(source, source_listing_id)` as the unique external listing identity.

It also documents Owner-approved persistence fields that are not yet
implemented in the Python `ApartmentListing` domain model, including recurring
apartment costs, included-in-rent status fields, broker-fee fields, and
`protected_space_type`.

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
- arnona_amount
- arnona_period_months
- vaad_bayit
- arnona_included_in_rent
- vaad_bayit_included_in_rent
- internet_included_in_rent
- cable_tv_included_in_rent
- parking_fee
- broker_fee_amount
- broker_fee_terms
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
- protected_space_type
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
