from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from src.core.domain.topic import TopicIn
from src.infrastructure.dto.topicDTO import TopicDTO
from src.infrastructure.services.topic import TopicService
from src.container import Container

router = APIRouter(prefix="/topic", tags=["topic"])


@router.get("/", response_model=list[TopicDTO])
@inject
async def list_topics(
    service: TopicService = Depends(Provide[Container.topic_service]),
):
    return await service.get_all()


@router.get("/{id_topic}", response_model=TopicDTO)
@inject
async def get_topic(
    id_topic: int,
    service: TopicService = Depends(Provide[Container.topic_service]),
):
    topic = await service.get_by_id(id_topic)
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    return topic


@router.post(
    "/", response_model=TopicDTO, status_code=status.HTTP_201_CREATED
)
@inject
async def create_topic(
    payload: TopicIn,
    service: TopicService = Depends(Provide[Container.topic_service]),
):
    created = await service.create(payload)
    if not created:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Topic already exists")
    return created


@router.put("/{id_topic}", response_model=TopicDTO)
@inject
async def update_topic(
    id_topic: int,
    payload: TopicIn,
    service: TopicService = Depends(Provide[Container.topic_service]),
):
    updated = await service.update(id_topic, payload)
    if not updated:
        # brak rekordu lub konflikt nazwy
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found or name conflict")
    return updated


@router.delete("/{id_topic}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_topic(
    id_topic: int,
    service: TopicService = Depends(Provide[Container.topic_service]),
):
    ok = await service.delete(id_topic)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    return None
