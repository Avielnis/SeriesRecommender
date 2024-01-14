import csv
import pickle
from settings import OPENAI_API_KEY
from openai import OpenAI


class OpenAIEmbeddingsClient():
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.embeddings = {}
        self.model = "text-embedding-ada-002"

    def get_embedding(self, text):
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input = [text], model=self.model).data[0].embedding


class ShowSuggesterAI():
    def __init__(self, openai_client):
        self.openai_client = openai_client
        self.shows = {}
        self.embeddings = {}
    
    def load_shows(self, shows_file_path):
        with open(shows_file_path, newline="") as f:
            reader = csv.reader(f)
            # reader.__next__()
            for row in reader:
                self.shows[row[0]] = row[1]

    def calculate_embeddings(self, embeddings_file_path):
        for show in self.shows:
            show_description = self.shows[show]
            self.embeddings[show] = self.openai_client.get_embedding(show_description)
        
        # save embeddings to file using pickle
        with open('my_dict.pickle', 'wb') as file:
            pickle.dump(embeddings_file_path, file)
    


def main():
    openai_client = OpenAIEmbeddingsClient(OPENAI_API_KEY)
    show_suggester = ShowSuggesterAI(openai_client)
    show_suggester.load_shows(r"C:\Users\rlapu\Desktop\Univeristy\Software-Development-Using-AI\Assignment-2\Exercise2\imdb_tvshows-imdb_tvshows.csv")
    print(show_suggester.shows)

if __name__ == "__main__":
    main()