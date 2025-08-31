from fastapi import APIRouter, Depends, HTTPException
from typing import List

router = APIRouter()

@router.get("")
async def get_stats():
    pass
