from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.EmotionDto import MakeEmotionReportRequest
from app.services.log_service import (create_usertalk_log_service, get_log_service, get_logs_by_gree_service, get_logs_service, delete_log_service, get_user_talk_contents_by_gree_id)
from app.schemas.LogDto import CreateUserTalkLogDto, LogResponseDto

router = APIRouter()

@router.post("/", response_model=LogResponseDto)
async def create_log(log_dto: CreateUserTalkLogDto, db: AsyncSession = Depends(get_db)):
    return await create_usertalk_log_service(db, log_dto)

@router.get("/{log_id}", response_model=LogResponseDto)
async def read_log(log_id: int, db: AsyncSession = Depends(get_db)):
    return await get_log_service(db, log_id)

@router.get("/", response_model=List[LogResponseDto])
async def read_logs(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await get_logs_service(db, skip, limit)

@router.delete("/{log_id}", response_model=LogResponseDto)
async def delete_log(log_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_log_service(db, log_id)

@router.get("/gree/{gree_id}", response_model=List[LogResponseDto])
async def read_logs_by_gree(gree_id: int, db: AsyncSession = Depends(get_db)):
    return await get_logs_by_gree_service(db, gree_id)

@router.get("/sentence/{gree_id}", response_model=MakeEmotionReportRequest)
async def get_user_talks_for_emotion_report(gree_id: int, db: AsyncSession = Depends(get_db)):
    sentences = await get_user_talk_contents_by_gree_id(gree_id, db)

    if not sentences:
        raise HTTPException(status_code=404, detail="Logs not found")

    return MakeEmotionReportRequest(sentences=sentences)