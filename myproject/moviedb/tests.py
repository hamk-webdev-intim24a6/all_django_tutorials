import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Director, Genre, Movie

# ---------------------------------------------------------------------------
# Shared test data
# ---------------------------------------------------------------------------

LONG_STRING_110K = "A" * 110_000          # well above every max_length
CHINESE_TEXT     = "功夫熊猫电影导演黑泽明"   # 10 CJK chars
ARABIC_TEXT      = "مرحباً بكم في السينما"  # Arabic greeting
CYRILLIC_TEXT    = "Кино и режиссёр"        # Russian text


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_director(first="John", last="Doe"):
    return Director.objects.create(first_name=first, last_name=last)


def make_genre(name="Action"):
    return Genre.objects.create(name=name)


def make_movie(title="Test Movie", pub_date=None, description="A great film.",
               directors=None, genres=None):
    if pub_date is None:
        pub_date = datetime.date(2000, 1, 1)
    movie = Movie.objects.create(title=title, pub_date=pub_date,
                                 description=description)
    if directors:
        movie.directors.set(directors)
    if genres:
        movie.genres.set(genres)
    return movie


# ===========================================================================
# Director model
# ===========================================================================

class DirectorModelTest(TestCase):

    # --- basic creation & __str__ -------------------------------------------

    def test_create_director(self):
        d = make_director("Steven", "Spielberg")
        self.assertEqual(d.first_name, "Steven")
        self.assertEqual(d.last_name, "Spielberg")

    def test_str(self):
        d = make_director("James", "Cameron")
        self.assertEqual(str(d), "James Cameron")

    # --- Unicode names -------------------------------------------------------

    def test_chinese_name_valid(self):
        d = Director(first_name=CHINESE_TEXT, last_name=CHINESE_TEXT)
        d.full_clean()   # must not raise
        d.save()
        self.assertEqual(Director.objects.get(pk=d.pk).first_name, CHINESE_TEXT)

    def test_arabic_name_valid(self):
        d = Director(first_name=ARABIC_TEXT, last_name=ARABIC_TEXT)
        d.full_clean()
        d.save()
        self.assertEqual(str(d), f"{ARABIC_TEXT} {ARABIC_TEXT}")

    def test_cyrillic_name_valid(self):
        d = Director(first_name=CYRILLIC_TEXT, last_name=CYRILLIC_TEXT)
        d.full_clean()
        d.save()
        self.assertIn(CYRILLIC_TEXT, str(d))

    def test_mixed_scripts_in_name(self):
        mixed = "Ян Zhang علي"
        d = Director(first_name=mixed, last_name=mixed)
        d.full_clean()
        d.save()
        self.assertEqual(Director.objects.get(pk=d.pk).first_name, mixed)

    # --- Empty strings -------------------------------------------------------

    def test_empty_first_name_raises(self):
        d = Director(first_name="", last_name="Doe")
        with self.assertRaises(ValidationError):
            d.full_clean()

    def test_empty_last_name_raises(self):
        d = Director(first_name="John", last_name="")
        with self.assertRaises(ValidationError):
            d.full_clean()

    def test_both_names_empty_raises(self):
        d = Director(first_name="", last_name="")
        with self.assertRaises(ValidationError):
            d.full_clean()

    # --- Max-length boundaries -----------------------------------------------

    def test_first_name_at_max_boundary_valid(self):
        d = Director(first_name="A" * 100, last_name="Doe")
        d.full_clean()   # exactly 100 chars – must pass
        d.save()
        self.assertEqual(len(d.first_name), 100)

    def test_first_name_one_over_max_raises(self):
        d = Director(first_name="A" * 101, last_name="Doe")
        with self.assertRaises(ValidationError):
            d.full_clean()

    def test_last_name_at_max_boundary_valid(self):
        d = Director(first_name="John", last_name="B" * 100)
        d.full_clean()
        d.save()
        self.assertEqual(len(d.last_name), 100)

    def test_last_name_one_over_max_raises(self):
        d = Director(first_name="John", last_name="B" * 101)
        with self.assertRaises(ValidationError):
            d.full_clean()

    # --- Very long strings (>100k) -------------------------------------------

    def test_first_name_110k_chars_raises(self):
        d = Director(first_name=LONG_STRING_110K, last_name="Doe")
        with self.assertRaises(ValidationError):
            d.full_clean()

    def test_last_name_110k_chars_raises(self):
        d = Director(first_name="John", last_name=LONG_STRING_110K)
        with self.assertRaises(ValidationError):
            d.full_clean()

    def test_both_names_110k_chars_raises(self):
        d = Director(first_name=LONG_STRING_110K, last_name=LONG_STRING_110K)
        with self.assertRaises(ValidationError):
            d.full_clean()


