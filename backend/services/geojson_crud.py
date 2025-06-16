
from shapely.geometry import shape
from shapely.validation import explain_validity
from geoalchemy2.shape import from_shape, to_shape
from geoalchemy2 import Geometry
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, delete, select, update, func, cast
from datetime import datetime


from ..pydm.schemas import GeoJSONUpload, GroupedRoadFeature
from ..sqlm.sqlm_tables import RoadFeature

def safe_str(val):
    """Lanes and Widgth can be String, List or None from the files """
    if isinstance(val, list):
        return ", ".join(map(str, val))
    return str(val) if val is not None else None

async def create_road_features(db: AsyncSession, geojson: GeoJSONUpload, customer_id: int):

    for feature in geojson.features:
        geom = shape(feature.geometry)

        # print("GEOM EXPLAIN:", explain_validity(geom))

        if geom.is_valid:
            db_obj = RoadFeature(
                customer_id=customer_id,
                highway=feature.properties.get("highway"),
                ref=feature.properties.get("ref"),
                lanes=safe_str(feature.properties.get("lanes")),
                oneway=safe_str(feature.properties.get("oneway")),
                length=safe_str(feature.properties.get("length")),
                width=safe_str(feature.properties.get("width")),
                geometry=from_shape(geom, srid=4326),
                is_current=True,
                created_at=datetime.now()
            )
            db.add(db_obj)
    await db.commit()

async def update_road_features(db: AsyncSession, geojson: GeoJSONUpload, customer_id: int):

    await db.execute(update(RoadFeature).where(
        and_(RoadFeature.customer_id == customer_id, RoadFeature.is_current == True))
        .values({RoadFeature.is_current: False, RoadFeature.updated_at: datetime.now()}))

    await db.commit()
    await create_road_features(db, geojson, customer_id)


async def delete_all_road_features(db: AsyncSession, customer_id: int):

    await db.execute(delete(RoadFeature).where(
        and_(RoadFeature.customer_id == customer_id)))

    await db.commit()



async def get_road_features_as_geojson(db: AsyncSession, customer_id: int, as_of: datetime = None):

    if as_of:
        query = await db.execute(select(RoadFeature).where(and_(RoadFeature.customer_id == customer_id, RoadFeature.created_at <= as_of)))
    else:
        query = await db.execute(select(RoadFeature).where(and_(RoadFeature.customer_id == customer_id, RoadFeature.is_current == True)))

    features = []

    query_result = query.scalars().all()

    for row in query_result:
        geom = to_shape(row.geometry)
        features.append({
            "type": "Feature",
            "properties": {
                "highway": row.highway,
                "ref": row.ref,
                "lanes": row.lanes,
                "oneway": row.oneway,
                "length": row.length,
                "width": row.width,
                "current": row.is_current,
                "created_at": row.created_at.isoformat()
            },
            "geometry": geom.__geo_interface__
        })

    return {
        "type": "FeatureCollection",
        "features": features
    }

async def get_roads_timestamps(db: AsyncSession, customer_id: int):
    """Fetch data to a table in frontend so can choose old versions"""
    stmt = (
        select(
            RoadFeature.updated_at,
            RoadFeature.is_current,
            RoadFeature.customer_id,
            func.count(RoadFeature.geometry).label("geometry_points")
        )
        .group_by(
            RoadFeature.updated_at,
            RoadFeature.is_current,
            RoadFeature.customer_id
        )
        .having(RoadFeature.customer_id == customer_id)
    )
    result = await db.execute(stmt)

    rows = result.mappings().all()
    return [GroupedRoadFeature.model_validate(row) for row in rows]
