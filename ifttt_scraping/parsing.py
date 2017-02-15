import simplejson as json
import re

import mysl.file_reader as fr
import ifttt_scraping.types as ist

FILENAME = 0
URL = 1
ID = 2
TITLE = 3
DESC = 4
AUTHOR = 5
FEATURED = 6
USES = 7
FAVORITES = 8
CODE = 9

OPEN = '('
CLOSE = ')'

DOUBLE_QUOTES = '"'

ROOT_IF = '(ROOT (IF) '
THEN = '(THEN) '

TRIGGER = 'TRIGGER'
ACTION = 'ACTION'
FUNC = 'FUNC'
PARAMS = 'PARAMS'
TYPES = [TRIGGER, ACTION]


def _solve_inconsistency(text):
    text = text.replace('(PARAMS(Include))', '(PARAMS(Include(None)))')
    text = text.replace('(PARAMS(Tombinfo))', '(PARAMS(Tombinfo(None)))')
    text = text.replace('(PARAMS(Includi_anche))', '(PARAMS(Includi_anche(None)))')
    text = text.replace('PARAMS(Scenario_identifier)', 'PARAMS(Scenario_identifier(None))')
    text = text.replace('(Select_the_days_of_the_week))))(', '(Select_the_days_of_the_week(None)))))(')
    text = text.replace('(Pick_the_days_of_the_week_here.))))', '(Pick_the_days_of_the_week_here.(None)))))')
    text = text.replace('(Days_of_the_week))))', '(Days_of_the_week(None)))))')
    text = text.replace('(Which_days_of_the_week))))', '(Which_days_of_the_week(None)))))')
    text = text.replace('(And_the_days_of_the_week))))', '(And_the_days_of_the_week(None)))))')
    text = text.replace('(PARAMS(Incluir))', '(PARAMS(Incluir(None)))')
    text = text.replace('(Which_days_of_the_week?))))', '(Which_days_of_the_week?(None)))))')

    text = text.replace('(retweets)(replies)))', '(retweets/replies)))')
    text = text.replace('(__disabled)(', '[__disabled](')

    text = text.replace('(central-california)', '[central-california]')
    text = text.replace('(south-africa)', '[south-africa]')
    text = text.replace('(france)', '[france]')
    text = text.replace('(southern-california)', '[southern-california]')
    text = text.replace('Location(spain)', 'Location[spain]')
    text = text.replace('Location(southeast-brazil)', 'Location[southeast-brazil]')
    text = text.replace('Location(ireland)', 'Location[ireland]')
    text = text.replace('Location(north-island)', 'Location[north-island]')
    text = text.replace('Location(new-south-wales)', 'Location[new-south-wales]')
    text = text.replace('Location(southern-brazil)', 'Location[southern-brazil]')
    text = text.replace('Location(new-england)', 'Location[new-england]')
    text = text.replace('Location(texas)', 'Location[texas]')
    text = text.replace('Location(portugal)', 'Location[portugal]')
    text = text.replace('Location(florida)', 'Location[florida]')
    text = text.replace('Location(florida-gulf)', 'Location[florida-gulf]')
    text = text.replace('Location(southeast)', 'Location[southeast]')
    text = text.replace('Location(taiwan)', 'Location[taiwan]')
    text = text.replace('Location(mid-atlantic)', 'Location[mid-atlantic]')
    text = text.replace('Location(morocco)', 'Location[morocco]')
    text = text.replace('Location(el-salvador)', 'Location[el-salvador]')

    text = text.replace('Team(ita.1)(', 'Team("ita.1)(')
    text = text.replace('|ita.1&quot;}', '|ita.1&quot;}"')

    text = text.replace('Team(esp.1)(', 'Team("esp.1)(')
    text = text.replace('|esp.1&quot;}', '|esp.1&quot;}"')

    text = text.replace('Team(eng.1)(', 'Team("eng.1)(')
    text = text.replace('|eng.1&quot;}', '|eng.1&quot;}"')

    text = text.replace('(ger.1)("{&quot;', '("ger.1)({&quot;')
    text = text.replace('(nhl)("{&quot;', '("nhl)({&quot;')
    text = text.replace('(ncaambb)("{&quot;', '("ncaambb)({&quot;')
    text = text.replace('(nfl)("{&quot;', '("nfl)({&quot;')
    text = text.replace('(nba)("{&quot;', '("nba)({&quot;')
    text = text.replace('(mlb)("{&quot;', '("mlb)({&quot;')
    text = text.replace('(victoria)("{&quot;', '("victoria)({&quot;')
    text = text.replace('(northern-california)("{&quot;', '("northern-california)({&quot;')
    text = text.replace('(wnba)("{&quot;', '("wnba)({&quot;')
    text = text.replace('(nhl)("{&quot;', '("nhl)({&quot;')
    text = text.replace('(nhl)("{&quot;', '("nhl)({&quot;')
    text = text.replace('(nhl)("{&quot;', '("nhl)({&quot;')

    text = text.replace('(Team(mlb)("', '(Team("mlb)(')
    text = text.replace('Team(ncaambb)("', 'Team("ncaambb)(')
    text = text.replace('Team(nfl)("', 'Team("nfl)(')
    text = text.replace('Team(nba)("', 'Team("nba)(')
    text = text.replace('Team(ncaawbb)("', 'Team("ncaawbb)(')
    text = text.replace('team(ncaawbb)("', 'team("ncaawbb)(')
    text = text.replace('Team(mls)("', 'Team("mls)(')
    text = text.replace('Team(nhl)("', 'Team("nhl)(')
    text = text.replace('Team(ncaaf)("', 'Team("ncaaf)(')
    text = text.replace('team(nba)("', 'team("nba)(')
    text = text.replace('team(mlb)("', 'team("mlb)(')
    text = text.replace('team?(nba)("', 'team?("nba)(')
    text = text.replace('Tide(ncaaf)("', 'Tide("ncaaf)(')
    text = text.replace('team:(nfl)("', 'team:("nfl)(')
    text = text.replace('Bruins(nhl)("', 'Bruins("nhl)(')
    text = text.replace('Blue_Jays(mlb)("', 'Blue_Jays("mlb)(')
    text = text.replace('team(nfl)("', 'team("nfl)(')
    text = text.replace('Newcastle_United(nfl)("', 'Newcastle_United("nfl)(')
    text = text.replace('Sounders(mls)("', 'Sounders("mls)(')
    text = text.replace('Seahawks(nfl)("', 'Seahawks("nfl)(')
    text = text.replace('Rebels(ncaambb)("', 'Rebels("ncaambb)(')
    text = text.replace('spot:(morocco)("', 'spot:("morocco)(')
    text = text.replace('spot:(barbados)("', 'spot:("barbados)(')
    text = text.replace('location(morocco)("', 'location("morocco)(')
    text = text.replace('team!(nfl)("', 'team!("nfl)(')

    text = text.replace('Football(ncaaf)', 'Football[ncaaf]')
    text = text.replace('here:(nba)("', 'here:("nba)(')
    text = text.replace('Astros(mlb)("', 'Astros("mlb)(')
    text = text.replace('team?(nfl)("', 'team?("nfl)(')
    text = text.replace('(nfl)("', '("nfl)(')


    solver = dict()
    key = '(TRIGGER(Date_&_Time)(FUNC(Every_day_of_the_week_at)(PARAMS(Time_of_day(07:30))(Days_of_the_week))))(ACTION(SMS)(FUNC(Send_me_an_SMS)(PARAMS(Message("Street Sweepers are coming!")))))'
    value = '(TRIGGER(Date_&_Time)(FUNC(Every_day_of_the_week_at)(PARAMS(Time_of_day(07:30))(Days_of_the_week(None)))))(ACTION(SMS)(FUNC(Send_me_an_SMS)(PARAMS(Message("Street Sweepers are coming!")))))'
    solver[key] = value

    key = '(TRIGGER(Date_&_Time)(FUNC(Every_day_of_the_week_at)(PARAMS(Time_of_day(12:00))(Days_of_the_week))))(ACTION(Campfire)(FUNC(Post_a_message)(PARAMS(Which_room?(""))(Message("Hark! I have something to say...")))))'
    value = '(TRIGGER(Date_&_Time)(FUNC(Every_day_of_the_week_at)(PARAMS(Time_of_day(12:00))(Days_of_the_week(None)))))(ACTION(Campfire)(FUNC(Post_a_message)(PARAMS(Which_room?(""))(Message("Hark! I have something to say...")))))'
    solver[key] = value

    #if '"{\\"lat\\"' in text or 'aviso@servipag.com' in text:
    text = text.replace('\\"', '')

    solver[key] = value

    return solver[text] if text in solver else text