# ===========================================================================
# Genre model
# ===========================================================================

class GenreModelTest(TestCase):

    def test_create_genre(self):
        g = make_genre("Drama")
        self.assertEqual(g.name, "Drama")

    def test_str(self):
        g = make_genre("Comedy")
        self.assertEqual(str(g), "Comedy")

    # --- Unicode -------------------------------------------------------------

    def test_chinese_genre_valid(self):
        g = Genre(name=CHINESE_TEXT)
        g.full_clean()
        g.save()
        self.assertEqual(Genre.objects.get(pk=g.pk).name, CHINESE_TEXT)

    def test_arabic_genre_valid(self):
        g = Genre(name=ARABIC_TEXT)
        g.full_clean()
        g.save()
        self.assertEqual(str(g), ARABIC_TEXT)

    def test_cyrillic_genre_valid(self):
        g = Genre(name=CYRILLIC_TEXT)
        g.full_clean()
        g.save()
        self.assertIn(CYRILLIC_TEXT, str(g))

    # --- Empty string --------------------------------------------------------

    def test_empty_name_raises(self):
        g = Genre(name="")
        with self.assertRaises(ValidationError):
            g.full_clean()

    # --- Max-length boundaries -----------------------------------------------

    def test_name_at_max_boundary_valid(self):
        g = Genre(name="X" * 100)
        g.full_clean()
        g.save()
        self.assertEqual(len(g.name), 100)

    def test_name_one_over_max_raises(self):
        g = Genre(name="X" * 101)
        with self.assertRaises(ValidationError):
            g.full_clean()

    # --- Very long strings ---------------------------------------------------

    def test_name_110k_chars_raises(self):
        g = Genre(name=LONG_STRING_110K)
        with self.assertRaises(ValidationError):
            g.full_clean()


# ===========================================================================
# Movie model
# ===========================================================================

