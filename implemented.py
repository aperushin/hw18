from dao.director import DirectorDAO
from dao.genre import GenreDAO
from dao.model.models import MovieSchema, DirectorSchema, GenreSchema
from dao.movie import MovieDAO
from service.director import DirectorService
from service.genre import GenreService
from service.movie import MovieService
from setup_db import db

movie_dao = MovieDAO(db.session)
movie_service = MovieService(movie_dao)
movie_schema = MovieSchema()

director_dao = DirectorDAO(db.session)
director_service = DirectorService(director_dao)
director_schema = DirectorSchema()

genre_dao = GenreDAO(db.session)
genre_service = GenreService(genre_dao)
genre_schema = GenreSchema()
