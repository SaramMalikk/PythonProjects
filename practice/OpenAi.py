import openai
# https://platform.openai.com/usage/activity  we get api_key fom here
openai.api_key = ("sk-proj-2NC47W1kK6ugTFb5A2YngoAHe-SNschfpf4R4ie3N1T58PaEivIjl3ICGTBcjhTKC3beQdw8yqT3BlbkFJZZwOt"
                  "-xpsJrOAaNxZNA6nRsy1B9rdPuENJUCZc9_jkXJEws_zVxBENbL3_hkYHcYu2I0dRCFoA")


def chat_with_gpt(prompt):
    try:
        gpt_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return gpt_response.choices[0].message["content"].strip()
    except Exception as e:
        return f"An error occurred: {e}"


while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit"]:
        print("Exiting the chat.")
        break
    response = chat_with_gpt(user_input)
    print("OpenAI:", response)


