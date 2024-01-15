import json
import logging

from settings import OPENAI_API_KEY
from openai import OpenAI


class OpenAIClient:
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
        prompt = f"""Here is a list of TV series: {','.join(lst)}. Based on this list, 
            output a new TV series that doesn't exist that might be similar.
            Give a short paragraph about the story plot. Your output should be in the following JSON format: 
            "title" : "<Title>", 
            "description" : "<description>"
            """

        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.text_model,
            response_format={"type": "json_object"}
        ).choices[0].message.content

        logging.info(response)
        data = json.loads(response)

        # Extracting the key and value
        title = data["title"]
        description = data["description"]
        description = description.replace('.', '.\n')
        logging.info(f"Got Title : {title} and Description : {description}")
        return title, description

    def get_img(self, title, description):
        prompt = f"poster of a tv show called {title} about {description}"
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        logging.info(f"image url crate for {title} : {description} -> {image_url}")
        return image_url
