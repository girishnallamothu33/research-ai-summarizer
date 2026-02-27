from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import SummarizeRequest, SummarizeResponse, CrossDomainRequest, ClusterRequest, ClusterResponse, HistoryResponse
from app import models
from app.services import pdf_service, ai_service, clustering_service

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    contents = await file.read()
    try:
        text = pdf_service.extract_text_from_pdf(contents)
        return {"filename": file.filename, "extracted_text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

@router.post("/summarize", response_model=SummarizeResponse)
def summarize_text(request: SummarizeRequest, db: Session = Depends(get_db)):
    try:
        result = ai_service.generate_summary(request.text, request.discipline)
        
        # Save to db
        db_record = models.SummaryHistory(
            filename="user_input_or_pypdf",
            discipline=request.discipline,
            extracted_text=request.text[:1000], # store snippet
            short_summary=result.get("short_summary", ""),
            detailed_summary=result.get("detailed_summary", ""),
            keywords=result.get("keywords", []),
            key_insights=result.get("key_insights", []),
            discipline_interpretation=result.get("discipline_interpretation", "")
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cross-domain")
def cross_domain(request: CrossDomainRequest):
    return ai_service.get_cross_domain_ideas(request.text)

@router.post("/cluster", response_model=ClusterResponse)
def cluster_texts(request: ClusterRequest):
    try:
        clusters = clustering_service.group_texts(request.texts)
        return {"clusters": clusters}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=list[HistoryResponse])
def get_history(db: Session = Depends(get_db)):
    records = db.query(models.SummaryHistory).order_by(models.SummaryHistory.created_at.desc()).limit(10).all()
    return records

@router.get("/topics")
def get_topics():
    # Mock topics graph
    return {
        "nodes": [{"id": "Neural Networks", "group": 1}, {"id": "Biomedicine", "group": 2}],
        "links": [{"source": "Neural Networks", "target": "Biomedicine", "value": 1}]
    }
