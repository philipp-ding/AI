import re
import random
import json


list_groups = []


# def reassemble(before_match, after_match, string_match, reassembly_rule, original_rules, position_temp=0,
#                list_match=[]):
#     if reassembly_rule == ":newkey":
#         return None
#     elif reassembly_rule.startswith("="):
#         return find_matching_rule(original_rules, before_match+string_match+after_match,
#                                   keyword_given=reassembly_rule.replace("=", ""))
#     else:
#         matches = re.findall("\$\d", reassembly_rule)
#         if matches:
#             for match in matches:
#                 position = int(re.sub("\$", "", match))
#                 number_of_matches = len(string_match.split())
#                 match_pos_after = 2 if before_match else 1
#                 match_pos_after += position_temp
#                 if position == 1:
#                     reassembly_rule = reassembly_rule.replace(match, before_match)
#                 elif position == number_of_matches + match_pos_after:
#                     reassembly_rule = reassembly_rule.replace(match, after_match)
#                 else:
#                     word_for_str_pos = list_match[position-2]
#                     if word_for_str_pos == "*":
#                         for word in string_match:
#                             word_for_str_pos = string_match.replace(word, "")
#                     reassembly_rule = reassembly_rule.replace(match, word_for_str_pos)
#             return reassembly_rule
#         else:
#             return reassembly_rule
def reassemble(before_match, after_match, string_match, reassembly_rule, original_rules, position_temp=0, list_match=[]):
    """
    Reassembles a string based on input parameters.

    Arguments:
    - before_match: string
        The string before the matched pattern.
    - after_match: string
        The string after the matched pattern.
    - string_match: string
        The matched pattern.
    - reassembly_rule: string
        The rule to reassemble the string.
    - original_rules: dict
        A dictionary of the original rules.
    - position_temp: int
        The position of the matched pattern.
    - list_match: list
        A list of matched words.

    Returns:
    - string: The reassembled string.
    """

    # If the reassembly rule is ":newkey", return None
    if reassembly_rule == ":newkey":
        return None

    # If the reassembly rule starts with "=", find the matching rule
    elif reassembly_rule.startswith("="):
        return find_matching_rule(original_rules, before_match+string_match+after_match, keyword_given=reassembly_rule.replace("=", ""))

    # Otherwise, replace the placeholders in the reassembly rule with the appropriate values
    else:
        # Find all the matches in the reassembly rule
        matches = re.findall("\$\d", reassembly_rule)
        if matches:
            # Replace each match with the appropriate value
            for match in matches:
                # Get the position of the match
                position = int(re.sub("\$", "", match))
                # Get the number of words in the matched pattern
                number_of_matches = len(string_match.split())
                # Calculate the position of the match after the matched pattern
                match_pos_after = 2 if before_match else 1
                match_pos_after += position_temp

                # If the match is the first word in the matched pattern, replace it with the before match
                if position == 1:
                    reassembly_rule = reassembly_rule.replace(match, before_match)

                # If the match is the last word in the matched pattern, replace it with the after match
                elif position == number_of_matches + match_pos_after:
                    reassembly_rule = reassembly_rule.replace(match, after_match)

                # Otherwise, replace it with the appropriate word from the list of matched words
                else:
                    # Get the word for the current position
                    word_for_str_pos = list_match[position-2]

                    # If the word is "*", replace it with all the words in the matched pattern
                    if word_for_str_pos == "*":
                        for word in string_match:
                            word_for_str_pos = string_match.replace(word, "")

                    # Replace the match with the appropriate word
                    reassembly_rule = reassembly_rule.replace(match, word_for_str_pos)

            # Return the reassembled string
            return reassembly_rule

        # If there are no matches, return the reassembly rule as is
        else:
            return reassembly_rule


