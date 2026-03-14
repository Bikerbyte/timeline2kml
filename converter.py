import json
from pathlib import Path
import simplekml


def _parse_lat_lng(lat_lng_value: str):
    if not lat_lng_value:
        return None

    cleaned = lat_lng_value.replace("Â°", "").replace("°", "").strip()
    parts = cleaned.split(", ")
    if len(parts) != 2:
        parts = [part.strip() for part in cleaned.split(",")]
    if len(parts) != 2:
        return None

    try:
        lat, lon = map(float, parts)
    except (TypeError, ValueError):
        return None

    return lat, lon


def convert_timeline_to_kml(input_path: str, output_path: str):
    source_path = Path(input_path)
    destination_path = Path(output_path)

    if not source_path.is_file():
        raise FileNotFoundError(f"Input file not found: {source_path}")

    try:
        with source_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in input file: {source_path}") from exc

    geojson = {
        "type": "FeatureCollection",
        "features": [],
    }

    for segment in data.get("semanticSegments", []):
        # ---- Visit ----
        if "visit" in segment:
            visit = segment.get("visit", {})
            top_candidate = visit.get("topCandidate", {})
            place_location = top_candidate.get("placeLocation", {})
            parsed = _parse_lat_lng(place_location.get("latLng", ""))

            if parsed is not None:
                lat, lon = parsed
                geojson["features"].append(
                    {
                        "type": "Feature",
                        "geometry": {"type": "Point", "coordinates": [lon, lat]},
                        "properties": {
                            "type": "visit",
                            "semanticType": top_candidate.get("semanticType", "Unknown"),
                            "startTime": segment.get("startTime"),
                            "endTime": segment.get("endTime"),
                        },
                    }
                )

        # ---- Activity Record ----
        if "activityRecord" in segment:
            act = segment.get("activityRecord", {})
            activities = act.get("probableActivities", [])
            if activities:
                best = max(activities, key=lambda x: x.get("confidence", 0))
                geojson["features"].append(
                    {
                        "type": "Feature",
                        "geometry": None,
                        "properties": {
                            "type": "activity",
                            "timestamp": act.get("timestamp"),
                            "bestActivity": best.get("type", "Unknown"),
                            "confidence": best.get("confidence"),
                        },
                    }
                )

        # ---- Timeline Path ----
        if "timelinePath" in segment:
            coords = []
            for point in segment.get("timelinePath", []):
                parsed = _parse_lat_lng(point.get("point", ""))
                if parsed is None:
                    continue
                lat, lon = parsed
                coords.append([lon, lat])

            if coords:
                geojson["features"].append(
                    {
                        "type": "Feature",
                        "geometry": {"type": "LineString", "coordinates": coords},
                        "properties": {"type": "path"},
                    }
                )

    kml = simplekml.Kml()

    for feature in geojson["features"]:
        geom = feature["geometry"]
        props = feature["properties"]

        if geom is None:
            kml.newpoint(
                name=f"Activity: {props['bestActivity']}",
                description=(
                    f"Confidence: {props['confidence']}<br>"
                    f"Time: {props.get('timestamp')}"
                ),
            )
        elif geom["type"] == "Point":
            lon, lat = geom["coordinates"]
            kml.newpoint(
                name=f"Visit ({props.get('semanticType')})",
                coords=[(lon, lat)],
                description=(
                    f"Start: {props.get('startTime')}<br>"
                    f"End: {props.get('endTime')}"
                ),
            )
        elif geom["type"] == "LineString":
            kml.newlinestring(
                name="Path",
                coords=geom["coordinates"],
                description="Timeline Path",
            )

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save KML
    kml.save(str(destination_path))
