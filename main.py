from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine
from models import MovieModel
from scraper import MovieScraper

app = FastAPI(title='Movie Review')


@app.get('/movies')
async def movies():
    with Session(engine) as session:
        statement = select(MovieModel)
        movies_obj_list = session.scalars(statement).all()

    if movies_obj_list:
        result = []
        for m in movies_obj_list:
            result.append(
                {'id': m.id, 'title': m.title}
            )

        return result
    else:
        return HTTPException(404, 'No movies found. Search movie by title at /movie/search')


@app.get('/movie/search/{movie_name}')
async def movie_search(movie_name: str):
    movie_scraper = MovieScraper(movie_name)
    list_of_movies = await movie_scraper.parse_html_document()
    result = []
    with (Session(engine) as session):
        for movie in list_of_movies:
            statement = select(MovieModel).filter_by(title=movie.title, year=movie.year, rating=movie.rating)
            movie_obj = session.scalars(statement).first()
            if not movie_obj:
                session.add(movie)
            result.append(
                {
                    'title': movie.title,
                    'year': movie.year,
                    'rating': movie.rating,
                    'review': movie.review
                }
            )
        session.commit()

    return result

@app.get('/movie/{movie_id}')
async def movie(movie_id: int):
    with Session(engine) as session:
        movie_record = session.get(MovieModel, movie_id)

    if movie_record:
        return movie_record
    else:
        return HTTPException(404, 'Movie not found')