import openai

client = openai.OpenAI(api_key="...")

completion_prompt = 'Vervollständige den folgenden Satz. Gibt 3 alternative Ergänzungen. Keine Erklärungen hinzufügen. "{0}"...'
artcile_prompt = 'Gib nur den Artikel des folgenden Substantivs an "{0}"'
correction_prompt = 'Korrigiere das Deutsche im Text "{0}"'

command_dict = {
    'cor': correction_prompt,
    'art': artcile_prompt,
    'a': artcile_prompt,
    'com': completion_prompt
}


# TODO: Add stream lit UI on top of this 

def query_chatgpt(prompt):
    completion = client.chat.completions.create(
        # model="gpt-4-turbo",
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        seed=0,
        # n=3,
        # temperature=1.2,
        # max_tokens=5,
        logprobs=False
    )

    if len(response.choices) == 1:
        print(response.choices[0].message.content)
    else:
        return [completion.message.content for _ in response.choices]

    return response


while True:
    input_string = input(": ")

    try:
        ws_pos = input_string.find(' ')
        command = input_string[:ws_pos]
        input_string = input_string[ws_pos + 1:]

        prompt = command_dict[command]
        prompt = prompt.format(input_string)

        response = query_chatgpt(prompt)

        if len(response.choices) == 1:
            print(response.choices[0].message.content)
        else:
            for i, completion in enumerate(response.choices):
                print(f"Output {i + 1}: {completion.message.content}")
    except Exception as e:
        print(f"An error occurred: {e}")



