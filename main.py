from fastapi import FastAPI, HTTPException, status
from models.db import db
from models.models import Sheep

app = FastAPI()

@app.post("/sheep/", response_model=Sheep, status_code=status.HTTP_201_CREATED)
def add_sheep(sheep: Sheep):
    # Use db's add_sheep method to add the sheep
    try:
        return db.add_sheep(sheep)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sheep/{id}", response_model=Sheep)
def get_sheep(id: int):
    # Retrieve sheep from db by ID
    sheep = db.get_sheep(id)
    if sheep is None:
        raise HTTPException(status_code=404, detail="Sheep not found")
    return sheep

@app.delete("/sheep/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sheep(id: int):
    if id not in db.data:
        raise HTTPException(status_code=404, detail="Sheep not found")
    del db.data[id]
    return  # 204 No Content shows a successful deletion without response body

@app.put("/sheep/{id}", response_model=Sheep)
def update_sheep(id: int, updated_sheep: Sheep):
    if id not in db.data:
        raise HTTPException(status_code=404, detail="Sheep not found")
    db.data[id] = updated_sheep
    return updated_sheep

@app.get("/sheep/", response_model=list[Sheep])
def get_all_sheep():
    return list(db.data.values())
