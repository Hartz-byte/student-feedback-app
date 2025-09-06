from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime
from .models import Feedback, FeedbackCreate
from .storage import load_store, save_store
from pathlib import Path
import os

# llama-cpp
from llama_cpp import Llama

MODEL_PATH = "../../../local_models/mistral-7b-instruct/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
llm = None

app = FastAPI(title="Student Feedback API")

# ---- Startup: load model ----
@app.on_event("startup")
def startup_event():
    global llm
    if not Path(MODEL_PATH).exists():
        raise RuntimeError(f"Model file not found at {MODEL_PATH}")
    llm = Llama(model_path=MODEL_PATH, n_ctx=2048)  # loaded once
    print("✅ Local model loaded successfully.")


# ---- CRUD ----
@app.get("/feedback", response_model=List[Feedback])
def list_feedback():
    return load_store()

@app.post("/feedback", response_model=Feedback)
def create_feedback(item: FeedbackCreate):
    store = load_store()
    new_entry = Feedback(
        id=int(datetime.utcnow().timestamp() * 1000),
        submitted_at=datetime.utcnow(),
        **item.dict()
    )
    store.append(new_entry.dict())
    save_store(store)
    return new_entry

@app.put("/feedback/{item_id}", response_model=Feedback)
def update_feedback(item_id: int, item: FeedbackCreate):
    store = load_store()
    for idx, entry in enumerate(store):
        if entry["id"] == item_id:
            updated = Feedback(id=item_id, submitted_at=datetime.utcnow(), **item.dict())
            store[idx] = updated.dict()
            save_store(store)
            return updated
    raise HTTPException(status_code=404, detail="Feedback not found")

@app.delete("/feedback/{item_id}")
def delete_feedback(item_id: int):
    store = load_store()
    for idx, entry in enumerate(store):
        if entry["id"] == item_id:
            del store[idx]
            save_store(store)
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Feedback not found")


# ---- Summarize ----
@app.get("/summarize/{item_id}")
def summarize_feedback(item_id: int):
    store = load_store()
    entry = next((e for e in store if e["id"] == item_id), None)
    if not entry:
        raise HTTPException(status_code=404, detail="Feedback not found")

    # Construct prompt
    prompt = f"""Summarize the following student feedback in 2-3 sentences:

Name: {entry['name']}
Course: {entry['course']}
Rating: {entry['rating']}
Comments: {entry['comments']}
Tags: {', '.join(entry['tags']) if entry['tags'] else 'N/A'}

Summary:
"""
    output = llm.create(prompt=prompt, max_tokens=200, temperature=0.2)
    summary = output["choices"][0]["text"].strip()
    return {"summary": summary}
