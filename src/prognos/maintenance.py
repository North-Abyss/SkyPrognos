"""Maintenance scheduling logic."""

import math


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in km."""
    R = 6371.0  # Earth radius in kilometers
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)
    ) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def find_nearest_base(aircraft_lat, aircraft_lon, bases_df, parts_df, required_part):
    """Find the nearest airbase that has the required part in stock and crew capacity."""
    available_bases = parts_df[(parts_df["part_id"] == required_part) & (parts_df["stock"] > 0)]
    if available_bases.empty:
        return None

    valid_bases = bases_df[
        bases_df["base_id"].isin(available_bases["base_id"]) & (bases_df["crew_capacity"] > 0)
    ].copy()
    if valid_bases.empty:
        return None

    valid_bases["distance"] = valid_bases.apply(
        lambda row: haversine_distance(aircraft_lat, aircraft_lon, row["lat"], row["lon"]), axis=1
    )

    nearest = valid_bases.loc[valid_bases["distance"].idxmin()]
    return nearest.to_dict()
