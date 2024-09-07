# Imports
from fastapi import FastAPI

# Repositories
from src.repositories.embrapa.embrapa import Embrapa

# Controllers
from src.controllers import auth_controller
from src.controllers import embrapa_controller

# Instances
app = FastAPI(
    title='Embrapa wine API',
    description=f'This API is useful for getting data from "{Embrapa.EMBRAPA_URL}" and standardize its labels.',
    version='1.0'
)

# Routers
app.include_router(auth_controller.router)
app.include_router(embrapa_controller.router)

# Run script
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
