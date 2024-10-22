import asyncio
from fastapi import APIRouter, Depends, HTTPException
from db.database import get_db
from models.discipleship import DiscipleshipReport
from schemas.discipleship import DiscipleshipReportCreate, DiscipleshipReportUpdate
from typing import List
from fastapi.responses import JSONResponse
from fastapi import (
    UploadFile,
    File,
    status,
)
import os
from pathlib import Path as FilePath
import uuid
import pandas as pd
from models.states import States
from bson import ObjectId

discipleship_router = router = APIRouter(tags=["Discipleship Report"])


UPLOAD_DIRECTORY = "./discipleshipuploads"

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
                "Attendance": int(record["Attendance"]),  # This should not be null
                "SD_Cards": (
                    int(record["S.D Cards"]) if pd.notna(record["S.D Cards"]) else None
                ),
                "Manuals_Given": (
                    int(record["Manuals Given"])
                    if pd.notna(record["Manuals Given"])
                    else None
                ),
                "Bibles_Given": (
                    int(record["Bibles Given"])
                    if pd.notna(record["Bibles Given"])
                    else None
                ),
                "Month": record["Month"].upper(),
            }

            # Update existing record or insert new one
            await db.discipleship_collection.update_one(
                {
                    "Team": record["Team"],
                    "State": state or record["State"],
                    "Ward": record["Ward"],
                    "Village": record["Village"],
                    "Month": record["Month"].upper(),
                },
                {"$set": record_data},
                upsert=True,
            )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error inserting data: {str(e)}")


@router.post("/discipleship-upload")
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
@router.post(
    "/discipleship-report/", status_code=201, response_model=DiscipleshipReport
)
async def create_discipleship_report(
    report: DiscipleshipReportCreate, db=Depends(get_db)
):
    try:
        report_dict = report.model_dump()
        await db.discipleship_collection.insert_one(report_dict)
        return DiscipleshipReport(**report_dict)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/discipleship-reports/", response_model=List[DiscipleshipReport])
async def get_all_discipleship_reports(
    skip: int = 0, limit: int = 100, db=Depends(get_db)
):
    try:
        cursor = db.discipleship_collection.find().skip(skip).limit(limit)
        reports = await cursor.to_list(length=limit)
        return [DiscipleshipReport(**report) for report in reports]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/discipleship-report/{report_id}", response_model=DiscipleshipReport)
async def get_discipleship_report(report_id: str, db=Depends(get_db)):
    try:
        report = await db.discipleship_collection.find_one({"_id": ObjectId(report_id)})
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return report
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/discipleship-report/month/{month}", response_model=List[DiscipleshipReport]
)
async def get_discipleship_reports_by_month(month: str, db=Depends(get_db)):
    try:
        cursor = db.discipleship_collection.find({"Month": month.upper()})
        reports = await cursor.to_list(length=None)
        if not reports:
            raise HTTPException(
                status_code=404, detail=f"No reports found for month: {month}"
            )
        return [DiscipleshipReport(**report) for report in reports]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/discipleship-report/{report_id}", response_model=DiscipleshipReport)
async def update_discipleship_report(
    report_id: str,
    report_update: DiscipleshipReportUpdate,
    db=Depends(get_db),
):
    try:
        update_data = {k: v for k, v in report_update.dict(exclude_unset=True).items()}

        result = await db.discipleship_collection.update_one(
            {"_id": ObjectId(report_id)}, {"$set": update_data}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Report not found")

        updated_report = await db.discipleship_collection.find_one(
            {"_id": ObjectId(report_id)}
        )
        return DiscipleshipReport(**updated_report)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/discipleship-report/{report_id}", response_model=dict)
async def delete_discipleship_report(report_id: str, db=Depends(get_db)):
    try:
        result = await db.discipleship_collection.delete_one(
            {"_id": ObjectId(report_id)}
        )
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Report not found")

        return {"message": "Report deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
