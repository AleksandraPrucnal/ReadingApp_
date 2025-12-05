from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container
from src.infrastructure.services.inflection import InflectionService
from src.infrastructure.dto.inflectionDTO import InflectionRequest, InflectionResponse

router = APIRouter(prefix="/inflection", tags=["inflection"])


@router.post("/text", response_model=InflectionResponse, status_code=status.HTTP_200_OK)
@inject
async def get_inflected_text(
        body: InflectionRequest,
        service: InflectionService = Depends(Provide[Container.inflection_service]),
) -> InflectionResponse:
    """
    Przyjmuje tekst i słownik imion, zwraca tekst po odmianie/personalizacji.
    """

    result_text = service.personalize_text(
        text=body.text,
        names=body.names
    )

    return InflectionResponse(
        original_text=body.text,
        inflected_text=result_text
    )