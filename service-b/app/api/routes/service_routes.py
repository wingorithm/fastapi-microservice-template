from http import HTTPStatus

from fastapi import APIRouter
from fastapi.params import Depends
from loguru import logger

from app.api.dependencies.service import get_crud_service
from app.model.schemas.global_response import GlobalResponse, OutputSchema
from app.service.crud_service import CrudService

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.get(
    path="/service-b/get-data",
    response_model=GlobalResponse
)
async def get_product(service: CrudService = Depends(get_crud_service))-> GlobalResponse:
    logger.info("Request get_product")
    response = await service.get_random_trainer()

    logger.info(f"Response get_product {response}")
    return GlobalResponse(
        output_schema=OutputSchema(
            http_status=HTTPStatus.OK,
            error_code="SA-000",
            message="data retrieval successful"
        ),
        content=response
    )

@router.get(
    path="/service-b/potential-trainer/{pokemon_id}",
    response_model=GlobalResponse
)
async def get_product(
        pokemon_id: int,
        service: CrudService = Depends(get_crud_service)
)-> GlobalResponse:
    logger.info("Request get_product")
    response = await service.get_trainer(pokemon_id)

    logger.info(f"Response get_product {response}")
    return GlobalResponse(
        output_schema=OutputSchema(
            http_status=HTTPStatus.OK,
            error_code="SA-000",
            message="data retrieval successful"
        ),
        content=response
    )