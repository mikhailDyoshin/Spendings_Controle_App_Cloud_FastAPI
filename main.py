from fastapi import FastAPI
import uvicorn
from routes.users import user_router
from routes.spendings import event_router
from database.connection import Settings


app = FastAPI()

settings = Settings()

# Register routes
app.include_router(user_router, prefix='/user')
app.include_router(event_router, prefix='/event')

# Initializing the database when the app starts up
@app.on_event('startup')
async def init_db():
    await settings.initialize_database()


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
