from pathlib import Path

from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File,
)

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from app.agents.orchestrator import run_agent_pipeline
from app.services.evaluation_service import evaluate_pipeline
from app.services.document_service import (
    process_uploaded_document,
)


# ==================================================
# FASTAPI APPLICATION
# ==================================================

app = FastAPI(
    title="Agentic RAG API",
    description="Multi-agent Retrieval Augmented Generation system",
    version="1.0.0",
)


# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# REQUEST MODELS
# ==================================================

class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    query: str
    plan: list[str]
    answer: str | None
    confidence: float
    citations: list[dict]
    evaluation: dict
    verification: dict


class UploadResponse(BaseModel):
    filename: str
    documents_loaded: int
    chunks_created: int
    total_documents: int
    status: str


# ==================================================
# ROOT ENDPOINT
# ==================================================

@app.get("/")
def root():
    return {
        "message": "Agentic RAG API is running",
        "status": "success",
    }


# ==================================================
# QUERY ENDPOINT
# ==================================================

@app.post(
    "/query",
    response_model=QueryResponse
)
def query_agent(request: QueryRequest):

    # ----------------------------------------------
    # Validate query
    # ----------------------------------------------

    if not request.query.strip():

        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty."
        )

    try:

        # ------------------------------------------
        # Run Agentic RAG pipeline
        # ------------------------------------------

        state = run_agent_pipeline(
            request.query
        )

        # ------------------------------------------
        # Evaluate pipeline
        # ------------------------------------------

        evaluation = evaluate_pipeline(
            retrieved_documents=state.get(
                "retrieved_documents",
                []
            ),
            answer=state.get(
                "answer",
                ""
            ),
            confidence=state.get(
                "confidence",
                0.0
            ),
        )

        # ------------------------------------------
        # Return response
        # ------------------------------------------

        return QueryResponse(
            query=state.get(
                "query",
                request.query
            ),
            plan=state.get(
                "plan",
                []
            ),
            answer=state.get(
                "answer",
                ""
            ),
            confidence=float(
                state.get(
                    "confidence",
                    0.0
                )
            ),
            citations=state.get(
                "citations",
                []
            ),
            evaluation=evaluation,
            verification=state.get(
                "verification",
                {}
            ),
        )

    except Exception as error:

        print(
            f"Query processing error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ==================================================
# DOCUMENT UPLOAD ENDPOINT
# ==================================================

@app.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_document(
    file: UploadFile = File(...)
):

    allowed_extensions = {
        ".pdf",
        ".txt",
    }

    # ----------------------------------------------
    # Validate file extension
    # ----------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Only PDF and TXT files are allowed."
            )
        )

    # ----------------------------------------------
    # Create documents folder
    # ----------------------------------------------

    documents_folder = Path(
        "data/documents"
    )

    documents_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    # ----------------------------------------------
    # Save uploaded file
    # ----------------------------------------------

    file_path = documents_folder / file.filename

    try:

        contents = await file.read()

        with open(
            file_path,
            "wb"
        ) as output_file:

            output_file.write(
                contents
            )

        # ------------------------------------------
        # Process document
        # ------------------------------------------

        result = process_uploaded_document(
            str(file_path)
        )

        # ------------------------------------------
        # Return upload result
        # ------------------------------------------

        return UploadResponse(
            filename=result["filename"],
            documents_loaded=result[
                "documents_loaded"
            ],
            chunks_created=result[
                "chunks_created"
            ],
            total_documents=result[
                "total_documents"
            ],
            status=result["status"],
        )

    except Exception as error:

        print(
            f"Upload processing error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )