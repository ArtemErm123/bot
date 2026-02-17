from fastapi import APIRouter

from app.api.v1 import calculate, calculations, compare, materials, mixes, predict, projects, reports, variants

api_router = APIRouter()
api_router.include_router(projects.router)
api_router.include_router(variants.router)
api_router.include_router(materials.router)
api_router.include_router(mixes.router)
api_router.include_router(calculations.router)
api_router.include_router(reports.router)
api_router.include_router(calculate.router)
api_router.include_router(predict.router)
api_router.include_router(compare.router)
