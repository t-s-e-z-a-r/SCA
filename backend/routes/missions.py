from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Mission, Target, Cat
from ..schemas import (
    MissionCreate, MissionUpdate, MissionResponse, MissionListResponse,
    TargetUpdate, TargetResponse
)

router = APIRouter(prefix="/missions", tags=["missions"])


@router.post("/", response_model=MissionResponse, status_code=status.HTTP_201_CREATED)
def create_mission(mission: MissionCreate, db: Session = Depends(get_db)):
    if mission.cat_id:
        cat = db.query(Cat).filter(Cat.id == mission.cat_id).first()
        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cat with id {mission.cat_id} not found"
            )
        active_mission = db.query(Mission).filter(
            Mission.cat_id == mission.cat_id,
            Mission.is_complete == False
        ).first()
        if active_mission:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cat with id {mission.cat_id} already has an active mission"
            )
    
    db_mission = Mission(cat_id=mission.cat_id, is_complete=False)
    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)
    
    for target_data in mission.targets:
        db_target = Target(
            mission_id=db_mission.id,
            name=target_data.name,
            country=target_data.country,
            notes=target_data.notes,
            is_complete=False
        )
        db.add(db_target)
    
    db.commit()
    db.refresh(db_mission)
    return db_mission


@router.get("/", response_model=List[MissionListResponse])
def list_missions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    missions = db.query(Mission).offset(skip).limit(limit).all()
    return missions


@router.get("/{mission_id}", response_model=MissionResponse)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with id {mission_id} not found"
        )
    return mission


@router.patch("/{mission_id}", response_model=MissionResponse)
def update_mission(mission_id: int, mission_update: MissionUpdate, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with id {mission_id} not found"
        )
    
    if mission_update.cat_id is not None:
        cat = db.query(Cat).filter(Cat.id == mission_update.cat_id).first()
        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cat with id {mission_update.cat_id} not found"
            )
        active_mission = db.query(Mission).filter(
            Mission.cat_id == mission_update.cat_id,
            Mission.is_complete == False,
            Mission.id != mission_id
        ).first()
        if active_mission:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cat with id {mission_update.cat_id} already has an active mission"
            )
        mission.cat_id = mission_update.cat_id
    
    db.commit()
    db.refresh(mission)
    return mission


@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with id {mission_id} not found"
        )
    
    if mission.cat_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete mission with id {mission_id} because it is assigned to a cat"
        )
    
    db.delete(mission)
    db.commit()
    return None


@router.patch("/{mission_id}/targets/{target_id}", response_model=TargetResponse)
def update_target(
    mission_id: int,
    target_id: int,
    target_update: TargetUpdate,
    db: Session = Depends(get_db)
):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with id {mission_id} not found"
        )
    
    target = db.query(Target).filter(
        Target.id == target_id,
        Target.mission_id == mission_id
    ).first()
    
    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Target with id {target_id} not found in mission {mission_id}"
        )
    
    if target_update.notes is not None:
        if target.is_complete or mission.is_complete:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot update notes for a completed target or mission"
            )
        target.notes = target_update.notes
    
    if target_update.is_complete is not None:
        target.is_complete = target_update.is_complete
        
        all_targets = db.query(Target).filter(Target.mission_id == mission_id).all()
        if all(t.is_complete for t in all_targets):
            mission.is_complete = True
    
    db.commit()
    db.refresh(target)
    return target
