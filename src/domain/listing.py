"""Define the canonical Phase 1 apartment-listing data model.

This module contains the shared apartment-listing structure used throughout
the application. Crawlers should convert source-specific listing data into
this normalized model before the data is processed, compared, or stored.

The model validates field types and rejects unexpected fields so that all
parts of the application work with the same predictable structure.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field


class ApartmentListing(BaseModel):
    """Represent one normalized apartment listing.

    This model is the canonical data contract shared by all apartment
    crawlers. Each crawler may collect information in a different format,
    but it must convert that information into this structure before passing
    it to later application components.

    Required fields identify the listing and record when it was collected.
    Optional fields represent information that may not be available from
    every source.

    Attributes:
        source:
            Name of the website or data source from which the listing was
            collected, such as ``yad2`` or ``facebook``.

        source_listing_id:
            Listing identifier assigned by the original source. It should be
            stored as a string because some websites use non-numeric IDs.

        listing_url:
            Valid HTTP or HTTPS URL of the original apartment listing.

        raw_title:
            Original title exactly as it appeared in the source listing,
            except for surrounding whitespace removed by the model.

        extraction_timestamp:
            Date and time when the application collected or extracted the
            listing.

        raw_description:
            Original unprocessed listing description. ``None`` means that no
            description was provided or collected.

        monthly_rent:
            Monthly rent amount before optional utilities or additional fees.
            The value must be greater than zero when provided.

        currency:
            Three-letter uppercase ISO-style currency code, such as ``ILS``
            or ``USD``.

        city:
            Normalized city name associated with the apartment.

        neighborhood:
            Neighborhood or local area within the city.

        street:
            Street name without requiring a house number.

        rooms:
            Number of rooms advertised for the apartment. ``Decimal`` allows
            values such as ``2.5`` or ``3.5``.

        area_sqm:
            Apartment area in square meters. The value must be greater than
            zero when provided.

        floor:
            Floor on which the apartment is located. Negative values may
            represent basement levels, and zero may represent the ground
            floor.

        available_from:
            Date from which the apartment is available for occupancy.

        publisher_type:
            Indicates whether the listing was published by the property owner,
            by a real-estate broker, or the publisher type is unknown.

        publication_date:
            Date and time when the original source published the listing.

    Raises:
        pydantic.ValidationError:
            If a required field is missing, a field has an invalid type,
            a numeric constraint is violated, the URL is invalid, the
            currency format is invalid, or an unexpected field is supplied.

    Notes:
        Use ``model_dump()`` to convert an instance to a Python dictionary.

        Use ``model_dump(mode="json")`` when values such as dates, datetimes,
        decimals, and URLs need JSON-compatible representations.

    Example:
        >>> listing = ApartmentListing(
        ...     source="example",
        ...     source_listing_id="12345",
        ...     listing_url="https://example.com/listings/12345",
        ...     raw_title="3-room apartment in Holon",
        ...     extraction_timestamp=datetime.now(),
        ...     monthly_rent=Decimal("5200"),
        ...     currency="ILS",
        ... )
        >>> listing.model_dump()
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    source: str = Field(
        min_length=1,
        description=(
            "Name of the website or data source from which the listing "
            "was collected."
        ),
    )

    source_listing_id: str = Field(
        min_length=1,
        description="Identifier assigned to the listing by its original source.",
    )

    listing_url: AnyHttpUrl = Field(
        description="HTTP or HTTPS URL of the original apartment listing.",
    )

    raw_title: str = Field(
        min_length=1,
        description="Original listing title before normalization.",
    )

    extraction_timestamp: datetime = Field(
        description="Date and time when the listing was collected.",
    )

    raw_description: str | None = Field(
        default=None,
        description="Original unprocessed listing description.",
    )

    monthly_rent: Decimal | None = Field(
        default=None,
        gt=0,
        description="Monthly rent amount, which must be greater than zero.",
    )

    currency: str | None = Field(
        default=None,
        pattern=r"^[A-Z]{3}$",
        description="Three-letter uppercase currency code, such as ILS or USD.",
    )

    city: str | None = Field(
        default=None,
        description="Normalized city name.",
    )

    neighborhood: str | None = Field(
        default=None,
        description="Neighborhood or local area within the city.",
    )

    street: str | None = Field(
        default=None,
        description="Street name associated with the apartment.",
    )

    rooms: Decimal | None = Field(
        default=None,
        gt=0,
        description="Number of rooms, including fractional values such as 2.5.",
    )

    area_sqm: Decimal | None = Field(
        default=None,
        gt=0,
        description="Apartment area in square meters.",
    )

    floor: int | None = Field(
        default=None,
        description="Floor number, where zero may represent the ground floor.",
    )

    available_from: date | None = Field(
        default=None,
        description="Date from which the apartment is available.",
    )

    publisher_type: Literal["owner", "broker", "unknown"] = Field(
        default="unknown",
        description="Whether the listing was published by an owner, broker, or is unknown.",
    )

    publication_date: datetime | None = Field(
        default=None,
        description="Date and time when the source published the listing.",
    )