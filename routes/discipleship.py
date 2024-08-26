import asyncio
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db.database import get_db
from models.discipleship import DiscipleshipReport
from schemas.discipleship import DiscipleshipReportCreate, DiscipleshipReportUpdate
from typing import List
from uuid import UUID
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


def process_file(df: pd.DataFrame, db: Session) -> None:
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
            existing_record = (
                db.query(DiscipleshipReport)
                .filter_by(
                    Team=record["Team"],
                    State=state or record["State"],
                    LGA=record["LGA"],
                    Ward=record["Ward"],
                    Village=record["Village"],
                )
                .first()
            )

            record_data = {
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
                "Month": record["Month"],
            }

            if existing_record:
                for key, value in record_data.items():
                    setattr(existing_record, key, value)
            else:
                discipleship_data = DiscipleshipReport(
                    Team=record["Team"],
                    State=record["State"],
                    LGA=record["LGA"],
                    Ward=record["Ward"],
                    Village=record["Village"],
                    **record_data,
                )
                db.add(discipleship_data)

        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error inserting data: {str(e)}")


@router.post("/discipleship-upload")
async def upload_files(
    files: List[UploadFile] = File(...), db: Session = Depends(get_db)
):

    try:
        for file in files:
            file_path = await save_file(file)
            try:
                df = await read_excel_file(file_path)
                process_file(df, db)
            finally:
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
def create_discipleship_report(
    report: DiscipleshipReportCreate, db: Session = Depends(get_db)
):
    try:
        db_report = DiscipleshipReport(**report.dict())
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        return db_report
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/discipleship-reports/", response_model=List[DiscipleshipReport])
def get_all_discipleship_reports(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    try:

        reports = db.exec(select(DiscipleshipReport).offset(skip).limit(limit)).all()
        return reports
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/discipleship-report/{report_id}", response_model=DiscipleshipReport)
def get_discipleship_report(report_id: UUID, db: Session = Depends(get_db)):
    try:

        report = db.get(DiscipleshipReport, report_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return report
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/discipleship-report/month/{month}", response_model=List[DiscipleshipReport]
)
def get_discipleship_reports_by_month(month: str, db: Session = Depends(get_db)):
    try:
        reports = db.exec(
            select(DiscipleshipReport).where(DiscipleshipReport.Month == month.upper())
        ).all()
        if not reports:
            raise HTTPException(
                status_code=404, detail=f"No reports found for month: {month}"
            )
        return reports
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/discipleship-report/{report_id}", response_model=DiscipleshipReport)
def update_discipleship_report(
    report_id: UUID,
    report_update: DiscipleshipReportUpdate,
    db: Session = Depends(get_db),
):
    try:
        db_report = db.get(DiscipleshipReport, report_id)
        if not db_report:
            raise HTTPException(status_code=404, detail="Report not found")

        report_data = report_update.dict(exclude_unset=True)
        for key, value in report_data.items():
            setattr(db_report, key, value)

        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        return db_report
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/discipleship-report/{report_id}", response_model=dict)
def delete_discipleship_report(report_id: UUID, db: Session = Depends(get_db)):
    try:
        db_report = db.get(DiscipleshipReport, report_id)
        if not db_report:
            raise HTTPException(status_code=404, detail="Report not found")

        db.delete(db_report)
        db.commit()
        return {"message": "Report deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
