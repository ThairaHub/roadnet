import json
from fastapi import APIRouter, Depends, Form, HTTPException, Query, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from .dependencies import ResponseWrapper, async_get_db
from ..pydm.schemas import GeoJSONUpload, GroupedRoadFeature
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from ..setup.auth import get_current_user

from ..services import geojson_crud


router = APIRouter(prefix="/geojson", tags=["GeoJson"])


@router.get("/roads", response_model=ResponseWrapper[dict])
async def get_roads(as_of: datetime = Query(None), user_id: int = Depends(get_current_user), db: AsyncSession = Depends(async_get_db)):
    try:
        print("GET ROADS CALL HERE LOGIN ------------------")
        result = await geojson_crud.get_road_features_as_geojson(db, user_id, as_of)
        
        if not result["features"]:
            raise HTTPException(status_code=404, detail="No features found not found")
        
        return ResponseWrapper(
            success=True,
            data=result,
            error=None
        )
    
    except SQLAlchemyError as e:
        await db.rollback()
        return ResponseWrapper(success=False, data=None, error=f"Database error: {str(e)}")

    except HTTPException as e:
        raise e 

    except Exception as e:
        await db.rollback()
        return ResponseWrapper(success=False, data=None, error=f"Unexpected error: {str(e)}")

@router.get("/roads_timestamps", response_model=ResponseWrapper[List[GroupedRoadFeature]])
async def get_roads(user_id: int = Depends(get_current_user), db: AsyncSession = Depends(async_get_db)):
    try:

        result = await geojson_crud.get_roads_timestamps(db, user_id)
        
        if not result:
            raise HTTPException(status_code=404, detail="No features found not found")
        
        return ResponseWrapper(
            success=True,
            data=result,
            error=None
        )
    
    except SQLAlchemyError as e:
        await db.rollback()
        return ResponseWrapper(success=False, data=None, error=f"Database error: {str(e)}")

    except HTTPException as e:
        raise e 

    except Exception as e:
        await db.rollback()
        return ResponseWrapper(success=False, data=None, error=f"Unexpected error: {str(e)}")

@router.post("/upload", response_model=ResponseWrapper[dict])
async def upload_geojson(
    file: UploadFile = File(...), 
    user_id: int = Depends(get_current_user), 
    db: AsyncSession = Depends(async_get_db)
):
    try:
        contents = await file.read()
        geojson = GeoJSONUpload(**json.loads(contents))
        await geojson_crud.create_road_features(db, geojson, user_id)
        return ResponseWrapper(success=True, data={"status": "uploaded"}, error=None)

    except SQLAlchemyError as e:
        await db.rollback()
        return ResponseWrapper(success=False, data=None, error=f"Database error: {str(e)}")

    except HTTPException as e:
        raise e 

    except Exception as e:
        await db.rollback()
        return ResponseWrapper(success=False, data=None, error=f"Unexpected error: {str(e)}")

@router.put("/update", response_model=ResponseWrapper[dict])
async def update_geojson(
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(async_get_db)
):
    try:
        contents = await file.read()
        geojson = GeoJSONUpload(**json.loads(contents))
        await geojson_crud.update_road_features(db, geojson, user_id)

        return ResponseWrapper(success=True, data={"status": "updated"}, error=None)

    except SQLAlchemyError as e:
        await db.rollback()
        return ResponseWrapper(success=False, data=None, error="Database error")

    except HTTPException as e:
        raise e 

    except Exception as e:
        await db.rollback()
        return ResponseWrapper(success=False, data=None, error="Unexpected error")

@router.delete("/delete_all", response_model=ResponseWrapper[dict])
async def delete_all_geojson(
    db: AsyncSession = Depends(async_get_db),
    user_id: int = Depends(get_current_user)

):
    try:
        await geojson_crud.delete_all_road_features(db, user_id)
        return ResponseWrapper(success=True, data={"status": "deleted"}, error=None)

    except SQLAlchemyError as e:
        await db.rollback()
        return ResponseWrapper(success=False, data=None, error="Database error")

    except HTTPException as e:
        raise e 

    except Exception as e:
        await db.rollback()
        return ResponseWrapper(success=False, data=None, error="Unexpected error")