class MovieModelTest(TestCase):

    def setUp(self):
        self.director = make_director()
        self.genre    = make_genre()

    # --- basic creation & __str__ -------------------------------------------

    def test_create_movie(self):
        m = make_movie(directors=[self.director], genres=[self.genre])
        self.assertEqual(Movie.objects.count(), 1)
        self.assertIn(self.director, m.directors.all())
        self.assertIn(self.genre, m.genres.all())

    def test_str_includes_title_and_year(self):
        m = make_movie(title="Inception", pub_date=datetime.date(2010, 7, 16))
        self.assertEqual(str(m), "Inception (2010)")

    def test_str_very_old_date(self):
        m = make_movie(title="Ancient", pub_date=datetime.date(1895, 12, 28))
        self.assertEqual(str(m), "Ancient (1895)")

    # --- Date edge cases -----------------------------------------------------

    def test_year_1_ad_stored(self):
        m = Movie(title="Year One", pub_date=datetime.date(1, 1, 1),
                  description="Very old film.")
        m.full_clean()
        m.save()
        self.assertEqual(Movie.objects.get(pk=m.pk).pub_date.year, 1)

    def test_first_lumiere_screening_date(self):
        m = Movie(title="Train Arrival",
                  pub_date=datetime.date(1895, 12, 28),
                  description="First commercially screened film.")
        m.full_clean()
        m.save()
        self.assertEqual(str(m), "Train Arrival (1895)")

    def test_future_date_stored(self):
        m = Movie(title="Future Film", pub_date=datetime.date(2099, 12, 31),
                  description="Coming soon.")
        m.full_clean()
        m.save()
        self.assertEqual(Movie.objects.get(pk=m.pk).pub_date.year, 2099)

    def test_invalid_date_string_raises(self):
        m = Movie(title="Bad Date", pub_date="not-a-date",
                  description="Oops.")
        with self.assertRaises((ValidationError, ValueError, TypeError)):
            m.full_clean()

    def test_none_pub_date_raises(self):
        m = Movie(title="No Date", pub_date=None, description="Fine.")
        with self.assertRaises(ValidationError):
            m.full_clean()

    # --- Unicode titles & descriptions --------------------------------------

    def test_chinese_title_valid(self):
        m = Movie(title=CHINESE_TEXT, pub_date=datetime.date(2020, 1, 1),
                  description=CHINESE_TEXT)
        m.full_clean()
        m.save()
        self.assertEqual(Movie.objects.get(pk=m.pk).title, CHINESE_TEXT)

    def test_arabic_title_valid(self):
        m = Movie(title=ARABIC_TEXT, pub_date=datetime.date(2020, 1, 1),
                  description=ARABIC_TEXT)
        m.full_clean()
        m.save()
        self.assertIn(ARABIC_TEXT, str(m))

    def test_cyrillic_title_valid(self):
        m = Movie(title=CYRILLIC_TEXT, pub_date=datetime.date(2020, 1, 1),
                  description=CYRILLIC_TEXT)
        m.full_clean()
        m.save()
        self.assertEqual(Movie.objects.get(pk=m.pk).title, CYRILLIC_TEXT)

    def test_mixed_scripts_description(self):
        mixed = f"{CHINESE_TEXT} {ARABIC_TEXT} {CYRILLIC_TEXT} Latin"
        m = Movie(title="Multilingual", pub_date=datetime.date(2020, 1, 1),
                  description=mixed)
        m.full_clean()
        m.save()
        self.assertEqual(Movie.objects.get(pk=m.pk).description, mixed)

    # --- Empty fields --------------------------------------------------------

    def test_empty_title_raises(self):
        m = Movie(title="", pub_date=datetime.date(2000, 1, 1),
                  description="Fine.")
        with self.assertRaises(ValidationError):
            m.full_clean()

    def test_empty_description_raises(self):
        m = Movie(title="Title", pub_date=datetime.date(2000, 1, 1),
                  description="")
        with self.assertRaises(ValidationError):
            m.full_clean()

    def test_none_title_raises(self):
        m = Movie(title=None, pub_date=datetime.date(2000, 1, 1),
                  description="Fine.")
        with self.assertRaises(ValidationError):
            m.full_clean()

    # --- Max-length boundaries -----------------------------------------------

    def test_title_at_max_boundary_valid(self):
        m = Movie(title="T" * 200, pub_date=datetime.date(2000, 1, 1),
                  description="Fine.")
        m.full_clean()
        m.save()
        self.assertEqual(len(Movie.objects.get(pk=m.pk).title), 200)

    def test_title_one_over_max_raises(self):
        m = Movie(title="T" * 201, pub_date=datetime.date(2000, 1, 1),
                  description="Fine.")
        with self.assertRaises(ValidationError):
            m.full_clean()

    def test_description_at_max_boundary_valid(self):
        m = Movie(title="Title", pub_date=datetime.date(2000, 1, 1),
                  description="D" * 2000)
        m.full_clean()
        m.save()
        self.assertEqual(len(Movie.objects.get(pk=m.pk).description), 2000)

    def test_description_one_over_max_no_model_error(self):
        # TextField.max_length is enforced at the form level only in Django 6.
        # full_clean() does NOT raise for over-length TextField values;
        # form-level rejection is verified in CreateMovieViewTest.
        m = Movie(title="Title", pub_date=datetime.date(2000, 1, 1),
                  description="D" * 2001)
        m.full_clean()   # must not raise at model level

    # --- Very long strings (>100k) -------------------------------------------

    def test_title_110k_chars_raises(self):
        m = Movie(title=LONG_STRING_110K, pub_date=datetime.date(2000, 1, 1),
                  description="Fine.")
        with self.assertRaises(ValidationError):
            m.full_clean()

    def test_description_110k_chars_no_model_error(self):
        # Same as above: TextField.max_length is form-level only in Django 6.
        m = Movie(title="Title", pub_date=datetime.date(2000, 1, 1),
                  description=LONG_STRING_110K)
        m.full_clean()   # must not raise at model level

    # --- Incorrect input types -----------------------------------------------

    def test_integer_title_coerced_to_string(self):
        """Django coerces int to str for CharField; full_clean must succeed."""
        m = Movie(title=42, pub_date=datetime.date(2000, 1, 1),
                  description="Fine.")
        m.full_clean()   # should not raise


# ===========================================================================
# IndexView
# ===========================================================================

