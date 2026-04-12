from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
from knowledge_base import error_db
from memory import save_error
from datetime import datetime

app = FastAPI()

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')
db_embeddings = [
    model.encode(entry["error"], convert_to_tensor=True)
    for entry in error_db
]
# Precompute embeddings (IMPORTANT)
db_embeddings = [
    model.encode(entry["error"], convert_to_tensor=True)
    for entry in error_db
]

class DebugInput(BaseModel):
    error: str
    code: str = ""

@app.get("/")
def home():
    return {"message": "AI Debug Assistant is running"}

# Rule-based analysis
def analyze_error_locally(error, code):
    error = error.lower()

    if "typeerror" in error:
        return "Type mismatch. You may be trying to combine incompatible data types."
    elif "syntaxerror" in error:
        return "Syntax issue. Check brackets or indentation."
    elif "nameerror" in error:
        return "Variable not defined."
    elif "indexerror" in error:
        return "Index out of range."
    else:
        return "General error. Check logic."

# Similarity search
def find_similar_error(user_error):
    user_embedding = model.encode(user_error, convert_to_tensor=True)

    best_match = None
    best_score = -1

    for i, entry in enumerate(error_db):
        score = util.cos_sim(user_embedding, db_embeddings[i]).item()

        if score > best_score:
            best_score = score
            best_match = entry

    return best_match

# Main route
@app.post("/analyze")
def analyze_error(input: DebugInput):
    rule_based = analyze_error_locally(input.error, input.code)
    similar = find_similar_error(input.error)

    result = {
        "input_error": input.error,
        "analysis": {
            "rule_based": rule_based,
            "similar_error": similar["error"] if similar else None,
            "fix": similar["solution"] if similar else "No similar error found"
        },
        "timestamp": str(datetime.now())
    }

    # Save safely
    try:
        save_error(result)
    except:
        pass

    return result