def _simplify_7_days(text, fixed):
    regex = "(.*)({})(\([0-9]+\))(\([0-9]+\))(\([0-9]+\))(\([0-9]+\))(\([0-9]+\))(\([0-9]+\))(\([0-9]+\))(.*)".format(fixed)
    m = re.match(regex, text)

    if m is not None and len(m.groups()) == 10:
        new_text = list()
        new_text.append(m.group(1)) #previous data
        new_text.append(m.group(2)) # fixed
        new_text.append(m.group(3)[:-1])
        new_text.append('-')
        new_text.append(m.group(4)[1:-1])
        new_text.append('-')
        new_text.append(m.group(5)[1:-1])
        new_text.append('-')
        new_text.append(m.group(6)[1:-1])
        new_text.append('-')
        new_text.append(m.group(7)[1:-1])
        new_text.append('-')
        new_text.append(m.group(8)[1:-1])
        new_text.append('-')
        new_text.append(m.group(9)[1:]) # minutes
        new_text.append(m.group(10)) # end of the sentence

        return ''.join(new_text)

    return text

def _simplify_6_days(text, fixed):
    regex = "(.*)({})(\([0-9]+\))(\([0-9]+\))(\([0-9]+\))(\([0-9]+\))(\([0-9]+\))(\([0-9]+\))(.*)".format(fixed)
    m = re.match(regex, text)

    if m is not None and len(m.groups()) == 9:
        new_text = list()
        new_text.append(m.group(1)) #previous data
        new_text.append(m.group(2)) # fixed
        new_text.append(m.group(3)[:-1])
        new_text.append('-')
        new_text.append(m.group(4)[1:-1])
        new_text.append('-')
        new_text.append(m.group(5)[1:-1])
        new_text.append('-')
        new_text.append(m.group(6)[1:-1])
        new_text.append('-')
        new_text.append(m.group(7)[1:-1])
        new_text.append('-')
        new_text.append(m.group(8)[1:]) # minutes
        new_text.append(m.group(9)) # end of the sentence

        return ''.join(new_text)

    return text


