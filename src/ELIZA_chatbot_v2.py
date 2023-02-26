import re
import random
import sys
import json
# sys.path.append('..')

#
# # define default answers for the user
# DEFAULT_ANSWERS = [
#     # the structure for all rules stays the same: first comes the keyword, in this case as a regular expression
#     [r'(.*)',
#      # afterwards the corresponding reassembly rules for the key word
#      ["Sorry I don't get it. Can your rephrase this?",
#       "You have to explain this deeper for me",
#       "Why {0}?"]]]

def reassemble(before_match, after_match, string_match, reassembly_rule, original_rules):
    if reassembly_rule == ":newkey":
        return None
    elif reassembly_rule.startswith("="):
        return find_matching_rule(original_rules, before_match+string_match+after_match)
    else:
        matches = re.findall("\$\d", reassembly_rule)
        if matches:
            for match in matches:
                position = int(re.sub("\$", "", match))
                number_of_matches = len(string_match.split())
                match_pos_after = 2 if before_match else 1
                if position == 1:
                    reassembly_rule = re.replace(match, before_match)
                elif position == number_of_matches + match_pos_after:
                    reassembly_rule = reassembly_rule.replace(match, after_match)
            return reassembly_rule
        else:
            return reassembly_rule


def reformat_rule_to_answer(rules: dict, statement: str, original_rules: dict):
    for rule in rules["rules"]:
        rule_regex = re.sub("\*", r"", rule["decomposition"])
        match = re.search(rule_regex, statement, re.IGNORECASE)
        if match:
            pos_match_start = match.start()
            string_match = match.group(0)
            pos_match_end = pos_match_start + len(string_match)
            before_match = statement[:pos_match_start]
            after_match = statement[pos_match_end:]

            reassembly_rule = random.choice(rule["reassembly"])
            return reassemble(before_match, after_match, string_match, reassembly_rule, original_rules)

    return None

def find_matching_rule(rules, sub_sentence, reflections: dict = {}, groups: dict = {}, keyword=None):
    list_possible_responses = []
    # iterate over all rules and return the first matching rule
    for rule in rules:
        # search, if the statement fits a rule, ignore the case
        if keyword is None:
            for keyword in rule["keyword"]:
                match = re.search(keyword, sub_sentence, re.IGNORECASE)
        else:
            match = re.search(keyword, sub_sentence, re.IGNORECASE)
        # if matches select a random answer choice fitting the rule and return response
        # else try the next transformation rule
        if match:
            list_possible_responses.append(rule)

    list_possible_responses = sorted(list_possible_responses, key=lambda x: x["precedence"])

    if list_possible_responses:
        sub_sentence = re.sub("[\.\!\?,]", "", sub_sentence)
        # reflect the response
        sub_sentence = reflect(sub_sentence, reflections=reflections)

        # select random answer choice
        response = reformat_rule_to_answer(list_possible_responses[-1], sub_sentence, original_rules)
        # reflect the question (e.g. I to you) and return response
        return response # .format(*[reflect(g, reflections=reflections) for g in response])


# Define a function to generate a response based on the input statement
def respond(statement, transformation_rules, default_rules, reflections: dict = {}, groups: dict = {}):
    # split user input in (sub-) sentences
    statement_split_on_punctuation = re.findall(r"([^\.\!\?,]+[\.\!\?,]{1}|[^\.\!\?,]+$)", statement)
    # iterate over all parts
    for sub_sentence in statement_split_on_punctuation:
        
        # try to find rule for one part and continue with the next if nothing found
        response = find_matching_rule(transformation_rules, sub_sentence, reflections)
        # return response if one rule matches
        if response is not None:
            return response

    # if no rule matches return default values for the first subsequence of the user input
    return random.choice(default_rules)



# Define a function to reflect the input statement
def reflect(fragment: str, reflections: dict):
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
def chat_bot(opener_statement: list, transformation_rules: list, default_rules: list, reflections: dict, groups: dict,
             goodbyes: list):
    # start the conversation
    print(start(opener_statement))
    # answer conversation as long as person don't quit via quit or bye
    while True:
        # wait for user input
        statement = input("You: ")
        # say goodbye
        if statement.lower() == "quit" or "bye" in statement.lower():
            print(random.choice(goodbyes))
            break
        # response to the user
        print("ELIZA: " + respond(statement, transformation_rules=transformation_rules, default_rules=default_rules,
                                  reflections=reflections, groups=groups))


def respond_external(user_input: str, transformation_rules: list, default_transformation):
    return main(user_input, run_internal=False)


def start(openers_list):
    return random.choice(openers_list)


def main(user_input: str = "", run_internal: bool = False):
    # choose file with constant rules to take

    with open(r"../rules/doctor.json") as rule_file:
        rules = json.load(rule_file)

    DEFAULT_ANSWERS = rules["default"]
    REFLECTIONS = rules["reflections"]
    GREETINGS = rules["greetings"]
    GROUPS = rules["groups"]
    GOODBYE = rules["goodbyes"]
    KEYWORDS = rules["keywords"]

    if run_internal:
        chat_bot(opener_statement=GREETINGS, transformation_rules=KEYWORDS, default_rules=DEFAULT_ANSWERS,
                 reflections=REFLECTIONS, groups=GROUPS, goodbyes=GOODBYE)

    else:
        print(respond(user_input, transformation_rules=KEYWORDS, default_rules=DEFAULT_ANSWERS,
                reflections=REFLECTIONS, groups=GROUPS))

# Call the chat bot function
if __name__ == "__main__":
    # main(run_internal=True)

    user_input = "test do you remember test"
    main(user_input, run_internal=False)