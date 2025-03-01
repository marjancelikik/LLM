import streamlit as st
import openai
import pydantic

api_key = "..."
client = openai.OpenAI(api_key = api_key)

completion_prompt = 'Vervollständige den folgenden Satz. Gibt 3 alternative Ergänzungen. Keine Erklärungen hinzufügen: "{0}"...'
artcile_prompt = 'Gib nur den Artikel des folgenden Substantivs an "{0}". Keine Erklärungen hinzufügen.'
correction_prompt = 'Korrigiere das Deutsche im Text "{0}". Keine Erklärungen hinzufügen.'
translation_prompt = 'Translate the following text to german if it is in english and english if it is in german. Do not output additional text: "{0}"'



command_dict = {
    'Correction': correction_prompt,
    'Article': artcile_prompt,
    'Completion': completion_prompt,
    'Translation': translation_prompt,
}

# Set up the OpenAI API key
st.set_page_config(page_title="Basic German Grammar Correction App", layout="centered")
st.title("Basic German Grammar Correction App")

# Radio buttons
operation = st.radio(
    "What operation to perform?",
    ("Correction", "Article", "Completion", "Translation")
)

# Prompt input and settings
st.subheader("Query Settings")
input_string = st.text_area("Enter your prompt:", placeholder="Type your prompt here...")
temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.1)
model = st.text_area("What OpenAI LLM to use:", value="gpt-4o-mini")


def query_chatgpt(prompt, temperature=1.2, max_tokens=500, model="gpt-3.5-turbo"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        seed=0,
        # n=3,
        temperature=temperature,
        logprobs=False
    )
    return completion


# Submit button
if st.button("Generate Response"):
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar!")
    elif not input_string.strip():
        st.error("Please enter a prompt to query!")
    else:
        try:
            # Configure OpenAI API key
            openai.api_key = api_key

            client = openai.OpenAI(api_key=api_key)

            # Query OpenAI Completion API
            with st.spinner("Generating response..."):

                try:
                    prompt = command_dict[operation]
                    prompt = prompt.format(input_string)

                    response = query_chatgpt(
                        prompt=prompt,
                        temperature=temperature,
                        model=model,
                    )

                    final_response = ""
                    if len(response.choices) == 1:
                        final_response = response.choices[0].message.content
                    else:
                        for i, completion in enumerate(response.choices):
                            final_response += 'f"Output {i + 1}: {completion.message.content}"'
                except Exception as e:
                    st.error(f"An error occurred: {e}")

            st.text_area("AI Response:", value=final_response.strip(), height=200)
        except Exception as e:
            st.error(f"Error: {e}")

# Footer
# st.markdown(
#     """
#     ---
#     **Note**: This app requires an active OpenAI API key to work.
#     """
# )