def apply_groups(fragment: str, groups: dict):
    global list_groups
    # Define a function to reflect the input statement
    tokens = fragment.lower().split()
    # iterate over all input words
    for i, token in enumerate(tokens):
        # proof if one word out of the reflections is included in the user input
        for key, value in groups.items():
            if token in value:
                # change input token if one word is included
                tokens[i] = "@" + key
                list_groups.append(token)
    # join the reflected statement and return it
    return ' '.join(tokens)

def reformat_rule_to_answer(rules: dict, statement: str, original_rules: dict):
    for rule in rules["rules"]:
        rule_regex = rule["decomposition"]
        if rule["decomposition"].startswith("*"):
            rule_regex = rule_regex[2:]
        if rule["decomposition"].endswith("*"):
            rule_regex = rule_regex[:-2]
        if "*" in rule_regex:
            rule_regex = re.sub(" \* ", r".*", rule_regex)
            _position_temp = 3
        else:
            _position_temp = 0
        match = re.search(rule_regex, statement, re.IGNORECASE)
        if match:
            pos_match_start = match.start()
            string_match = match.group(0)
            if _position_temp == 3:
                list_match = string_match.split()
                list_match.insert(1, "*")
            else:
                list_match = []
            pos_match_end = pos_match_start + len(string_match)
            before_match = statement[:pos_match_start]
            after_match = statement[pos_match_end:]

            reassembly_rule = random.choice(rule["reassembly"])
            return reassemble(before_match, after_match, string_match, reassembly_rule, original_rules, _position_temp,
                              list_match)

    return None

def find_matching_rule(rules, sub_sentence, reflections: dict = {}, groups: dict = {}, keyword_given=None):
    list_possible_responses = []
    # iterate over all rules and return the first matching rule
    for rule in rules:
        # search, if the statement fits a rule, ignore the case
        if keyword_given is None:
            for keyword in rule["keyword"]:
                keyword_temp = keyword + " " if not sub_sentence.lower().endswith(keyword) else ""
                keyword_temp = " " + keyword_temp if not sub_sentence.lower().startswith(keyword) else ""
                match = re.search(keyword_temp, sub_sentence, re.IGNORECASE)
                if match:
                    list_possible_responses.append(rule)
        else:
            match = False
            for keyword in rule["keyword"]:
                if keyword_given == keyword:
                    list_possible_responses.append(rule)
        # if matches select a random answer choice fitting the rule and return response
        # else try the next transformation rule
        # if match:
        #     list_possible_responses.append(rule)

    list_possible_responses = sorted(list_possible_responses, key=lambda x: x["precedence"])

    if list_possible_responses:
        sub_sentence = re.sub("[\.\!\?,]", "", sub_sentence)
        # reflect the response
        sub_sentence = reflect(sub_sentence, reflections=reflections)
        sub_sentence = apply_groups(sub_sentence, groups=groups)


        # select random answer choice
        response = reformat_rule_to_answer(list_possible_responses[-1], sub_sentence, rules)
        # reflect the question (e.g. I to you) and return response
        return response # .format(*[reflect(g, reflections=reflections) for g in response])


# Define a function to generate a response based on the input statement
def respond(statement, transformation_rules, default_rules, reflections: dict = {}, groups: dict = {}):
    global list_groups
    # split user input in (sub-) sentences
    statement_split_on_punctuation = re.findall(r"([^\.\!\?,]+[\.\!\?,]{1}|[^\.\!\?,]+$)", statement)
    # iterate over all parts
    for sub_sentence in statement_split_on_punctuation:
        
        # try to find rule for one part and continue with the next if nothing found
        response = find_matching_rule(transformation_rules, sub_sentence, reflections, groups)
        # return response if one rule matches
        if response is not None:
            if list_groups:
                for item in list_groups:
                    response = re.sub(r"@[A-Za-z]*", item, response)
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
    main(run_internal=True)

    # user_input = "test my test mother test"
    # user_input = "Hi ELIZA, I'm cold and feeling not well because my sister isn't here"
    # main(user_input, run_internal=False)
