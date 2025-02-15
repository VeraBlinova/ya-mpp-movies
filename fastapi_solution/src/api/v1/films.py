from http import HTTPStatus
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from models.film import FilmList, FilmSearchResult

from models.film import Film
from services.film import FilmService, get_film_service
from auth import security_jwt

router = APIRouter()


@router.get("/", response_model=list[FilmList])
async def list_films(
    user: Annotated[dict, Depends(security_jwt)],
    sort: Optional[str] = Query(None),
    genre: Optional[str] = None,
    film_service: FilmService = Depends(get_film_service),
):
    films = await film_service.list_films(genre=genre, sort=sort)
    return films



@router.get("/popular", response_model=list[FilmList])
async def get_popular_films(
    sort: Optional[str] = Query(None),
    film_service: FilmService = Depends(get_film_service)
):
    return await film_service.get_popular_films(sort=sort)


@router.get("/{film_id}/similar", response_model=list[FilmSearchResult])
async def get_similar_films(
    user: Annotated[dict, Depends(security_jwt)],
    film_id: str,
    film_service: FilmService = Depends(get_film_service)
):
    return await film_service.get_similar_films(str(film_id))


@router.get("/search", response_model=list[FilmSearchResult])
async def search_films(
    user: Annotated[dict, Depends(security_jwt)],
    query: str = Query(None),
    page_number: int = Query(1),
    page_size: int = Query(50),
    film_service: FilmService = Depends(get_film_service)
):
    return await film_service.search_films(
        query=query,
        page_number=page_number,
        page_size=page_size,
    )


@router.get('/{film_id}', response_model=Film)
async def film_details(
    user: Annotated[dict, Depends(security_jwt)],
    film_id: str,
    film_service:
    FilmService = Depends(get_film_service)
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return film
