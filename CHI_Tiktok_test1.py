import openai
import getpass

# Asking user to input the API key without echoing it on the screen.

#api_key = getpass.getpass("Please enter your OpenAI API key:")

openai.api_key = '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'

text = input("Please enter the text you want to check: ")

chat_prompt =   'Determine if the statement above contains any misinformation. In the part one, the results are first displayed in the first line, \'May contain misinformation\', \'Cannot be recognized at this time\' or \'No misinformation detected\'. In the part two, an operation is performed to extract keywords from the input text, providing up to six keywords, sorted in order of criticality. In the part three, briefly summarize the reasons for determining whether it contains misinformation. Three reasons of no more than 50 words each are required. Add line breaks between each section. Regardless of the state of the text given, it must be answered in the format given above.'

def call_gpt_model(prompt):
    response = openai.ChatCompletion.create(
      model="gpt-4",
                            
      messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": text}
    ])

    return response.choices[0].message['content']

answer = call_gpt_model(chat_prompt)

print(answer)

input('\nPress any key to exit')