import collections

OriginalRecipe = collections.namedtuple('OriginalRecipe', 'url id title desc author featured uses favorites code')
Recipe = collections.namedtuple('Recipe', 'url, name, desc, trigger_channel, trigger, action_channel, action, ids')

ActionInstance = collections.namedtuple('ActionInstance', 'id, name, params')
Mapping = collections.namedtuple('Mapping', 'id, action_instances, nl_command_statment')


def recipe_to_mapping(id, recipe):
    action_instances = list()
    action_instances.append(ActionInstance(recipe['ids']['trigger'], None, list()))
    action_instances.append(ActionInstance(recipe['ids']['action'], None, list()))

    return Mapping(id, action_instances, recipe['name'])


def original_recipe_to_recipe(original_recipe, ds):
    if type(original_recipe) == dict:
        url = original_recipe['url']
        name = original_recipe['title']
        desc = original_recipe['desc']
        code = original_recipe['code']
    else:
        url = original_recipe.url
        name = original_recipe.title
        desc = original_recipe.desc
        code = original_recipe.code

    trigger_channel = code['trigger']['name']
    trigger = code['trigger']['func']

    action_channel = code['action']['name']
    action = code['action']['func']

    ids = dict()
    ids['trigger'] = ds.get_action_id(trigger_channel, trigger)
    ids['action'] = ds.get_action_id(action_channel, action)

    if ids['trigger'] is None:
        print('trigger_channel: {} | trigger {}'.format(trigger_channel, trigger))

    if ids['action'] is None:
        print('action_channel: {} | action {}'.format(action_channel, action))

    return Recipe(url, name, desc, trigger_channel, trigger, action_channel, action, ids)
