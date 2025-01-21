import json
from difflib import get_close_matches


def load_knowledge_file(file_path: str) -> dict:  # load the knowledge file from json into the program to match ans
    # "->"denotes the return type of function
    with open(file_path, 'r') as file:  # 'r' means "read mode," so it opens the file for reading.
        data = json.load(file)
    return data


def save_response(file_path: str, data: dict):
    with open(file_path, 'w') as file:   # "w" means in write mode
        json.dump(data, file, indent=2)  # to insert the data in json file


def find_best_answer(user_question: str, questions: list) -> str or None:
    # "cutoff = 0.6" means if the answer is 60 percent matched it will return the response otherwise it will return None
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.7)
    # "n=1" means it will return 1 matched answer if we write 2 it will return top 2 matched answer
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge: dict) -> str or None:
    for q in knowledge['questions']:
        if q['question'] == question:
            return q['answer']


def chatbot():
    knowledge = load_knowledge_file('knowledge.json')
    while True:
        user_input = str(input("You: "))
        if user_input.lower() == 'skip':
            break
        elif user_input == "":
            print("Bot: It seems you didn't type anything. How can I help you?")
            continue  # it skips the rest of code and start the function again

        best_match: dict or None = find_best_answer(user_input, [q['question'] for q in knowledge['questions']])
        # this will match and get the best answer form knowledge file
        if best_match:
            answer = get_answer_for_question(best_match, knowledge)
            print(f"Bot: {answer}")
        else:
            print("Sorry! I don't know the answer Can you please teach me.")
            new_answer = input("Type the answer please or 'skip' to exit: ")
            if new_answer.lower() == 'skip':
                break
            elif new_answer.lower() != 'skip':
                knowledge['questions'].append({"question": user_input, "answer": new_answer})
                save_response('knowledge.json', knowledge)
                print('Thankyou! I learned a new response.')


if __name__ == "__main__":
    chatbot()
