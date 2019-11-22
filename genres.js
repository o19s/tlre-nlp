var movies = JSON.parse(require('fs').readFileSync('tmdb.json'));
var genres = {}
for(var movieId in movies) {
	var movie = movies[movieId];
	if (movie.genres instanceof Array) {
		for(var g=0;g<movie.genres.length;g++) {
			genre = movie.genres[g]
			if(!genres[genre.id]) {
				genres[genre.id] = genre;
				genres[genre.id]['count'] = 0;
			}
			genres[genre.id]['count']++;
		}
	}
}
console.log(genres);


for(var g in genres) {

}