class IndexViewTest(TestCase):

    def setUp(self):
        self.url = reverse("moviedb:index")

    def test_get_empty_db_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "moviedb/index.html")

    def test_empty_queryset_on_fresh_db(self):
        response = self.client.get(self.url)
        self.assertQuerySetEqual(response.context["latest_movies"], [])

    def test_past_movie_shown(self):
        make_movie(title="Old Film", pub_date=datetime.date(1980, 6, 1))
        response = self.client.get(self.url)
        self.assertContains(response, "Old Film")

    def test_future_movie_not_shown(self):
        make_movie(title="Upcoming Film", pub_date=datetime.date(2099, 1, 1))
        response = self.client.get(self.url)
        self.assertNotContains(response, "Upcoming Film")

    def test_today_movie_shown(self):
        make_movie(title="Today Film", pub_date=timezone.now().date())
        response = self.client.get(self.url)
        self.assertContains(response, "Today Film")

    def test_movies_ordered_newest_first(self):
        make_movie(title="Film 1990", pub_date=datetime.date(1990, 1, 1))
        make_movie(title="Film 2000", pub_date=datetime.date(2000, 1, 1))
        make_movie(title="Film 1970", pub_date=datetime.date(1970, 1, 1))
        response = self.client.get(self.url)
        movies = list(response.context["latest_movies"])
        self.assertEqual(movies[0].title, "Film 2000")
        self.assertEqual(movies[1].title, "Film 1990")
        self.assertEqual(movies[2].title, "Film 1970")

    def test_pagination_first_page_has_five(self):
        for i in range(6):
            make_movie(title=f"Film {i}", pub_date=datetime.date(2000 + i, 1, 1))
        response = self.client.get(self.url)
        self.assertEqual(len(response.context["latest_movies"]), 5)

    def test_pagination_second_page_has_one(self):
        for i in range(6):
            make_movie(title=f"Film {i}", pub_date=datetime.date(2000 + i, 1, 1))
        response = self.client.get(self.url + "?page=2")
        self.assertEqual(len(response.context["latest_movies"]), 1)

    def test_unicode_titles_displayed(self):
        make_movie(title=CHINESE_TEXT,  pub_date=datetime.date(2020, 1, 1))
        make_movie(title=ARABIC_TEXT,   pub_date=datetime.date(2020, 1, 2))
        make_movie(title=CYRILLIC_TEXT, pub_date=datetime.date(2020, 1, 3))
        response = self.client.get(self.url)
        self.assertContains(response, CHINESE_TEXT)
        self.assertContains(response, ARABIC_TEXT)
        self.assertContains(response, CYRILLIC_TEXT)

    def test_very_old_date_movie_shown(self):
        make_movie(title="Ancient Film", pub_date=datetime.date(1, 1, 1))
        response = self.client.get(self.url)
        self.assertContains(response, "Ancient Film")

    def test_page_out_of_range_returns_404(self):
        response = self.client.get(self.url + "?page=9999")
        self.assertEqual(response.status_code, 404)


# ===========================================================================
# CreateMovieView
# ===========================================================================

