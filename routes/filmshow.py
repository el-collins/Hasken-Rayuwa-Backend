from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, select, delete
from db.database import get_db
from models.filmshow import FilmShowReport
from schemas.filmshow import FilmShowReportCreate, FilmShowReportUpdate
from typing import List
from uuid import UUID
from fastapi import (
    UploadFile,
    File,
    status,
)
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
    # Delete the file after processing
    os.remove(file_path)



async def read_excel_file(file_path: FilePath) -> pd.DataFrame:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, pd.read_excel, file_path)


def process_file(df: pd.DataFrame, db: Session) -> None:
    try:
        for _, record in df.iterrows():
            date_str = record["Date"]
            # # if the date is in the wrong format, try to convert it else return it like that
            try:
                date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
            except Exception:
                # If the above fails, try another common format
                # date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                continue


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
                db.query(FilmShowReport)
                .filter_by(
                    Team=record["Team"],
                    State=state or record["State"],
                    # LGA=record["LGA"],
                    Ward=record["Ward"],
                    Village=record["Village"],
                    # Date=record["Date"].date(),  
                    Date=date_obj or record["Date"],
                    # Date=date_obj,

                )
                .first()
            )

            record_data = {
                "LGA": str(record["LGA"]) if pd.notna(record["LGA"]) else None,
                "Population": int(record["Population"]) if pd.notna(record["Population"]) else None,
                "UPG": record["UPG"] if pd.notna(record["UPG"]) else None,
                "Attendance": int(record["Attendance"]),  # This should not be null
                "SD_Cards": int(record["S.D Cards"]) if pd.notna(record["S.D Cards"]) else None,
                "Audio_Bibles": int(record["Audio Bibles"]) if pd.notna(record["Audio Bibles"]) else None,
                "People_Saved": int(record["People Saved"]) if pd.notna(record["People Saved"]) else None,
                # "Date": record["Date"].date(),
                "Date": date_obj or record["Date"],
                "Month": record["Month"],
            }

            if existing_record:
                for key, value in record_data.items():
                    setattr(existing_record, key, value)
            else:
                filmshow_data = FilmShowReport(
                    Team=record["Team"],
                    State=state or record["State"],
                    # LGA=record["LGA"],
                    Ward=record["Ward"],
                    Village=record["Village"],
                    **record_data,
                )
                db.add(filmshow_data)

        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error inserting data: {str(e)}")



@router.post("/filmshow-upload")
async def upload_files(
    files: List[UploadFile] = File(...), db: Session = Depends(get_db)
):

    try:
        for file in files:
            file_path = await save_file(file)
            df = await read_excel_file(file_path)
            process_file(df, db)
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
def create_film_show_report(
    report: FilmShowReportCreate, db: Session = Depends(get_db)
):
    """Create a new film show report manually."""
    try:
        db_report = FilmShowReport(**report.dict())
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        return db_report
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




@router.get("/film-show-reports/", response_model=List[FilmShowReport])
def get_all_film_show_reports(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    try:

        reports = db.exec(select(FilmShowReport).offset(skip).limit(limit)).all()
        return reports
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



# API for fetching all data in a particular month
@router.get("/film-show-reports/{month}", response_model=List[FilmShowReport])
def get_film_show_reports_by_month(month: str, db: Session = Depends(get_db)):
    month = month.upper()
    try:
        reports = db.exec(
            select(FilmShowReport).where(FilmShowReport.Month == month.upper())
        ).all()
        if not reports:
            raise HTTPException(
                status_code=404, detail=f"No reports found for month: {month}"
            )
        return reports
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# API for updating/editing one or more fields by ID
@router.put("/film-show-report/{report_id}", response_model=FilmShowReport)
def update_film_show_report(
    report_id: UUID, report_update: FilmShowReportUpdate, db: Session = Depends(get_db)
):
    try:
        db_report = db.get(FilmShowReport, report_id)
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

# API for deleting data
@router.delete("/film-show-report/{report_id}", response_model=dict)
def delete_film_show_report(report_id: UUID, db: Session = Depends(get_db)):
    try:
        db_report = db.get(FilmShowReport, report_id)
        if not db_report:
            raise HTTPException(status_code=404, detail="Report not found")

        db.delete(db_report)
        db.commit()
        return {"message": "Report deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# API for deleting data by month
@router.delete("/film-show-reports/{month}", response_model=dict)
def delete_film_show_reports_by_month(month: str, db: Session = Depends(get_db)):
    try:
        # Convert month to uppercase for consistency
        month = month.upper()

        # Select all reports for the given month
        statement = select(FilmShowReport).where(FilmShowReport.Month == month)
        reports = db.exec(statement).all()

        if not reports:
            raise HTTPException(status_code=404, detail=f"No reports found for month: {month}")

        # Delete all reports for the given month
        delete_statement = delete(FilmShowReport).where(FilmShowReport.Month == month) # type: ignore
        db.exec(delete_statement) # type: ignore
        db.commit()

        return {"message": f"All reports for month {month} deleted successfully", "count": len(reports)}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
