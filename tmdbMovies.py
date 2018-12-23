import json


def rawTmdbMovies():
    return json.load(open('tmdb.json'))


def writeTmdmMovies(rawMoviesJson, path):
    with open(path, 'w') as f:
        json.dump(rawMoviesJson, f)

def tmdbMovies():
    tmdbMovies = rawTmdbMovies()
    for movieId, tmdbMovie in tmdbMovies.items():
        yield (movieId, tmdbMovie)


def indexableMovies():
    """ Generates TMDB movies, similar to how ES Bulk indexing
        uses a generator to generate bulk index/update actions """
    for movieId, tmdbMovie in tmdbMovies():
        try:
            releaseDate = None
            if 'release_date' in tmdbMovie and len(tmdbMovie['release_date']) > 0:
                releaseDate = tmdbMovie['release_date'] + 'T00:00:00Z'

            yield {'id': movieId,
                   'title': tmdbMovie['title'],
                   'overview': tmdbMovie['overview'],
                   'tagline': tmdbMovie['tagline'],
                   'directors': [director['name'] for director in tmdbMovie['directors']],
                   'cast': [castMember['name'] for castMember in tmdbMovie['cast']],
                   'genres': [genre['name'] for genre in tmdbMovie['genres']],
                   'release_date': releaseDate,
                   'vote_average': tmdbMovie['vote_average'] if 'vote_average' in tmdbMovie else None,
                   'vote_count': int(tmdbMovie['vote_count']) if 'vote_count' in tmdbMovie else None,
                   }
        except KeyError as k: # Ignore any movies missing these attributes
            continue