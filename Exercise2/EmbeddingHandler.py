import csv
import pickle
import logging
from OpenAI_Client import OpenAIClient
import os


class EmbeddingHandler:
    def __init__(self, openai_client):
        self.openai_client = openai_client
        self.shows = {}
        self.embeddings = {}

    def load_shows(self, shows_file_path):
        with open(shows_file_path, newline="", encoding='utf-8') as f:
            reader = csv.reader(f)
            reader.__next__()
            for row in reader:
                self.shows[row[0]] = row[1]
        logging.info(self.shows.keys())

    def calculate_embeddings(self):
        embeddings_file_path = 'embeddings.pickle'
        for show in self.shows:
            show_description = self.shows[show]
            self.embeddings[show] = self.openai_client.get_embedding(show_description)
            logging.info(f"{self.embeddings[show]}")

            # save embeddings to file using pickle
        with open(embeddings_file_path, 'wb') as file:
            pickle.dump(self.embeddings, file)


def load_shows_embeddings():
    embeddings_file = "embeddings.pickle"

    if not os.path.exists(embeddings_file):
        openai_client = OpenAIClient()
        show_suggester = EmbeddingHandler(openai_client)
        show_suggester.load_shows("imdb_tvshows-imdb_tvshows.csv")

    with open(embeddings_file, 'rb') as file:
        data = pickle.load(file)
        return data
