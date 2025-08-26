from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import asyncpg
import os
import time
import re

app = FastAPI()

# -----------------------
# Database Setup
# -----------------------
DATABASE_URL = "postgresql://postgres:password@localhost:5432/mydb"

async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)

# -----------------------
# Example Agent Functions
# -----------------------

async def agent1_preprocess(text: str):
    """Preprocess: lowercase, remove punctuation, split tokens."""
    processed = re.sub(r"[^a-zA-Z0-9\s]", "", text).lower().split()
    return processed, f"Preprocessing completed → {len(processed)} tokens"

async def agent2_inference(tokens: list[str]):
    """Inference: simple word frequency count."""
    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    return freq, f"Inference completed → {len(freq)} unique words"

async def agent3_postprocess(freq: dict):
    """Postprocess: extract top 5 words."""
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    top_words = sorted_words[:5]
    return top_words, f"Postprocessing completed → top {len(top_words)} words extracted"

async def agent4_fetch_from_db():
    """Fetch some data from Postgres."""
    conn = await get_db_connection()
    try:
        rows = await conn.fetch("SELECT id, name FROM users LIMIT 3;")
        data = [{"id": r["id"], "name": r["name"]} for r in rows]
        return data, f"Database query completed → fetched {len(data)} rows"
    finally:
        await conn.close()

async def generate_file(results: list[tuple[str, int]], db_data: list[dict]):
    """Generate final result file."""
    output_dir = "files"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"output_{int(time.time())}.txt")

    with open(file_path, "w") as f:
        f.write("Top extracted keywords:\n")
        for word, count in results:
            f.write(f"{word}: {count}\n")

        f.write("\nSample DB rows:\n")
        for row in db_data:
            f.write(f"{row['id']}: {row['name']}\n")

    return file_path

# -----------------------
# Streaming Logic
# -----------------------

async def run_pipeline():
    text_input = "FastAPI is an amazing framework! FastAPI makes APIs super fast, easy, and fun to build."

    # Step 1: Preprocessing
    yield f"data: Agent 1 started (Preprocessing)\n\n"
    tokens, log1 = await agent1_preprocess(text_input)
    yield f"data: {log1}\n\n"

    # Step 2: Inference
    yield f"data: Agent 2 started (Inference)\n\n"
    freq, log2 = await agent2_inference(tokens)
    yield f"data: {log2}\n\n"

    # Step 3: Postprocessing
    yield f"data: Agent 3 started (Postprocessing)\n\n"
    top_words, log3 = await agent3_postprocess(freq)
    yield f"data: {log3}\n\n"

    # Step 4: Database Query
    yield f"data: Agent 4 started (Database Fetch)\n\n"
    db_data, log4 = await agent4_fetch_from_db()
    yield f"data: {log4}\n\n"

    # Step 5: File Generation
    yield f"data: Generating final file...\n\n"
    file_path = await generate_file(top_words, db_data)

    file_url = f"http://localhost:8000/{file_path}"
    yield f"data: {{\"file_url\": \"{file_url}\"}}\n\n"


@app.get("/progress")
async def progress():
    return StreamingResponse(run_pipeline(), media_type="text/event-stream")

# Serve files so UI can download
app.mount("/files", StaticFiles(directory="files"), name="files")
