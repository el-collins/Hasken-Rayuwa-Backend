# routes/states.py
import os
import uuid
import asyncio
import pandas as pd
from typing import List
from bson import ObjectId
from pathlib import Path as FilePath
from schemas.states import StateDataInput, StateDataMultiUpdate
from fastapi.responses import JSONResponse
from fastapi import (
    APIRouter,
    Body,
    Path,
    HTTPException,
    UploadFile,
    File,
    status,
    Query,
    Depends,
)


# from core.auth import authenticate_user, logout_user
from db.database import get_db
from models.states import States


states_router = router = APIRouter(tags=["States"])

UPLOAD_DIRECTORY = "./uploads"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


async def save_file(file: UploadFile) -> FilePath:
    file_path = FilePath(UPLOAD_DIRECTORY) / f"{uuid.uuid4()}.xlsx"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    return file_path


async def delete_file(file_path: FilePath) -> None:
    os.remove(file_path)


async def read_excel_file(file_path: FilePath) -> pd.DataFrame:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, pd.read_excel, file_path)


async def process_file(df: pd.DataFrame, db) -> None:

    data_to_insert = df.to_dict(orient="records")

    try:
        for record in data_to_insert:
            state = record["State"].capitalize()
            village = record["Village"]

            existing_record = await db.states_collection.find_one(
                {"State": state, "Village": village}
            )

            record_data = {
                "Lga": record["L.G.A"],
                "Ward": record["Ward"],
                "Estimated_Christian_Population": record["Esti Christians population"],
                "Estimated_Muslim_Population": record["Esti Muslims"],
                "Estimated_Traditional_Religion_Population": record[
                    "Esti Traditional People"
                ],
                "Converts": record["Converts"],
                "Estimated_Total_Population": record["Esti population of the village"],
                "Film_Attendance": record["Film Attendance"],
                "People_Group": record["People Group"],
                "Practiced_Religion": record["Practiced Religion"],
            }

            if existing_record:
                await db.states_collection.update_one(
                    {"_id": existing_record["_id"]}, {"$set": record_data}
                )
            else:
                await db.states_collection.insert_one(
                    {"State": state, "Village": village, **record_data}
                )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error inserting data: {str(e)}")


@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...), db=Depends(get_db)):

    try:
        for file in files:
            file_path = await save_file(file)
            df = await read_excel_file(file_path)
            await process_file(df, db)
            await delete_file(file_path)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "File(s) uploaded and data saved successfully."},
        )

    except Exception as e:
        print(f"Error uploading files: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )


@router.post("/add_state_data")
async def manual_input(
    state_data: StateDataInput,
    db=Depends(get_db),
):
    data = {
        "State": state_data.state,
        "Lga": state_data.lga,
        "Ward": state_data.ward,
        "Village": state_data.village,
        "Estimated_Christian_Population": state_data.estimated_christian_population,
        "Estimated_Muslim_Population": state_data.estimated_muslim_population,
        "Estimated_Traditional_Religion_Population": state_data.estimated_traditional_religion_population,
        "Converts": state_data.converts,
        "Estimated_Total_Population": state_data.estimated_total_population,
        "Film_Attendance": state_data.film_attendance,
        "People_Group": state_data.people_group,
        "Practiced_Religion": state_data.practiced_religion,
    }

    try:
        await db.states_collection.insert_one(data)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Data saved successfully."},
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )


@router.get("/states_data")
async def states_list(
    state: str | None = Query(None),
    skip: int = 0,
    limit: int = 5,
    db=Depends(get_db),
) -> dict:
    """
    Retrieves a list of State from the database based on the specified criteria.

    Returns:
        dict: A dictionary containing the list of State objects and their aggregate data.
    """
    try:
        pipeline = []
        match_stage = {}

        if state:
            match_stage["State"] = state
            pipeline.append({"$match": match_stage})

        # Get paginated data
        data_pipeline = pipeline.copy()
        data_pipeline.extend([{"$skip": skip}, {"$limit": limit}])

        cursor = db.states_collection.aggregate(data_pipeline)
        data = await cursor.to_list(length=None)

        # Get totals
        totals_pipeline = []
        if state:
            totals_pipeline.append({"$match": {"State": state}})

        totals_pipeline.append(
            {
                "$group": {
                    "_id": None,
                    "total_estimated_christian_population": {
                        "$sum": "$Estimated_Christian_Population"
                    },
                    "total_estimated_muslim_population": {
                        "$sum": "$Estimated_Muslim_Population"
                    },
                    "total_estimated_traditional_religion_population": {
                        "$sum": "$Estimated_Traditional_Religion_Population"
                    },
                    "total_converts": {"$sum": "$Converts"},
                    "total_estimated_total_population": {
                        "$sum": "$Estimated_Total_Population"
                    },
                    "total_film_attendance": {"$sum": "$Film_Attendance"},
                }
            }
        )
        totals_cursor = db.states_collection.aggregate(totals_pipeline)
        totals_list = await totals_cursor.to_list(length=None)
        totals = totals_list[0] if totals_list else {}

        if "_id" in totals:
            del totals["_id"]

        # Convert str to string in response
        for item in data:
            item["id"] = str(item.pop("_id"))

        return {"status": "success", "data": data, "totals": totals}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# # Retrieves state by ID
@router.get("/state_data/{state_id}")
async def get_state_data(state_id: str, db = Depends(get_db)) -> dict:
    """
    Retrieves a State from the database based on the specified ID.

    Args:
        state_id (UUID): The ID of the State to retrieve.

    Returns:
        dict: A dictionary containing the State object.
    """
    try:
        state = await db.states_collection.find_one({"_id": ObjectId(state_id)})
        print(state)
        if not state:
            raise HTTPException(status_code=404, detail="State data not found")

        state["id"] = str(state.pop("_id"))
        return {"status": "success", "data": state}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/states")
async def get_states(db = Depends(get_db)) -> dict:
    """
    Retrieves all States from the database.

    Returns:
        dict: A dictionary containing the list of States.
    """
    try:
        cursor = db.states_collection.distinct("State")
        states = await cursor
        return {"status": "success", "data": states}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/edit_state_data/{state_id}")
async def edit_state_data(
    state_id: str = Path(...),
    update_data: StateDataMultiUpdate = Body(...),
    db = Depends(get_db),
):
    try:
        # Verify state exists
        state = await db.states_collection.find_one({"_id": ObjectId(state_id)})
        if not state:
            raise HTTPException(status_code=404, detail="State data not found")

        # Prepare updates
        updates = {}
        for field, value in update_data.updates.items():
            if field == "State":
                try:
                    value = States(value).value
                except ValueError:
                    raise HTTPException(status_code=400, detail=f"Invalid State value: {value}")
            updates[field] = value

        # Update document
        result = await db.states_collection.update_one(
            {"_id": str(state_id)},
            {"$set": updates}
        )

        if result.modified_count > 0:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "State data updated successfully.",
                    "updated_fields": updates
                }
            )
        else:
            raise HTTPException(status_code=400, detail="No changes made")


    except ValueError:
            raise HTTPException(
                status_code=400, detail=f"Invalid value type for field {field}"
            )


@router.delete("/delete_state_data/{state_id}")
async def delete_state_data(
    state_id: str = Path(...),
    db = Depends(get_db),
):
    try:
        result = await db.states_collection.delete_one({"_id": ObjectId(state_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="State data not found")

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "State data deleted successfully."}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting state data: {str(e)}")
