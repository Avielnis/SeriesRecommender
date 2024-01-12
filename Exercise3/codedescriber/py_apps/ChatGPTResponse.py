from openai import OpenAI
from API_settings import openai_key


def save_message(data, filename):
    with open(filename, 'a') as f:
        f.write(str(data))


class ChatGPTResponse:
    def __init__(self):
        self.client = OpenAI(api_key=openai_key)
        self.full_responses = []
        self.responses_messages = []

    def get_response_for(self, messages):
        response = self.client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo"
        )

        response_message = response.choices[0].message.content
        self.full_responses.append(response)
        self.responses_messages.append(response_message)

        #####################
        save_message({"message": response_message}, 'GPT_msg.txt')
        ######################
        return response_message



# if __name__ == '__main__':
#     content = "You are an expert python developer. " \
#               "Create for me a python program that checks if a number is prime.\n"
#     comments = "Do not write any explanations, just show me the code itself. \n"
#     unittest_content = "Also please include unit tests that check the logic of the program " \
#                        "using 5 different inputs and expected outputs.if all the assert passed" \
#                        " print 'Code creation completed successfully !"
#     gpt = ChatGPTResponse()
#     msg, code = gpt.get_response_for(content + comments + unittest_content)
#
#     GeneratedCodeHandler.run_generated_code()
