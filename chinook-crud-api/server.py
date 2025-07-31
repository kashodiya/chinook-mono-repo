from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Dict, Any, Optional

app = FastAPI(title="Chinook Database API", version="1.0.0")

DB_PATH = "chinook.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_tables():
    with get_db() as conn:
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [row[0] for row in cursor.fetchall()]

def get_table_schema(table_name: str):
    with get_db() as conn:
        cursor = conn.execute(f"PRAGMA table_info({table_name})")
        return {row[1]: row[2] for row in cursor.fetchall()}

@app.get("/")
def root():
    return {"message": "Chinook Database API", "tables": get_tables()}

@app.get("/{table_name}")
def get_all_records(table_name: str, limit: int = 100, offset: int = 0):
    if table_name not in get_tables():
        raise HTTPException(status_code=404, detail="Table not found")
    
    with get_db() as conn:
        cursor = conn.execute(f"SELECT * FROM {table_name} LIMIT ? OFFSET ?", (limit, offset))
        return [dict(row) for row in cursor.fetchall()]

@app.get("/{table_name}/{record_id}")
def get_record(table_name: str, record_id: int):
    if table_name not in get_tables():
        raise HTTPException(status_code=404, detail="Table not found")
    
    schema = get_table_schema(table_name)
    pk_column = next(iter(schema.keys()))
    
    with get_db() as conn:
        cursor = conn.execute(f"SELECT * FROM {table_name} WHERE {pk_column} = ?", (record_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Record not found")
        return dict(row)

@app.post("/{table_name}")
def create_record(table_name: str, data: Dict[str, Any]):
    if table_name not in get_tables():
        raise HTTPException(status_code=404, detail="Table not found")
    
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?" for _ in data])
    
    with get_db() as conn:
        cursor = conn.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", list(data.values()))
        conn.commit()
        return {"id": cursor.lastrowid, "message": "Record created"}

@app.put("/{table_name}/{record_id}")
def update_record(table_name: str, record_id: int, data: Dict[str, Any]):
    if table_name not in get_tables():
        raise HTTPException(status_code=404, detail="Table not found")
    
    schema = get_table_schema(table_name)
    pk_column = next(iter(schema.keys()))
    
    set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
    
    with get_db() as conn:
        cursor = conn.execute(f"UPDATE {table_name} SET {set_clause} WHERE {pk_column} = ?", list(data.values()) + [record_id])
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Record not found")
        return {"message": "Record updated"}

@app.delete("/{table_name}/{record_id}")
def delete_record(table_name: str, record_id: int):
    if table_name not in get_tables():
        raise HTTPException(status_code=404, detail="Table not found")
    
    schema = get_table_schema(table_name)
    pk_column = next(iter(schema.keys()))
    
    with get_db() as conn:
        cursor = conn.execute(f"DELETE FROM {table_name} WHERE {pk_column} = ?", (record_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Record not found")
        return {"message": "Record deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)