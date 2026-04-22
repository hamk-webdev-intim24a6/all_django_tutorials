import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from moviedb.models import Director, Genre, Movie
from datetime import date

MOVIES = [
    {
        "title": "The Shawshank Redemption",
        "pub_date": date(1994, 9, 23),
        "directors": [("Frank", "Darabont")],
        "genres": ["Drama"],
        "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
    },
    {
        "title": "The Godfather",
        "pub_date": date(1972, 3, 24),
        "directors": [("Francis Ford", "Coppola")],
        "genres": ["Crime", "Drama"],
        "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
    },
    {
        "title": "The Dark Knight",
        "pub_date": date(2008, 7, 18),
        "directors": [("Christopher", "Nolan")],
        "genres": ["Action", "Crime", "Drama"],
        "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
    },
    {
        "title": "Schindler's List",
        "pub_date": date(1993, 12, 15),
        "directors": [("Steven", "Spielberg")],
        "genres": ["Biography", "Drama", "History"],
        "description": "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis.",
    },
    {
        "title": "The Lord of the Rings: The Return of the King",
        "pub_date": date(2003, 12, 17),
        "directors": [("Peter", "Jackson")],
        "genres": ["Action", "Adventure", "Drama"],
        "description": "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.",
    },
    {
        "title": "Pulp Fiction",
        "pub_date": date(1994, 10, 14),
        "directors": [("Quentin", "Tarantino")],
        "genres": ["Crime", "Drama"],
        "description": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
    },
    {
        "title": "Inception",
        "pub_date": date(2010, 7, 16),
        "directors": [("Christopher", "Nolan")],
        "genres": ["Action", "Adventure", "Sci-Fi"],
        "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
    },
    {
        "title": "The Matrix",
        "pub_date": date(1999, 3, 31),
        "directors": [("Lana", "Wachowski"), ("Lilly", "Wachowski")],
        "genres": ["Action", "Sci-Fi"],
        "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
    },
    {
        "title": "Goodfellas",
        "pub_date": date(1990, 9, 19),
        "directors": [("Martin", "Scorsese")],
        "genres": ["Biography", "Crime", "Drama"],
        "description": "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners Jimmy Conway and Tommy DeVito.",
    },
    {
        "title": "Interstellar",
        "pub_date": date(2014, 11, 7),
        "directors": [("Christopher", "Nolan")],
        "genres": ["Adventure", "Drama", "Sci-Fi"],
        "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
    },
    {
        "title": "Forrest Gump",
        "pub_date": date(1994, 7, 6),
        "directors": [("Robert", "Zemeckis")],
        "genres": ["Drama", "Romance"],
        "description": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold through the perspective of an Alabama man with an IQ of 75.",
    },
    {
        "title": "Fight Club",
        "pub_date": date(1999, 10, 15),
        "directors": [("David", "Fincher")],
        "genres": ["Drama"],
        "description": "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into something much, much more.",
    },
    {
        "title": "The Silence of the Lambs",
        "pub_date": date(1991, 2, 14),
        "directors": [("Jonathan", "Demme")],
        "genres": ["Crime", "Drama", "Thriller"],
        "description": "A young FBI cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer, a madman who skins his victims.",
    },
    {
        "title": "Parasite",
        "pub_date": date(2019, 5, 30),
        "directors": [("Bong", "Joon-ho")],
        "genres": ["Comedy", "Drama", "Thriller"],
        "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
    },
    {
        "title": "The Green Mile",
        "pub_date": date(1999, 12, 10),
        "directors": [("Frank", "Darabont")],
        "genres": ["Crime", "Drama", "Fantasy"],
        "description": "The lives of guards on Death Row are affected by one of their charges: a black man accused of child murder and rape, yet who has a mysterious gift.",
    },
    {
        "title": "Gladiator",
        "pub_date": date(2000, 5, 5),
        "directors": [("Ridley", "Scott")],
        "genres": ["Action", "Adventure", "Drama"],
        "description": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
    },
    {
        "title": "The Lion King",
        "pub_date": date(1994, 6, 24),
        "directors": [("Roger", "Allers"), ("Rob", "Minkoff")],
        "genres": ["Animation", "Adventure", "Drama"],
        "description": "Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself.",
    },
    {
        "title": "Whiplash",
        "pub_date": date(2014, 10, 10),
        "directors": [("Damien", "Chazelle")],
        "genres": ["Drama", "Music"],
        "description": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing to realize a student's potential.",
    },
    {
        "title": "The Departed",
        "pub_date": date(2006, 10, 6),
        "directors": [("Martin", "Scorsese")],
        "genres": ["Crime", "Drama", "Thriller"],
        "description": "An undercover cop and a mole in the police attempt to identify each other while simultaneously infiltrating an Irish gang in South Boston.",
    },
    {
        "title": "Spirited Away",
        "pub_date": date(2001, 7, 20),
        "directors": [("Hayao", "Miyazaki")],
        "genres": ["Animation", "Adventure", "Family"],
        "description": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.",
    },
]


def get_or_create_director(first_name, last_name):
    director, _ = Director.objects.get_or_create(
        first_name=first_name,
        last_name=last_name,
    )
    return director


def get_or_create_genre(name):
    genre, _ = Genre.objects.get_or_create(name=name)
    return genre


def populate():
    created_count = 0
    skipped_count = 0

    for movie_data in MOVIES:
        if Movie.objects.filter(title=movie_data["title"]).exists():
            print(f"  SKIP  {movie_data['title']}")
            skipped_count += 1
            continue

        directors = [
            get_or_create_director(fn, ln)
            for fn, ln in movie_data["directors"]
        ]
        genres = [get_or_create_genre(name) for name in movie_data["genres"]]

        movie = Movie.objects.create(
            title=movie_data["title"],
            pub_date=movie_data["pub_date"],
            description=movie_data["description"],
        )
        movie.directors.set(directors)
        movie.genres.set(genres)

        print(f"  ADD   {movie}")
        created_count += 1

    print(f"\nDone. Added: {created_count}, Skipped: {skipped_count}")


if __name__ == "__main__":
    populate()
