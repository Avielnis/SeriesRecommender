import csv
import pickle
from settings import OPENAI_API_KEY
from openai import OpenAI
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class OpenAIEmbeddingsClient():
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.embeddings = {}
        self.model = "text-embedding-ada-002"

    def get_embedding(self, text):
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input=[text], model=self.model).data[0].embedding


class EmbeddingHandler():
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


def main():
    openai_client = OpenAIEmbeddingsClient(OPENAI_API_KEY)
    show_suggester = EmbeddingHandler(openai_client)
    show_suggester.load_shows("imdb_tvshows-imdb_tvshows.csv")
    show_suggester.calculate_embeddings()


def load_shows_embeddings():
    with open('embeddings.pickle', 'rb') as file:
        data = pickle.load(file)
        return data

if __name__ == "__main__":
    main()
