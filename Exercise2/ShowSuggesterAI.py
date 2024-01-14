from thefuzz import process
import EmbeddingHandler
import numpy as np
import logging


class ShowSeggusterAI():
    def __init__(self):
        self.shows_embeddings_dict = EmbeddingHandler.load_shows_embeddings()
        self.user_shows = []
        self.user_shows_vectors = []

    def run(self):
        user_verify = False
        while not user_verify:
            user_loved_show = input(
                "Which TV shows did you love watching? Separate them by a comma. Make sure to enter more than 1 show")
            user_loved_show = user_loved_show.split(',')
            self.user_shows = [process.extractOne(show, self.shows_embeddings_dict.keys())[0] for show in
                               user_loved_show]

            user_verify = input(f"Just to make sure, do you mean {','.join(self.user_shows)} ?(y/n)") == 'y'
            if not user_verify:
                print("Sorry about that. Lets try again, please make sure to write the names of the tv shows correctly")
        print("“Great! Generating recommendations…")
        self.create_suggestions()

    def create_suggestions(self):
        self.user_shows_vectors = [self.shows_embeddings_dict[show] for show in self.user_shows]
        average_vector = np.mean(self.user_shows_vectors, axis=0)
        logging.info(average_vector)

        distances = []
        for show_name, vector in self.shows_embeddings_dict.items():
            if show_name not in self.user_shows:
                distances.append((show_name, self.cosine_similarity(average_vector, vector)))

        distances = sorted(distances, key=lambda item: item[1])
        distances = distances[-5:]
        logging.info(distances)
        #TODO: calculate precentage and print message

    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def main():
    suggestor = ShowSeggusterAI()
    suggestor.run()


if __name__ == '__main__':
    main()
