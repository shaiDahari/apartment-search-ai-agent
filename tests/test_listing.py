"""Tests for the canonical apartment-listing model."""

from datetime import UTC, date, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from src.domain.listing import ApartmentListing


def test_accepts_required_fields_only() -> None:
    """Verify that a listing can be created using only required fields."""

    listing = ApartmentListing(
        source="example",
        source_listing_id="listing-123",
        listing_url="https://example.com/listings/123",
        raw_title="3-room apartment in Holon",
        extraction_timestamp=datetime(
            2026,
            7,
            29,
            9,
            30,
            tzinfo=UTC,
        ),
    )

    assert listing.source == "example"
    assert listing.source_listing_id == "listing-123"
    assert listing.monthly_rent is None

def test_rejects_missing_required_source() -> None:
    """Verify that a listing without a source is rejected."""

    with pytest.raises(ValidationError):
        ApartmentListing(
            source_listing_id="listing-123",
            listing_url="https://example.com/listings/123",
            raw_title="3-room apartment in Holon",
            extraction_timestamp=datetime(
                2026,
                7,
                29,
                9,
                30,
                tzinfo=UTC,
            ),
        )

def test_rejects_invalid_listing_url() -> None:
    """Verify that a listing with an invalid URL is rejected."""

    with pytest.raises(ValidationError):
        ApartmentListing(
            source="example",
            source_listing_id="listing-123",
            listing_url="not-a-valid-url",
            raw_title="3-room apartment in Holon",
            extraction_timestamp=datetime(
                2026,
                7,
                29,
                9,
                30,
                tzinfo=UTC,
            ),
        )

def test_rejects_negative_monthly_rent() -> None:
    """Verify that monthly rent must be greater than zero."""

    with pytest.raises(ValidationError):
        ApartmentListing(
            source="example",
            source_listing_id="listing-123",
            listing_url="https://example.com/listings/123",
            raw_title="3-room apartment in Holon",
            extraction_timestamp=datetime(
                2026,
                7,
                29,
                9,
                30,
                tzinfo=UTC,
            ),
            monthly_rent=-100,
        )

def test_model_dump_returns_dictionary() -> None:
    """Verify that a listing can be converted to a Python dictionary."""

    listing = ApartmentListing(
        source="example",
        source_listing_id="listing-123",
        listing_url="https://example.com/listings/123",
        raw_title="3-room apartment in Holon",
        extraction_timestamp=datetime(
            2026,
            7,
            29,
            9,
            30,
            tzinfo=UTC,
        ),
    )

    result = listing.model_dump()

    assert isinstance(result, dict)
    assert result["source"] == "example"
    assert result["source_listing_id"] == "listing-123"

def test_rejects_unexpected_field() -> None:
    """Verify that fields outside the canonical model are rejected."""

    with pytest.raises(ValidationError):
        ApartmentListing(
            source="example",
            source_listing_id="listing-123",
            listing_url="https://example.com/listings/123",
            raw_title="3-room apartment in Holon",
            extraction_timestamp=datetime(
                2026,
                7,
                29,
                9,
                30,
                tzinfo=UTC,
            ),
            swimming_pool=True,
        )

def test_validates_field_assignment() -> None:
    """Verify that changing an existing field triggers validation."""

    listing = ApartmentListing(
        source="example",
        source_listing_id="listing-123",
        listing_url="https://example.com/listings/123",
        raw_title="3-room apartment in Holon",
        extraction_timestamp=datetime(
            2026,
            7,
            29,
            9,
            30,
            tzinfo=UTC,
        ),
        monthly_rent=5000,
    )

    with pytest.raises(ValidationError):
        listing.monthly_rent = -100

def test_strips_surrounding_whitespace() -> None:
    """Verify that surrounding whitespace is removed from string fields."""

    listing = ApartmentListing(
        source="  example  ",
        source_listing_id="listing-123",
        listing_url="https://example.com/listings/123",
        raw_title="  3-room apartment in Holon  ",
        extraction_timestamp=datetime(
            2026,
            7,
            29,
            9,
            30,
            tzinfo=UTC,
        ),
    )

    assert listing.source == "example"
    assert listing.raw_title == "3-room apartment in Holon"

def test_accepts_complete_valid_listing() -> None:
    """Verify that all Phase 1 fields accept valid values."""

    listing = ApartmentListing(
        source="example",
        source_listing_id="listing-123",
        listing_url="https://example.com/listings/123",
        raw_title="3.5-room apartment in Holon",
        extraction_timestamp=datetime(
            2026,
            7,
            29,
            9,
            30,
            tzinfo=UTC,
        ),
        raw_description="Renovated apartment near public transportation.",
        monthly_rent=Decimal(5200),
        currency="ILS",
        city="Holon",
        neighborhood="Kiryat Ben Gurion",
        street="Begin",
        rooms=Decimal("3.5"),
        area_sqm=Decimal("82.5"),
        floor=2,
        available_from=date(2026, 8, 15),
        owner_or_broker="owner",
        publication_date=datetime(
            2026,
            7,
            28,
            18,
            0,
            tzinfo=UTC,
        ),
    )

    assert listing.monthly_rent == Decimal(5200)
    assert listing.rooms == Decimal("3.5")
    assert listing.area_sqm == Decimal("82.5")
    assert listing.available_from == date(2026, 8, 15)
    assert listing.owner_or_broker == "owner"