def _simplify_5_days(text, fixed):
    regex = "(.*)({})(\([0-9]+\))(\([0-9]+\))(\([0-9]+\))(\([0-9]+\))(\([0-9]+\))(.*)".format(fixed)
    m = re.match(regex, text)

    if m is not None and len(m.groups()) == 8:
        new_text = list()
        new_text.append(m.group(1)) #previous data
        new_text.append(m.group(2)) # fixed
        new_text.append(m.group(3)[:-1])
        new_text.append('-')
        new_text.append(m.group(4)[1:-1])
        new_text.append('-')
        new_text.append(m.group(5)[1:-1])
        new_text.append('-')
        new_text.append(m.group(6)[1:-1])
        new_text.append('-')
        new_text.append(m.group(7)[1:]) # minutes
        new_text.append(m.group(8)) # end of the sentence

        return ''.join(new_text)

    return text


def _simplify_4_days(text, fixed):
    regex = "(.*)({})(\([0-9]+\))(\([0-9]+\))(\([0-9]+\))(\([0-9]+\))(.*)".format(fixed)
    m = re.match(regex, text)

    if m is not None and len(m.groups()) == 7:
        new_text = list()
        new_text.append(m.group(1)) #previous data
        new_text.append(m.group(2)) # fixed
        new_text.append(m.group(3)[:-1])
        new_text.append('-')
        new_text.append(m.group(4)[1:-1])
        new_text.append('-')
        new_text.append(m.group(5)[1:-1])
        new_text.append('-')
        new_text.append(m.group(6)[1:]) # minutes
        new_text.append(m.group(7)) # end of the sentence

        return ''.join(new_text)

    return text


