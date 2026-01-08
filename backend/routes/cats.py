from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Cat, Mission
from ..schemas import CatCreate, CatUpdate, CatResponse
from ..services import validate_breed

router = APIRouter(prefix="/cats", tags=["cats"])


@router.post("/", response_model=CatResponse, status_code=status.HTTP_201_CREATED)
async def create_cat(cat: CatCreate, db: Session = Depends(get_db)):
    is_valid_breed = await validate_breed(cat.breed)
    if not is_valid_breed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid breed: {cat.breed}. Please provide a valid cat breed."
        )
    
    db_cat = Cat(**cat.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


@router.get("/", response_model=List[CatResponse])
def list_cats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cats = db.query(Cat).offset(skip).limit(limit).all()
    return cats


@router.get("/{cat_id}", response_model=CatResponse)
def get_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(Cat).filter(Cat.id == cat_id).first()
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found"
        )
    return cat


@router.patch("/{cat_id}", response_model=CatResponse)
def update_cat(cat_id: int, cat_update: CatUpdate, db: Session = Depends(get_db)):
    cat = db.query(Cat).filter(Cat.id == cat_id).first()
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found"
        )
    
    cat.salary = cat_update.salary
    db.commit()
    db.refresh(cat)
    return cat


@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(Cat).filter(Cat.id == cat_id).first()
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found"
        )
    
    active_mission = db.query(Mission).filter(
        Mission.cat_id == cat_id,
        Mission.is_complete == False
    ).first()
    if active_mission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete cat with id {cat_id} because it has an active mission"
        )
    
    db.delete(cat)
    db.commit()
    return None
