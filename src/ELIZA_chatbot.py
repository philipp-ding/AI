import re
import random
import sys
sys.path.append('..')
from rules.psychiatrist_rules_ELIZA import psychobabble
from rules.small_talk_rules_ELIZA import small_talk

# define reflections
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

# define default answers for the user
DEFAULT_ANSWERS = [
    # the structure for all rules stays the same: first comes the keyword, in this case as a regular expression
    [r'(.*)',
     # afterwards the corresponding reassembly rules for the key word
     ["Sorry I don't get it. Can your rephrase this?",
      "You have to explain this deeper for me",
      "Why {0}?"]]]


def find_matching_rule(rules, sub_sentence):
    # iterate over all rules and return the first matching rule
    for pattern, responses in rules:
        # search, if the statement fits a rule, ignore the case
        match = re.search(pattern, sub_sentence, re.IGNORECASE)
        # if matches select a random answer choice fitting the rule and return response
        # else try the next transformation rule
        if match:
            # select random answer choice
            response = random.choice(responses)
            # reflect the question (e.g. I to you) and return response
            return response.format(*[reflect(g) for g in match.groups()])


# Define a function to generate a response based on the input statement
def respond(statement):
    # split user input in (sub-) sentences
    statement_split_on_punctuation = re.findall(r"([^\.\!\?,]+[\.\!\?,]{1}|[^\.\!\?,]+$)", statement)
    # iterate over all parts
    for sub_sentence in statement_split_on_punctuation:
        # try to find rule for one part and continue with the next if nothing found
        response = find_matching_rule(RULES, sub_sentence)
        # return response if one rule matches
        if response is not None:
            return response
    # if no rule matches return default values for the first subsequence of the user input
    return find_matching_rule(DEFAULT_ANSWERS, statement.rstrip(".!"))


# Define a function to reflect the input statement
def reflect(fragment):
    # split all different words in the input part
    tokens = fragment.lower().split()
    # iterate over all input words
    for i, token in enumerate(tokens):
        # proof if one word out of the reflections is included in the user input
        if token in reflections:
            # change input token if one word is included
            tokens[i] = reflections[token]
    # join the reflected statement and return it
    return ' '.join(tokens)


# Define a main function to run the chat bot
def chat_bot():
    # start the conversation
    print("ELIZA: Hello. How are you feeling today?")
    # answer conversation as long as person don't quit via quit or bye
    while True:
        # wait for user input
        statement = input("You: ")
        # say goodbye
        if statement.lower() == "quit" or "bye" in statement.lower():
            print("ELIZA: Goodbye. It was nice talking to you!")
            break
        # response to the user
        print("ELIZA: " + respond(statement))


def respond_external(user_input: str, rules: list = psychobabble + small_talk):
    global RULES
    RULES = rules
    return respond(user_input)


# Call the chat bot function
if __name__ == "__main__":
    # choose constant rules to take
    RULES = psychobabble + small_talk
    # run the chat bot
    chat_bot()
