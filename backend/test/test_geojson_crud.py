import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from shapely.geometry import mapping, LineString
from datetime import datetime

from ..sqlm.sqlm_tables import RoadFeature  
from ..pydm.schemas import GeoJSONUpload, GroupedRoadFeature
from ..services.geojson_crud import *
from geoalchemy2.shape import from_shape

class FakeRoadFeature:
    def __init__(self):
        self.highway = "residential"
        self.ref = "R1"
        self.lanes = "2"
        self.oneway = "no"
        self.length = "150.0"
        self.width = "4.5"
        self.is_current = True
        self.created_at = datetime(2024, 1, 1)
        self.geometry = from_shape(LineString([(0, 0), (1, 1)]), srid=4326)


@pytest.mark.asyncio
async def test_create_road_features():
    
    geometry = LineString([(0, 0), (1, 1)])
    feature = {
        "type": "Feature",
        "geometry": mapping(geometry),
        "properties": {
            "highway": "residential",
            "ref": "A1",
            "lanes": ["2", "3"],
            "oneway": "yes",
            "length": "100.5",
            "width": "5.0"
        }
    }

    geojson = GeoJSONUpload(
        type="FeatureCollection",
        name="Test Collection",
        crs={'EPSG':'4326'},
        features=[feature]
    )

    
    mock_session = AsyncMock()
    mock_add = MagicMock()
    mock_session.add = mock_add
    mock_session.commit = AsyncMock()

    
    await create_road_features(mock_session, geojson, customer_id=42)

    
    assert mock_add.call_count == 1
    added_obj = mock_add.call_args[0][0]

    assert isinstance(added_obj, RoadFeature)
    assert added_obj.customer_id == 42
    assert added_obj.highway == "residential"
    assert added_obj.ref == "A1"
    assert added_obj.lanes == "2, 3"
    assert added_obj.oneway == "yes"
    assert added_obj.length == "100.5"
    assert added_obj.width == "5.0"
    assert added_obj.is_current is True
    assert isinstance(added_obj.created_at, datetime)

    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
@patch("backend.services.geojson_crud.create_road_features", new_callable=AsyncMock)
async def test_update_road_features(mock_create_road_features):
    
    geometry = LineString([(0, 0), (1, 1)])
    feature = {
        "type": "Feature",
        "geometry": mapping(geometry),
        "properties": {
            "highway": "primary",
            "ref": "B2",
            "lanes": "2",
            "oneway": "no",
            "length": "200",
            "width": "6.0"
        }
    }

    geojson = GeoJSONUpload(
        type="FeatureCollection",
        name="Update Test",
        crs={'EPSG':'4326'},
        features=[feature]
    )

    mock_session = AsyncMock()
    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()

    
    await update_road_features(mock_session, geojson, customer_id=123)

    
    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    mock_create_road_features.assert_awaited_once_with(mock_session, geojson, 123)


@pytest.mark.asyncio
async def test_delete_all_road_features():
    
    mock_session = AsyncMock()
    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()

    
    await delete_all_road_features(mock_session, customer_id=999)

    
    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_road_features_as_geojson_without_as_of():
    mock_session = AsyncMock()

    
    mock_query_result = MagicMock()
    mock_query_result.scalars.return_value.all.return_value = [FakeRoadFeature()]
    mock_session.execute.return_value = mock_query_result

    result = await get_road_features_as_geojson(mock_session, customer_id=42)

    assert result["type"] == "FeatureCollection"
    assert len(result["features"]) == 1

    feature = result["features"][0]
    assert feature["type"] == "Feature"
    assert feature["properties"]["highway"] == "residential"
    assert feature["geometry"]["type"] == "LineString"
    assert "coordinates" in feature["geometry"]

    mock_session.execute.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_road_features_as_geojson_with_as_of():
    mock_session = AsyncMock()

    
    mock_query_result = MagicMock()
    mock_query_result.scalars.return_value.all.return_value = [FakeRoadFeature()]
    mock_session.execute.return_value = mock_query_result

    as_of_time = datetime(2024, 6, 1)

    result = await get_road_features_as_geojson(mock_session, customer_id=42, as_of=as_of_time)

    assert result["type"] == "FeatureCollection"
    assert len(result["features"]) == 1
    assert result["features"][0]["properties"]["created_at"] == "2024-01-01T00:00:00"

    mock_session.execute.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_roads_timestamps():
    
    mock_session = AsyncMock()

    
    row_data = {
        "updated_at": datetime(2024, 6, 1, 12, 0, 0),
        "is_current": True,
        "customer_id": 42,
        "geometry_points": 5
    }

    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = [row_data]
    mock_session.execute.return_value = mock_result

    
    result = await get_roads_timestamps(mock_session, customer_id=42)

    
    assert len(result) == 1
    item = result[0]

    assert isinstance(item, GroupedRoadFeature)
    assert item.customer_id == 42
    assert item.geometry_points == 5
    assert item.is_current is True
    assert item.updated_at == datetime(2024, 6, 1, 12, 0, 0)

    mock_session.execute.assert_awaited_once()
