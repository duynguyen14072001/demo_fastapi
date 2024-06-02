from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
import models
from database import engine, sessionlocal
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from datetime import date as date_type

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", name="home")
async def home(request: Request, db: Session = Depends(get_db)):
    spendings = db.query(models.Spending).order_by(models.Spending.id.desc())
    return templates.TemplateResponse("home.html", {"request": request, "spendings": spendings})

@app.post("/create")
async def add(request: Request, name: str = Form(...), date: date_type = Form(...), amount: float = Form(...), type: str = Form(...), db: Session = Depends(get_db)):
    spendings = models.Spending(name=name, date=date, amount=amount, type=type)
    db.add(spendings)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/edit/{spend_id}")
async def update(request: Request, spend_id: int, db: Session = Depends(get_db)):
    spending = db.query(models.Spending).filter(models.Spending.id == spend_id).first()
    if spending is None:
        raise HTTPException(status_code=404, detail="Spending not found")
    return templates.TemplateResponse("edit.html", {"request": request, "spending": spending})

@app.post("/update/{spend_id}")
async def update(request: Request, spend_id: int, name: str = Form(...), date: date_type = Form(...), amount: float = Form(...), type: str = Form(...), db: Session = Depends(get_db)):
    spending = db.query(models.Spending).filter(models.Spending.id == spend_id).first()
    if spending is None:
        raise HTTPException(status_code=404, detail="Spending not found")
    spending.name = name
    spending.date = date
    spending.amount = amount
    spending.type = type
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.delete("/delete/{spend_id}")
async def delete(request: Request, spend_id: int, db: Session = Depends(get_db)):
    spending = db.query(models.Spending).filter(models.Spending.id == spend_id).first()
    if spending is None:
        raise HTTPException(status_code=404, detail="Spending not found")
    db.delete(spending)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)