import re
import random
from rules.psychiatrist_rules_ELIZA import psychobabble
from rules.small_talk_rules_ELIZA import small_talk

reflections = {
    "am": "are",
    "was": "were",
    "i": "you",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "are": "am",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you"
}


# Define a function to generate a response based on the input statement
def respond(statement):
    for pattern, responses in RULES:
        match = re.search(pattern, statement.rstrip(".!"), re.IGNORECASE)
        if match:
            response = random.choice(responses)
            return response.format(*[reflect(g) for g in match.groups()])


# Define a function to reflect the input statement
def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)


# Define a main function to run the chatbot
def chatbot():
    print("ELIZA: Hello. How are you feeling today?")
    while True:
        statement = input("You: ")
        if statement == "quit":
            print("ELIZA: Goodbye. It was nice talking to you!")
            break
        print("ELIZA: " + respond(statement))


# Call the chatbot function
if __name__ == "__main__":
    RULES = psychobabble + small_talk
    chatbot()

# ToDo: just take one part of the sentence, not the whole sentence/ multiple sentences
# Delete questionmarks... in answers
# lowercase von allem v.a. regex
