import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from models import SessionLocal, Pet
from ai_service import call_inference

router = APIRouter()

# Dependency to provide a DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------------------------
# Pydantic schemas – keep them simple and instantiable
# ---------------------------------------------------------------------------
class SymptomItem(BaseModel):
    symptom: str
    severity: float
    date: str

class AnalyzeRequest(BaseModel):
    pet_id: str
    symptoms: List[SymptomItem]

class AnalysisResult(BaseModel):
    condition: str
    confidence: float
    recommendation: str

class AnalyzeResponse(BaseModel):
    analysis: List[AnalysisResult]

class RecommendRequest(BaseModel):
    pet_id: str
    symptoms: List[SymptomItem]

class RecommendationItem(BaseModel):
    type: str
    details: str

class RecommendResponse(BaseModel):
    recommendations: List[RecommendationItem]

class PetResponse(BaseModel):
    pet_id: int = Field(..., alias="id")
    name: str
    species: str
    breed: str | None = None
    age: int | None = None
    weight: float | None = None

    class Config:
        allow_population_by_field_name = True

# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------
@router.get("/pets/{pet_id}", response_model=PetResponse)
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    return pet

@router.post("/ai/analyze", response_model=AnalyzeResponse)
async def ai_analyze(request: AnalyzeRequest):
    # Build a prompt for the LLM – keep it concise for demo purposes
    user_content = json.dumps([s.dict() for s in request.symptoms])
    messages = [
        {"role": "system", "content": "You are a veterinary AI assistant. Analyze the provided symptom list and return a JSON array named 'analysis' where each element contains 'condition' (string), 'confidence' (0‑1 float), and 'recommendation' (string)."},
        {"role": "user", "content": user_content},
    ]
    raw_result = await call_inference(messages)
    # The inference helper already extracts JSON; we trust its structure but guard anyway
    if isinstance(raw_result, dict) and "analysis" in raw_result:
        return JSONResponse(content=raw_result)
    # Fallback – ensure the response matches the schema
    fallback = {"analysis": []}
    return JSONResponse(content=fallback)

@router.post("/ai/recommend", response_model=RecommendResponse)
async def ai_recommend(request: RecommendRequest):
    user_content = json.dumps([s.dict() for s in request.symptoms])
    messages = [
        {"role": "system", "content": "You are a veterinary AI assistant. Based on the symptom list, generate a JSON array named 'recommendations' where each element has 'type' (e.g., 'diet', 'exercise', 'vet_visit') and 'details' (string) providing actionable advice."},
        {"role": "user", "content": user_content},
    ]
    raw_result = await call_inference(messages)
    if isinstance(raw_result, dict) and "recommendations" in raw_result:
        return JSONResponse(content=raw_result)
    fallback = {"recommendations": []}
    return JSONResponse(content=fallback)
