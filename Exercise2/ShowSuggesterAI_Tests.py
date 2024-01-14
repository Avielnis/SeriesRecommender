import pytest
from EmbeddingHandler import EmbeddingHandler
from ShowSuggesterAI import ShowSuggesterAI
import numpy as np


@pytest.fixture
def show_suggester():
    show_suggester = ShowSuggesterAI()
    show_suggester.user_input_shows = ["Game of Thrones", "Breaking Bad", "The Walking Dead"]
    return show_suggester


@pytest.fixture
def embedding_handler():
    return EmbeddingHandler(None)


def test_cosine_similarity(show_suggester):
    vec_a = np.array([1, 2, 3])
    vec_b = np.array([4, 5, 6])
    similarity = show_suggester.cosine_similarity(vec_a, vec_b)
    assert round(similarity, 4) == round(0.9746318461970762, 4)


@pytest.mark.parametrize("input_tuples, expected_output", [
    ([('show1', 0.5), ('show2', 0.75), ('show3', 1.0)],
     [('show1', 0.5 / 1.01), ('show2', 0.75 / 1.01), ('show3', 1.0 / 1.01)]),

    # Test when one value is negative
    ([('show1', 0.5), ('show2', -0.75), ('show3', 1.0)],
     [('show1', 0.5 / 1.01), ('show2', -0.75 / 1.01), ('show3', 1.0 / 1.01)]),

    # Test with more decimal places
    ([('show1', 0.12345), ('show2', 0.67890), ('show3', 0.99999)],
     [('show1', 0.1188118811881188), ('show2', 0.6732673267326733), ('show3', 0.9900990099009901)])
])
def test_normalize_tuples(show_suggester, input_tuples, expected_output):
    normalized_tuples = show_suggester.normalize_tuples(input_tuples)
    assert normalized_tuples == expected_output


def test_create_suggestions(show_suggester):
    show_suggester.create_suggestions()
    assert show_suggester.recommendations == [('Falling Skies', 0.9887640449438202),
                                              ('Heroes', 0.9887640449438202),
                                              ('The Originals', 0.9887640449438202),
                                              ('Sense8', 0.9887640449438202),
                                              ('Grimm', 0.9887640449438202)]


def test_load_shows_from_csv_file(embedding_handler):
    embedding_handler.load_shows("imdb_tvshows-imdb_tvshows.csv")
    assert list(embedding_handler.shows.items())[:1] == [('Game of Thrones',
                                                          'Nine noble families fight for control over the lands of '
                                                          'Westeros, while an ancient enemy returns after being '
                                                          'dormant for millennia.')]
