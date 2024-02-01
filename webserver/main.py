from fastapi import FastAPI, HTTPException
import os
import psycopg2
from psycopg2.extras import RealDictCursor
# from remote_pdb import RemotePdb

# docker-compose up -d fastapi-app
# docker-compose up -d --build fastapi-app


app = FastAPI()

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'postgres'),
        port=os.environ.get('DB_PORT', '5432'),
        database=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD']
    )

@app.get("/{name}")
async def read_age(name: str):
    # RemotePdb('0.0.0.0', 4444).set_trace()  # Set a breakpoint
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT age FROM who WHERE LOWER(name) = LOWER(%s);", (name,))
    person = cursor.fetchone()
    conn.close()

    if person:
        return person
    else:
        raise HTTPException(status_code=404, detail="Not Found")