def _simplify_3_days(text, fixed):
    regex = "(.*)({})(\([0-9]+\))(\([0-9]+\))(\([0-9]+\))(.*)".format(fixed)
    m = re.match(regex, text)

    if m is not None and len(m.groups()) == 6:
        new_text = list()
        new_text.append(m.group(1)) #previous data
        new_text.append(m.group(2)) # fixed
        new_text.append(m.group(3)[:-1])
        new_text.append('-')
        new_text.append(m.group(4)[1:-1])
        new_text.append('-')
        new_text.append(m.group(5)[1:]) # minutes
        new_text.append(m.group(6)) # end of the sentence

        return ''.join(new_text)

    return text


def _simplify_2_days(text, fixed):
    regex = "(.*)({})(\([0-9]+\))(\([0-9]+\))(.*)".format(fixed)
    m = re.match(regex, text)

    if m is not None and len(m.groups()) == 5:
        new_text = list()
        new_text.append(m.group(1)) #previous data
        new_text.append(m.group(2)) # fixed
        new_text.append(m.group(3)[:-1]) # hour
        new_text.append('-')
        new_text.append(m.group(4)[1:]) # minutes
        new_text.append(m.group(5)) # end of the sentence

        return ''.join(new_text)

    return text


def _simplify_time(text, fixed):

    regex = "(.*)({})(\([0-9]+\))(\(:\))(\([0-9]+\))(.*)".format(fixed)
    m = re.match(regex, text)

    if m is not None and len(m.groups()) == 6:
        new_text = list()
        new_text.append(m.group(1)) #previous data
        new_text.append(m.group(2)) # fixed
        new_text.append(m.group(3)[:-1]) # hour
        new_text.append(m.group(4)[1:-1]) # colon
        new_text.append(m.group(5)[1:]) # minutes
        new_text.append(m.group(6)) # end of the sentence

        return ''.join(new_text)

    return text


def _simplify_data_time(text, fixed):

    regex = "(.*)({})(\([0-9]+\))(\([0-9]+\))(\(\—\))(\([0-9]+\))(\(:\))(\([0-9]+\))(.*)".format(fixed)
    m = re.match(regex, text)

    if m is not None and len(m.groups()) == 9:
        new_text = list()
        new_text.append(m.group(1))
        new_text.append(m.group(2))
        new_text.append(m.group(3)[:-1])
        new_text.append('/')
        new_text.append(m.group(4)[1:-1])
        new_text.append(m.group(5)[1:-1])
        new_text.append(m.group(6)[1:-1])
        new_text.append(m.group(7)[1:-1])
        new_text.append(m.group(8)[1:])
        new_text.append(m.group(9))

        return ''.join(new_text)

    return text


def _simplify(text):

    for fixed in ['Days_of_the_week', 'Uncheck_fasting_days']:
        text = _simplify_7_days(text, fixed)
        text = _simplify_6_days(text, fixed)
        text = _simplify_5_days(text, fixed)
        text = _simplify_4_days(text, fixed)
        text = _simplify_3_days(text, fixed)
        text = _simplify_2_days(text, fixed)

    text = _simplify_time(text, 'Time_of_day')
    text = _simplify_time(text, 'Select_the_time_of_day')
    text = _simplify_time(text, 'What_time_of_day_do_you_want_to_be_reminded\?')
    text = _simplify_time(text, 'Pick_a_time_of_day')
    text = _simplify_time(text, 'Pick_the_time_of_day')
    text = _simplify_time(text, 'What_time_of_day\?')

    text = _simplify_data_time(text, 'Date_and_time')
    text = _simplify_data_time(text, 'The_date_and_time_to_send_the_message')
    text = _simplify_data_time(text, 'The_timing')
    text = _simplify_data_time(text, 'What_time_is_a_good_time_to_call\?')
    text = _simplify_data_time(text, 'Your_Birthday')
    text = _simplify_data_time(text, 'When_did_you_first_see_the_light_of_day\?')
    text = _simplify_data_time(text, 'Date_and_time_one_week_before')
    text = _simplify_data_time(text, 'Дата_и_время')
    text = _simplify_data_time(text, 'The_25th_of_May')
    text = _simplify_data_time(text, 'When_is_your_birthday\?')
    text = _simplify_data_time(text, 'Set_to_his/her_birthday_@_midnight')
    text = _simplify_data_time(text, 'Your_birthday:')
    text = _simplify_data_time(text, 'Birthday')
    text = _simplify_data_time(text, '9:30')
    text = _simplify_data_time(text, 'Date_&amp;_Time')

    return text


