import uvicorn
from fastapi import FastAPI

from app.routers import router
from app.auth.routers import router as auth_routers


app = FastAPI()
app.include_router(router)
app.include_router(auth_routers)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
