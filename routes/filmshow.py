# from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from db.database import get_db
from models.filmshow import FilmShowReport
from schemas.filmshow import FilmShowReportCreate, FilmShowReportUpdate
from typing import List
from fastapi import (
    UploadFile,
    File,
    status,
)
from bson import ObjectId
import os
from pathlib import Path as FilePath
import uuid
import pandas as pd
import asyncio
from models.states import States


filmshow_router = router = APIRouter(tags=["Film Show Report"])


UPLOAD_DIRECTORY = "./filmshowuploads"

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
    try:
        for _, record in df.iterrows():
            # Handle different variations of FCT
            state = record["State"].strip().title()
            if state in ["Federal Capital Territory", "FCT", "Abuja"]:
                state = States.FCT
            else:
                try:
                    state = States(state)
                except ValueError:
                    raise ValueError(f"Invalid state: {state}")

            date_str = record["Date"]

            # Convert date object to string
            if isinstance(date_str, pd.Timestamp):
                date_str = date_str.strftime("%Y-%m-%d").replace("-", "/")
                print("hello world")
            else:
                date_str = str(date_str).split(" ")[0].replace("-", "/")

            record_data = {
                "Team": record["Team"],
                "State": state or record["State"],
                "LGA": str(record["LGA"]) if pd.notna(record["LGA"]) else None,
                "Ward": record["Ward"],
                "Village": record["Village"],
                "Population": (
                    int(record["Population"])
                    if pd.notna(record["Population"])
                    else None
                ),
                "UPG": record["UPG"] if pd.notna(record["UPG"]) else None,
                "Attendance": int(record["Attendance"]),
                "SD_Cards": (
                    int(record["S.D Cards"]) if pd.notna(record["S.D Cards"]) else None
                ),
                "Audio_Bibles": (
                    int(record["Audio Bibles"])
                    if pd.notna(record["Audio Bibles"])
                    else None
                ),
                "People_Saved": (
                    int(record["People Saved"])
                    if pd.notna(record["People Saved"])
                    else None
                ),
                "Date": date_str,
                "Month": record["Month"].upper(),
            }

            # Update existing record or insert new one
            await db.filmshow_collection.update_one(
                {
                    "Team": record["Team"],
                    "State": state or record["State"],
                    "Ward": record["Ward"],
                    "Village": record["Village"],
                    "Date": date_str,
                },
                {"$set": record_data},
                upsert=True,
            )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error inserting data: {str(e)}")


@router.post("/filmshow-upload")
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


# API for posting data manually
@router.post("/film-show-report/", status_code=201, response_model=FilmShowReport)
async def create_film_show_report(report: FilmShowReportCreate, db=Depends(get_db)):
    """Create a new film show report manually."""
    try:
        report_dict = report.model_dump()
        # report_dict["_id"] = str(ObjectId())
        await db.filmshow_collection.insert_one(report_dict)
        return FilmShowReport(**report_dict)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/film-show-reports/", response_model=List[FilmShowReport])
async def get_all_film_show_reports(
    skip: int = 0, limit: int = 100, db=Depends(get_db)
):
    """Fetch all film show reports."""
    try:
        cursor = db.filmshow_collection.find().skip(skip).limit(limit)
        reports = await cursor.to_list(length=limit)
        return [FilmShowReport(**report) for report in reports]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# API for fetching all data in a particular month
@router.get("/film-show-reports/{month}", response_model=List[FilmShowReport])
async def get_film_show_reports_by_month(month: str, db=Depends(get_db)):
    """Fetch all film show reports for a particular month."""
    month = month.upper()
    try:
        cursor = db.filmshows.find({"Month": month})
        reports = await cursor.to_list(length=None)
        if not reports:
            raise HTTPException(
                status_code=404, detail=f"No reports found for month: {month}"
            )
        return [FilmShowReport(**report) for report in reports]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Retrieves data by ID
@router.get("/film-show-report/{report_id}", response_model=FilmShowReport)
async def get_film_show_report(report_id: str, db=Depends(get_db)):
    """Fetch a film show report by ID."""
    try:
        report = await db.filmshow_collection.find_one({"_id": ObjectId(report_id)})
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return FilmShowReport(**report)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# API for updating/editing one or more fields by ID
@router.put("/film-show-report/{report_id}", response_model=FilmShowReport)
async def update_film_show_report(
    report_id: str, report_update: FilmShowReportUpdate, db=Depends(get_db)
):
    """Update a film show report."""
    try:
        update_data = {k: v for k, v in report_update.dict(exclude_unset=True).items()}

        result = await db.filmshow_collection.update_one(
            {"_id": ObjectId(report_id)}, {"$set": update_data}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Report not found")

        updated_report = await db.filmshow_collection.find_one(
            {"_id": ObjectId(report_id)}
        )
        return FilmShowReport(**updated_report)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# API for deleting data
@router.delete("/film-show-report/{report_id}", response_model=dict)
async def delete_film_show_report(report_id: str, db=Depends(get_db)):
    """Delete a film show report."""
    try:
        result = await db.filmshow_collection.delete_one({"_id": ObjectId(report_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Report not found")
            
        return {"message": "Report deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# API for deleting data by month
@router.delete("/film-show-reports/{month}", response_model=dict)
async def delete_film_show_reports_by_month(month: str, db=Depends(get_db)):
    """Delete all film show reports for a particular month."""
    try:
        # Convert month to uppercase for consistency
        month = month.upper()
        count = await db.filmshow_collection.count_documents({"Month": month})
        
        if count == 0:
            raise HTTPException(status_code=404, detail=f"No reports found for month: {month}")
        
        result = await db.filmshow_collection.delete_many({"Month": month})
        
        return {
            "message": f"All reports for month {month} deleted successfully",
            "count": result.deleted_count
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
