import json
import logging

from settings import OPENAI_API_KEY
from openai import OpenAI


class OpenAIEmbeddingsClient():
    def __init__(self, ):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.embeddings = {}
        self.embedding_model = "text-embedding-ada-002"
        self.text_model = "gpt-3.5-turbo-1106"
        self.img_model = "dall-e-3"

    def get_embedding(self, text):
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input=[text], model=self.embedding_model).data[0].embedding

    def get_text(self, lst: list):
        # prompt = "Give me on the base of this list a new TV - series:" \
        #          f"{','.join(lst)} " \
        #          f"in this format:" \
        #          f"Title: the title" \
        #          f"Description : the description"
        prompt = f"Here is a list of TV series: {','.join(lst)}" \
                 "Based on this list, output a new TV series that doesn't exist that might be similar. " \
                 "Give a short paragraph about the story plot" \
                 " Your output should be in the following format: {Title} : {Description} as a JSON"

        response = self.client.chat.completions.create(messages=[{"role": "user", "content": prompt}],
                                                       model=self.text_model,
                                                       response_format={"type": "json_object"}).choices[0].message.content
        logging.info(response)
        data = json.loads(response)

        # Extracting the key and value
        title = list(data.keys())[0]
        description = data[title]
        return title, description


if __name__ == '__main__':
    gpt = OpenAIEmbeddingsClient()
    ans = gpt.get_text(["game of thrones", "witcher"])
    print(ans)
