import os
import uuid
import asyncio
import pandas as pd
from typing import List
from pathlib import Path
from sqlalchemy import func
from sqlmodel import Session, select
from schemas.states import StateDataInput
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from core.auth import authenticate_user, logout_user
from db.database import get_db, get_or_create_entity
from models.states import StateData, States, ReligionType
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Request, Form, status, Body, Query

states_router = router = APIRouter(tags=["States"])

UPLOAD_DIRECTORY = "./uploads"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

async def save_file(file: UploadFile) -> Path:
    file_path = Path(UPLOAD_DIRECTORY) / f"{uuid.uuid4()}.xlsx"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    return file_path

async def read_excel_file(file_path: Path) -> pd.DataFrame:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, 
        pd.read_excel, 
        file_path
    )

def process_file(
    df: pd.DataFrame, 
    db: Session) -> None:
    
    data_to_insert = df.to_dict(orient='records')
    
    try:
        for record in data_to_insert:
            state = record["State"].capitalize()
            village = record["Village"]

            existing_record = db.query(StateData).filter_by(
                State=state, 
                Village=village
            ).first()
            
            record_data = {
                "Lga": record["L.G.A"],
                "Ward": record["Ward"],
                "Estimated_Christian_Population": record["Esti Christians population"],
                "Estimated_Muslim_Population": record["Esti Muslims"],
                "Estimated_Traditional_Religion_Population": record["Esti Traditional People"],
                "Converts": record["Converts"],
                "Estimated_Total_Population": record["Esti population of the village"],
                "Film_Attendance": record["Film Attendance"],
                "People_Group": record["People Group"],
                "Practiced_Religion": record["Practiced Religion"]
            }

            if existing_record:
                for key, value in record_data.items():
                    setattr(existing_record, key, value)
            else:
                state_data = StateData(
                    State=state, 
                    Village=village, 
                    **record_data
                )
                
                db.add(state_data)
        
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail=f"Error inserting data: {str(e)}"
        )
    
    
@router.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...), 
    db: Session = Depends(get_db)):
    
    try:
        for file in files:
            file_path = await save_file(file)
            df = await read_excel_file(file_path)
            process_file(df, db)
            
        return JSONResponse(
            status_code=status.HTTP_200_OK, 
            content={"message": "File(s) uploaded and data saved successfully."}
        )
        
    except Exception as e:
        print(f"Error uploading files: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content={"message": str(e)}
        )

@router.post("/add_state_data")
async def manual_input(
    state_data: StateDataInput,
    db: Session = Depends(get_db),
):
    data = StateData(
        State=state_data.state,
        Lga=state_data.lga,
        Ward=state_data.ward,
        Village=state_data.village,
        Estimated_Christian_Population=state_data.estimated_christian_population,
        Estimated_Muslim_Population=state_data.estimated_muslim_population,
        Estimated_Traditional_Religion_Population=state_data.estimated_traditional_religion_population,
        Converts=state_data.converts,
        Estimated_Total_Population=state_data.estimated_total_population,
        Film_Attendance=state_data.film_attendance,
        People_Group=state_data.people_group,
        Practiced_Religion=state_data.practiced_religion,
    )
    
    try:
        db.add(data)
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK, 
            content={"message": "Data saved successfully."}
        )
        
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content={"message": str(e)}
        )
    

@router.get('/states_data')
async def states_list(
    state: str | None = Query(None),
    skip: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db)
) -> dict:
    """
    Retrieves a list of State from the database based on the specified criteria.

    Returns:
        dict: A dictionary containing the list of State objects and their aggregate data.
    """
    try:
        query = db.query(StateData)
        data = []

        if state:
            state_data = query.filter(StateData.State == state).all()
            if not state_data:
                raise HTTPException(status_code=404, detail="State not found")
        else:
            state_data = query.offset(skip).limit(limit).all()

        totals = {
            'total_estimated_christian_population': db.query(func.sum(StateData.Estimated_Christian_Population)).filter(StateData.State == state).scalar(),
            'total_estimated_muslim_population': db.query(func.sum(StateData.Estimated_Muslim_Population)).filter(StateData.State == state).scalar(),
            'total_estimated_traditional_religion_population': db.query(func.sum(StateData.Estimated_Traditional_Religion_Population)).filter(StateData.State == state).scalar(),
            'total_converts': db.query(func.sum(StateData.Converts)).filter(StateData.State == state).scalar(),
            'total_estimated_total_population': db.query(func.sum(StateData.Estimated_Total_Population)).filter(StateData.State == state).scalar(),
            'total_film_attendance': db.query(func.sum(StateData.Film_Attendance)).filter(StateData.State == state).scalar()
        } if state else {
            'total_estimated_christian_population': db.query(func.sum(StateData.Estimated_Christian_Population)).scalar(),
            'total_estimated_muslim_population': db.query(func.sum(StateData.Estimated_Muslim_Population)).scalar(),
            'total_estimated_traditional_religion_population': db.query(func.sum(StateData.Estimated_Traditional_Religion_Population)).scalar(),
            'total_converts': db.query(func.sum(StateData.Converts)).scalar(),
            'total_estimated_total_population': db.query(func.sum(StateData.Estimated_Total_Population)).scalar(),
            'total_film_attendance': db.query(func.sum(StateData.Film_Attendance)).scalar()
        }

        data = [{
            'State': record.State.value,
            'Lga': record.Lga,
            'Ward': record.Ward,
            'Village': record.Village,
            'Estimated_Christian_Population': record.Estimated_Christian_Population,
            'Estimated_Muslim_Population': record.Estimated_Muslim_Population,
            'Estimated_Traditional_Religion_Population': record.Estimated_Traditional_Religion_Population,
            'Converts': record.Converts,
            'Estimated_Total_Population': record.Estimated_Total_Population,
            'Film_Attendance': record.Film_Attendance,
            'People_Group': record.People_Group,
            'Practiced_Religion': record.Practiced_Religion
        } for record in state_data]

        return {
            'status': 'success', 
            'data': data, 
            'totals': totals
        }

    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=str(e)
        )