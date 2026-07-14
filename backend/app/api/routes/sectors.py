from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.sector import SectorResponse
from app.services.sector_service import get_all_sectors

router = APIRouter(
    prefix="/sectors",
    tags=["Sectors"],
)


@router.get("/", response_model=list[SectorResponse])
def read_sectors(db: Session = Depends(get_db)):
    return get_all_sectors(db)