from thefuzz import process
import EmbeddingHandler
import numpy as np
import logging
from OpenAI_Client import OpenAIClient
import webbrowser

logging.basicConfig(filename='logs.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class ShowSuggesterAI:
    def __init__(self):
        self.shows_embeddings_dict = EmbeddingHandler.load_shows_embeddings()
        self.user_input_shows = []
        self.recommendations = []

    def run(self):
        user_verified = False
        while not user_verified:
            user_loved_show = input(
                "Which TV shows did you love watching? Separate them by a comma. Make sure to enter more than 1 show\n")
            user_loved_show = user_loved_show.split(',')
            self.user_input_shows = [process.extractOne(show, self.shows_embeddings_dict.keys())[0] for show in
                                     user_loved_show]

            user_verified = input(f"Just to make sure, do you mean {', '.join(self.user_input_shows)} ?(y/n)\n") == 'y'
            if not user_verified:
                print("Sorry about that. Lets try again, please make sure to write the names of the tv shows correctly")
        print("Great! Generating recommendations…")

        self.create_suggestions()
        self.propose()
        self.propose_new_shows()

    def propose_new_shows(self):
        print("\nI have also created just for you two shows which I think you would love.")
        gpt = OpenAIClient()
        input_base_title, input_base_description = gpt.get_text(self.user_input_shows)
        input_base_img_url = gpt.get_img(input_base_title, input_base_description)

        print(f"""Show #1 is based on the fact that you loved the input shows that you gave me. 
Name: {input_base_title}
Description: {input_base_description}\n\n""")

        recommendations_base_title, recommendations_base_description = gpt.get_text(
            [show_name for show_name, _ in self.recommendations])
        recommendations_base_img_url = gpt.get_img(recommendations_base_title, recommendations_base_description)

        print(f"""Show #2 is based on the shows that I recommended for you.
Name: {recommendations_base_title}
Description: {recommendations_base_description}
Here are also the 2 tv show ads. Hope you like them!\n\n""")

        webbrowser.open(recommendations_base_img_url)
        webbrowser.open(input_base_img_url)

    def create_suggestions(self):
        user_shows_vectors = [self.shows_embeddings_dict[show] for show in self.user_input_shows]
        average_vector = np.mean(user_shows_vectors, axis=0)
        logging.info(average_vector)

        distances = []
        for show_name, vector in self.shows_embeddings_dict.items():
            if show_name not in self.user_input_shows:
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
        second_elements = [round(x[1], 2) for x in tuples]
        max_val = max(second_elements)
        divisor = max_val + 0.01
        normalized_elements = [(x / divisor) for x in second_elements]
        normalized_tuples = [(tuples[i][0], normalized_elements[i]) for i in range(len(tuples))]
        return normalized_tuples


def main():
    suggestor = ShowSuggesterAI()
    suggestor.run()


if __name__ == '__main__':
    main()