class CreateMovieViewTest(TestCase):

    def setUp(self):
        self.url      = reverse("moviedb:create")
        self.director = make_director()
        self.genre    = make_genre()

    def _post_data(self, **overrides):
        data = {
            "title":       "New Movie",
            "pub_date":    "2020-06-15",
            "description": "A great film.",
            "directors":   [self.director.pk],
            "genres":      [self.genre.pk],
        }
        data.update(overrides)
        return data

    # --- GET -----------------------------------------------------------------

    def test_get_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moviedb/create.html")

    # --- Valid POST ----------------------------------------------------------

    def test_valid_post_creates_movie(self):
        self.client.post(self.url, self._post_data())
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(Movie.objects.first().title, "New Movie")

    def test_valid_post_redirects_to_index(self):
        response = self.client.post(self.url, self._post_data())
        self.assertRedirects(response, reverse("moviedb:index"))

    # --- Empty fields --------------------------------------------------------

    def test_empty_title_rejected(self):
        response = self.client.post(self.url, self._post_data(title=""))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movie.objects.count(), 0)

    def test_empty_description_rejected(self):
        response = self.client.post(self.url, self._post_data(description=""))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movie.objects.count(), 0)

    def test_missing_date_rejected(self):
        response = self.client.post(self.url, self._post_data(pub_date=""))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movie.objects.count(), 0)

    # --- Very long strings ---------------------------------------------------

    def test_title_over_200_chars_rejected(self):
        response = self.client.post(self.url, self._post_data(title="T" * 201))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movie.objects.count(), 0)

    def test_title_110k_chars_rejected(self):
        response = self.client.post(self.url, self._post_data(title=LONG_STRING_110K))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movie.objects.count(), 0)

    def test_description_over_2000_chars_rejected(self):
        response = self.client.post(self.url,
                                    self._post_data(description="D" * 2001))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movie.objects.count(), 0)

    def test_description_110k_chars_rejected(self):
        response = self.client.post(self.url,
                                    self._post_data(description=LONG_STRING_110K))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movie.objects.count(), 0)

    # --- Unicode -------------------------------------------------------------

    def test_chinese_title_and_description(self):
        self.client.post(self.url,
                         self._post_data(title=CHINESE_TEXT,
                                         description=CHINESE_TEXT))
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(Movie.objects.first().title, CHINESE_TEXT)

    def test_arabic_title_and_description(self):
        self.client.post(self.url,
                         self._post_data(title=ARABIC_TEXT,
                                         description=ARABIC_TEXT))
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(Movie.objects.first().title, ARABIC_TEXT)

    def test_cyrillic_title_and_description(self):
        self.client.post(self.url,
                         self._post_data(title=CYRILLIC_TEXT,
                                         description=CYRILLIC_TEXT))
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(Movie.objects.first().title, CYRILLIC_TEXT)

    # --- Date edge cases -----------------------------------------------------

    def test_very_old_date_accepted(self):
        self.client.post(self.url, self._post_data(pub_date="0001-01-01"))
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(Movie.objects.first().pub_date.year, 1)

    def test_future_date_accepted(self):
        self.client.post(self.url, self._post_data(pub_date="2099-12-31"))
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(Movie.objects.first().pub_date.year, 2099)

    def test_invalid_date_string_rejected(self):
        response = self.client.post(self.url,
                                    self._post_data(pub_date="not-a-date"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movie.objects.count(), 0)

    def test_dd_mm_yyyy_format_rejected(self):
        response = self.client.post(self.url,
                                    self._post_data(pub_date="15/06/2020"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movie.objects.count(), 0)

    def test_month_out_of_range_rejected(self):
        response = self.client.post(self.url,
                                    self._post_data(pub_date="2020-13-01"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movie.objects.count(), 0)

    def test_day_out_of_range_rejected(self):
        response = self.client.post(self.url,
                                    self._post_data(pub_date="2020-01-32"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movie.objects.count(), 0)

    # --- Invalid relation IDs ------------------------------------------------

    def test_nonexistent_director_id_rejected(self):
        response = self.client.post(self.url,
                                    self._post_data(directors=[99999]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movie.objects.count(), 0)

    def test_nonexistent_genre_id_rejected(self):
        response = self.client.post(self.url,
                                    self._post_data(genres=[99999]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movie.objects.count(), 0)

    def test_no_directors_rejected(self):
        data = self._post_data()
        del data["directors"]
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movie.objects.count(), 0)

    def test_no_genres_rejected(self):
        data = self._post_data()
        del data["genres"]
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movie.objects.count(), 0)


# ===========================================================================
# UpdateMovieView
# ===========================================================================

class UpdateMovieViewTest(TestCase):

    def setUp(self):
        self.director = make_director()
        self.genre    = make_genre()
        self.movie    = make_movie(directors=[self.director],
                                   genres=[self.genre])
        self.url      = reverse("moviedb:update", kwargs={"pk": self.movie.pk})

    def _update_data(self, **overrides):
        data = {
            "title":       "Updated Title",
            "pub_date":    "2021-03-10",
            "description": "Updated description.",
            "directors":   [self.director.pk],
            "genres":      [self.genre.pk],
        }
        data.update(overrides)
        return data

    # --- GET -----------------------------------------------------------------

    def test_get_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moviedb/update.html")

    def test_nonexistent_pk_returns_404(self):
        url = reverse("moviedb:update", kwargs={"pk": 99999})
        self.assertEqual(self.client.get(url).status_code, 404)

    # --- Valid POST ----------------------------------------------------------

    def test_valid_post_updates_title_and_date(self):
        self.client.post(self.url, self._update_data())
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, "Updated Title")
        self.assertEqual(self.movie.pub_date, datetime.date(2021, 3, 10))

    def test_valid_post_redirects_to_index(self):
        response = self.client.post(self.url, self._update_data())
        self.assertRedirects(response, reverse("moviedb:index"))

    # --- Empty / too-long fields ---------------------------------------------

    def test_empty_title_rejected(self):
        self.client.post(self.url, self._update_data(title=""))
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, "Test Movie")  # unchanged

    def test_title_110k_chars_rejected(self):
        response = self.client.post(self.url,
                                    self._update_data(title=LONG_STRING_110K))
        self.assertEqual(response.status_code, 200)
        self.movie.refresh_from_db()
        self.assertNotEqual(self.movie.title, LONG_STRING_110K)

    def test_description_110k_chars_rejected(self):
        response = self.client.post(
            self.url, self._update_data(description=LONG_STRING_110K))
        self.assertEqual(response.status_code, 200)
        self.movie.refresh_from_db()
        self.assertNotEqual(self.movie.description, LONG_STRING_110K)

    # --- Unicode updates -----------------------------------------------------

    def test_update_with_chinese_title(self):
        self.client.post(self.url,
                         self._update_data(title=CHINESE_TEXT,
                                           description=CHINESE_TEXT))
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, CHINESE_TEXT)

    def test_update_with_arabic_title(self):
        self.client.post(self.url,
                         self._update_data(title=ARABIC_TEXT,
                                           description=ARABIC_TEXT))
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, ARABIC_TEXT)

    def test_update_with_cyrillic_title(self):
        self.client.post(self.url,
                         self._update_data(title=CYRILLIC_TEXT,
                                           description=CYRILLIC_TEXT))
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, CYRILLIC_TEXT)

    # --- Date edge cases -----------------------------------------------------

    def test_update_with_year_1_ad(self):
        self.client.post(self.url, self._update_data(pub_date="0001-01-01"))
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.pub_date.year, 1)

    def test_update_with_future_date(self):
        self.client.post(self.url, self._update_data(pub_date="2099-12-31"))
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.pub_date.year, 2099)

    def test_update_with_invalid_date_rejected(self):
        original_date = self.movie.pub_date
        response = self.client.post(self.url,
                                    self._update_data(pub_date="not-a-date"))
        self.assertEqual(response.status_code, 200)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.pub_date, original_date)  # unchanged


