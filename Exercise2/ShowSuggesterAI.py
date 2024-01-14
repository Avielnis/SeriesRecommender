from thefuzz import process
import EmbeddingHandler
import numpy as np
import logging

logging.basicConfig(filename='logs.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class ShowSeggusterAI():

    def __init__(self):
        self.shows_embeddings_dict = EmbeddingHandler.load_shows_embeddings()
        self.user_shows = []
        self.user_shows_vectors = []
        self.recommendations = []

    def run(self):
        user_verify = False
        while not user_verify:
            user_loved_show = input(
                "Which TV shows did you love watching? Separate them by a comma. Make sure to enter more than 1 show\n")
            user_loved_show = user_loved_show.split(',')
            self.user_shows = [process.extractOne(show, self.shows_embeddings_dict.keys())[0] for show in
                               user_loved_show]

            user_verify = input(f"Just to make sure, do you mean {','.join(self.user_shows)} ?(y/n)\n") == 'y'
            if not user_verify:
                print("Sorry about that. Lets try again, please make sure to write the names of the tv shows correctly")
        print("“Great! Generating recommendations…")

        self.create_suggestions()
        self.propose()

    def create_suggestions(self):
        self.user_shows_vectors = [self.shows_embeddings_dict[show] for show in self.user_shows]
        average_vector = np.mean(self.user_shows_vectors, axis=0)
        logging.info(average_vector)

        distances = []
        for show_name, vector in self.shows_embeddings_dict.items():
            if show_name not in self.user_shows:
                distances.append((show_name, self.cosine_similarity(average_vector, vector)))

        distances = sorted(distances, key=lambda item: item[1])
        distances = self.normalize_tuples(distances)
        self.recommendations = distances[-5:][::-1]
        logging.info(distances)

    def propose(self):
        print("Here are the tv shows that i think you would love:")
        for show_name, p in self.recommendations:
            print(f"{show_name} ({int(p * 100)}%)")

    @staticmethod
    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    @staticmethod
    def normalize_tuples(tuples):
        second_elements = [x[1] for x in tuples]
        max_val = max(second_elements)
        divisor = max_val + 0.01
        normalized_elements = [(x / divisor) for x in second_elements]
        normalized_tuples = [(tuples[i][0], normalized_elements[i]) for i in range(len(tuples))]
        return normalized_tuples


def main():
    suggestor = ShowSeggusterAI()
    suggestor.run()


if __name__ == '__main__':
    main()
