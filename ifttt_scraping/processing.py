import os
from bs4 import BeautifulSoup

import mysl.file_reader as fr
import ifttt_scraping.types as ist


def parse_recipes(basedir, files):
    recipes = list()

    for file in files:
        print('Processing file "{}"'.format(file))
        with open(os.path.join(basedir, file)) as f:
            soup = BeautifulSoup(f, 'lxml')
            card = soup.body.main.find('div', id='card') if soup.body.main is not None else None
            if card is not None:
                div = card.find('div', class_='card-container').find('div', class_='full-applet-card') # never_enabled_for_user
                basic_data = div.find('div', class_='applet-content')
                name = basic_data.find('h1', class_='applet-name').getText().replace('\n', ' ')
                desc = basic_data.find('p', class_='applet-description').getText().replace('\n', ' ')

                recipe_div = div.find('div', class_='permissions-meta').ul
                parts = recipe_div.find_all('li', recursive=False)

                if len(parts) == 2:
                    trigger_channel = parts[0].find('h5').getText()
                    trigger = parts[0].find('span').getText()

                    action_channel = parts[1].find('h5').getText()
                    action = parts[1].find('span').getText()

                    recipes.append(ist.Recipe(file, name, desc, trigger_channel, trigger, action_channel, action))

                else:
                    print('Error: {}', file)
            else:
                print('Error: no card into "{}".'.format(file))
    return recipes


def run():
    outfile = '/home/juliano/Documents/phd/commands/ifttt-recipes/content.tsv'
    basedir = '/home/juliano/Documents/phd/commands/ifttt-recipes/relevant'
    files = os.listdir(basedir)
    #files = scraping.get_relevant_urls(strict=True)
    #files = [f.replace("https://ifttt.com/recipes/", "") for f in files]

    print('# of files: {}'.format(str(len(files))))

    recipes = parse_recipes(basedir, files)
    fr.write_tupla_per_line(outfile, recipes, separator='\t',
                    headline=ist.Recipe('#URL', 'NAME', 'DESC', 'TRIGGER_CHANNEL', 'TRIGGER', 'ACTION_CHANNEL', 'ACTION'))

#run()