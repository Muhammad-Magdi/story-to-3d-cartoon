import helpers.nltk_helper as nltk
import helpers.core_helper as core
import json

#This may be the main function that returns
#the JSON -List of Events- to be used in Graphics Part.
def nlp(raw_input):
    raw_input = core.solve_coref(raw_input)
    print(raw_input)
    raw_input = nltk.clean_data(raw_input)
    print(raw_input)
    raw_input = nltk.replace_actions(raw_input)
    print(raw_input)
    events = []     #list of Events -dicts-
    for event in raw_input.split(','):
        events.append(nltk.event_divider(event))
    return json.dumps(events)

print(nlp("Tom was running in the Street, the Car kicked him"))