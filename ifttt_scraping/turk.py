import simplejson as json

import mysl.file_reader as fr

import ifttt_scraping.types as ist
import ifttt_scraping.parsing as parsing
import ifttt_scraping.semeval as semeval


URL = 0
DESC = 1
TRIGGER_CHANNEL = 2
TRIGGER = 3
ACTION_CHANNEL = 4
ACTION = 5
IDS = 6


def get_relevant_urls(majority=False, gold=None):
    invalid_types = [] if majority else ['unintelligible', 'missing', 'nonenglish']
    candidate_urls = dict()
    candidate_gold = dict()

    turk_file = '/home/juliano/git/ifttt-quirk/data/turk_public.tsv'
    tuples = fr.line_to_tuple_in_list(turk_file, '\t', ignore_headline=True)
    result = list()

    for instance in tuples:
        url = instance[URL].strip()

        if url not in candidate_urls:
            candidate_urls[url] = [0, 0, 0, 0]
            candidate_gold[url] = 0

#        if url == 'https://ifttt.com/recipes/119595-when-man-united-game-starts-turn-lights-red':
#            print('aqui')

        for index in [TRIGGER_CHANNEL, TRIGGER, ACTION_CHANNEL, ACTION]:
            label = instance[index].strip().lower()
            if label in invalid_types:
                candidate_urls[url][index - TRIGGER_CHANNEL] -= 1
            else:
                candidate_urls[url][index - TRIGGER_CHANNEL] += 1

        if gold is not None:
            if url in gold:
                gold_tuple = gold[url]
                gold_temp = [gold_tuple['trigger_channel'], gold_tuple['trigger'],
                             gold_tuple['action_channel'], gold_tuple['action']]

                inst_temp = instance[TRIGGER_CHANNEL:ACTION]

                ok = True
                for i in range(len(gold_temp)-1):
                    if gold_temp[i].lower() != inst_temp[i].lower().replace(' ', '_'):
                        ok = False
                        break
                if ok:
                    candidate_gold[url] += 1
                else:
                    candidate_gold[url] -= 1
            else:
                candidate_gold[url] = -7 #file does not exist anymore
        else:
            candidate_gold[url] += 1 # in the case that gold is not provided, get all.

    for url, counters in candidate_urls.items():
        include = True
        for count in counters:
            if count <= 0:
                include = False
                break

        if include and candidate_gold[url] > 0:
            result.append(url)
            #print(gold[url])

    return result


def save_relevant_urls():
    org_file = '/home/juliano/Documents/phd/commands/ifttt-recipes/original/recipe_summaries.tsv'
    outfile = '/home/juliano/Documents/phd/commands/ifttt-recipes/all_relevant.json'

    action_kb_file = '/home/juliano/git/end-user/end-user-common/src/main/resources/dataset/simple/actionkb.json'
    ds = semeval.SemEvalDataSet(action_kb_file)

    original_recipes = parsing.parse_original_file(org_file, None)
    urls = get_relevant_urls()

    all = dict()
    for url in urls:
        all[url] = ist.original_recipe_to_recipe(original_recipes[url], ds)

    with open(outfile, 'w') as f:
        json.dump(all, f)


def run():
    infile = '/home/juliano/Documents/phd/commands/ifttt-recipes/all_relevant.json'
    outfile = '/home/juliano/git/end-user/end-user-common/src/main/resources/dataset/simple/quirk_mapping.json'
    with open(infile) as f:
        gold = json.load(f)

    urls = get_relevant_urls(majority=False, gold=gold)

    mappings = list()
    id = 99000
    for url in urls:
        recipe = gold[url]
        mapping = ist.recipe_to_mapping(id, recipe)
        mappings.append(mapping)
        id += 1

    with open(outfile, 'w') as f:
        json.dump(mappings, f)

    print('Total {}'.format(len(urls)))

run()