def _preprocess(text):
    if text.startswith(ROOT_IF):
        text = text.replace(ROOT_IF, OPEN, 1)

        if THEN in text:
            text = text.replace(THEN, '', 1)
            if THEN in text:
                print("Error: more than one 'then' - {}".format(text))
        else:
            print("Error: no 'then' - {}".format(text))
    else:
        print("Error: invalid INITIAL_PART - {}".format(text))

    text = text.replace('( ', '(').replace(' (', '(').replace(' )', ')').replace(') ', ')')[1:-1]
    text = _simplify(text)
    text = _solve_inconsistency(text)
    return text


def _tokenizer(text):
    tokens = list()
    token = ''

    into_string = False
    for c in text:
        if c == DOUBLE_QUOTES:
            into_string = not into_string
        elif not into_string and (c in [OPEN, CLOSE]):
            if len(token) > 0:
                tokens.append(token)
                token = ''
            tokens.append(c)
        else:
            token += c
    if len(token) > 0:
        tokens.append(token)


    return tokens


def _parse_code(text):
    text = _preprocess(text)
    #print('Preprocessed "{}"...'.format(text))
    code = dict()

    reading_params = False
    tokens = _tokenizer(text)
    stack = list()

    content = list()
    params = list()
    params_dict = dict()

    call = dict()

    for token in tokens:
        if token != CLOSE:
            stack.append(token)
            if token == PARAMS:
                reading_params = True
        else:
            chunk = list()
            while stack[-1] != OPEN:
                chunk.append(stack.pop())
            stack.pop()

            #in the case of empty params.
            if len(chunk) == 0:
                chunk.append('None')

            if len(chunk) == 1:
                if chunk[0] == PARAMS:
                    while len(params) > 0:
                        key = params.pop()
                        value = params.pop()
                        params_dict[key] = value
                    reading_params = False

                elif chunk[0] == FUNC:
                    call[FUNC.lower()] = content.pop()
                    call['params'] = params_dict
                    params_dict = dict()

                elif chunk[0] in TYPES:
                    call['name'] = content.pop()
                    code[chunk[0].lower()] = call

                    params_dict = dict()
                    call = dict()

                elif not reading_params:
                    content.append(chunk[0])
                else:
                    params.append(chunk[0])
            else:
                print("Error: invalid format {}".format(text))

    return code


def parse_original_file(infile, outfile):
    recipes = list()

    tuples = fr.line_to_tuple_in_list(infile, separator='\t', ignore_headline=True)

    for i, t in enumerate(tuples):
        if (i%1000) == 0 or i == len(tuples) - 1:
            print('Processing tuple {} out of {}...'.format(i+1, len(tuples)))

        code = _parse_code(t[CODE])
        url = t[URL]
        recipe = ist.OriginalRecipe(url, int(t[ID]), t[TITLE], t[DESC], t[AUTHOR], t[FEATURED], t[USES], t[FAVORITES], code)
        recipes.append(recipe)

    if outfile is not None:
        with open(outfile, 'w') as f:
            json.dump(recipes, f)
    else:
        recipes_dict = dict()
        for recipe in recipes:
            recipes_dict[recipe.url] = recipe
        return recipes_dict


def run():
    infile = '/home/juliano/Documents/phd/commands/ifttt-recipes/original/recipe_summaries.tsv'
    outfile = '/home/juliano/Documents/phd/commands/ifttt-recipes/mine.json'
    parse_original_file(infile, outfile)

#run()
