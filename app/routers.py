from fastapi import APIRouter, Query, Depends
from fastapi.responses import RedirectResponse

from app.schemas import URLSchema, URLCreate
from app.crud import (
    original_url_by_alias,
    create_alias as alias,
    all_aliases,
    deactivation_alias as deactivation,
    click_count,
)
from app.auth.auth import get_current_user


router = APIRouter()


@router.get("/all_aliases", summary="Вывод всех активных ссылок с пагинацией")
async def get_all_aliases(
    skip: int = Query(0, alias="skip"),
    limit: int = Query(10, alias="limit"),
    auth_user=Depends(get_current_user),
):
    return await all_aliases(skip, limit)


@router.post(
    "/create_alias", response_model=URLSchema, summary="Генерация короткой ссылки"
)
async def create_alias(url: URLCreate, auth_user=Depends(get_current_user)):
    return await alias(url.original_url)


@router.get("/{alias}", summary="Перенаправление на оригинальный URL")
async def redirect_url(alias: str):
    original_url = await original_url_by_alias(alias)
    await click_count(alias)
    return RedirectResponse(original_url.original_url)


@router.post("/deactivation_alias", summary="Деактивация короткой ссылки")
async def deactivation_alias(alias, auth_user=Depends(get_current_user)):
    return await deactivation(alias)
