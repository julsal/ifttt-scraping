import ifttt_scraping.parsing as parsing
import mysl.file_reader as fr


URL = 0
DESC = 1
TRIGGER_CHANNEL = 2
TRIGGER = 3
ACTION_CHANNEL = 4
ACTION = 5


def get_relevant_urls(majority=False, gold=None):

    invalid_types = ['unintelligible', 'missing', 'nonenglish']
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

        for index in [TRIGGER_CHANNEL, TRIGGER, ACTION_CHANNEL, ACTION]:
            label = instance[index].strip().lower()
            if label in invalid_types:
                candidate_urls[url][index - TRIGGER_CHANNEL] -= 1
            else:
                candidate_urls[url][index - TRIGGER_CHANNEL] += 1

        if url in gold:
            gold_tuple = gold[url]
            gold_temp = gold_tuple[-4:]
            inst_temp = instance[TRIGGER_CHANNEL:]

            ok = True
            for i in range(len(gold_temp)-1):
                if gold_temp[i].lower() != inst_temp[i].lower():
                    ok = False
                    break
            if ok:
                candidate_gold[url] += 1
            else:
                candidate_gold[url] -= 1
        else:
            candidate_gold[url] = -7 #file does not exist anymore

    for url, counters in candidate_urls.items():
        include = True
        for count in counters:
            if count <= 0:
                include = False
                break

        if include and candidate_gold[url] > 0:
            result.append(url)

    return result


def run():
    infile = '/home/juliano/Documents/phd/commands/ifttt-recipes/original/recipe_summaries.tsv'
    gold_recipes = parsing.parse_original_file(infile, None)

    urls = get_relevant_urls(majority=True, gold=gold_recipes)
    print(len(urls))

run()