# ===========================================================================
# DeleteMovieView
# ===========================================================================

class DeleteMovieViewTest(TestCase):

    def setUp(self):
        self.movie = make_movie()
        self.url   = reverse("moviedb:delete", kwargs={"pk": self.movie.pk})

    def test_get_shows_confirmation_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moviedb/movie_confirm_delete.html")

    def test_post_deletes_movie(self):
        self.assertEqual(Movie.objects.count(), 1)
        self.client.post(self.url)
        self.assertEqual(Movie.objects.count(), 0)

    def test_post_redirects_to_index(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("moviedb:index"))

    def test_delete_nonexistent_pk_returns_404(self):
        url = reverse("moviedb:delete", kwargs={"pk": 99999})
        self.assertEqual(self.client.post(url).status_code, 404)

    def test_delete_movie_with_unicode_title(self):
        m   = make_movie(title=CHINESE_TEXT, pub_date=datetime.date(2020, 1, 1))
        url = reverse("moviedb:delete", kwargs={"pk": m.pk})
        self.client.post(url)
        self.assertFalse(Movie.objects.filter(pk=m.pk).exists())

    def test_delete_movie_with_very_old_date(self):
        m   = make_movie(title="Ancient", pub_date=datetime.date(1, 1, 1))
        url = reverse("moviedb:delete", kwargs={"pk": m.pk})
        self.client.post(url)
        self.assertFalse(Movie.objects.filter(pk=m.pk).exists())

    def test_delete_movie_with_future_date(self):
        m   = make_movie(title="Future", pub_date=datetime.date(2099, 1, 1))
        url = reverse("moviedb:delete", kwargs={"pk": m.pk})
        self.client.post(url)
        self.assertFalse(Movie.objects.filter(pk=m.pk).exists())

    def test_get_on_deleted_pk_returns_404(self):
        self.client.post(self.url)   # delete it first
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)
