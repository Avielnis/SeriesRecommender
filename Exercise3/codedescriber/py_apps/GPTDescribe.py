from ChatGPTResponse import ChatGPTResponse
import sys

gpt = ChatGPTResponse()

code = sys.argv[1]


messages = [{"role": "user", "content": f"""""this is my code:
{code}

give me a full clear docstring for this code.
remember that when you finish a sentence to put new line
format:

    '''the description here
    :param:
    :return:
give me only the doc string without any further explanations'''
"""}]

resp = gpt.get_response_for(messages)

print(resp)

