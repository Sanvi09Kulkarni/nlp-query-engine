from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from .schema_discovery import SchemaDiscovery
from .document_processor import DocumentProcessor
from .query_engine import QueryEngine
from pydantic import BaseModel

app = FastAPI(title="NLP Query Engine - MVP")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

schema = {}
engine = None
doc_processor = DocumentProcessor()  # initialized once

class QueryBody(BaseModel):
    query: str

@app.post("/api/connect-database")
async def connect_database(connection_string: str = Form(...)):
    global schema, engine
    sd = SchemaDiscovery()
    schema, engine = sd.analyze_database(connection_string)
    return {"schema": schema}

@app.get("/api/schema")
async def get_schema():
    return {"schema": schema}

@app.post("/api/upload-documents")
async def upload_documents(files: list[UploadFile] = File(...)):
    doc_processor.process_files(files)
    return {"status": "ok", "count": len(doc_processor.docs)}

@app.post("/api/query")
async def process_query(body: QueryBody):
    if engine is None:
        return {"error": "No database connected. Call /api/connect-database first."}
    qe = QueryEngine(schema, engine, doc_processor)
    return qe.process_query(body.query)
