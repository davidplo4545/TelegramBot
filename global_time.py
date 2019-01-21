import requests
import json


def get_world_timezone(timezone):
    '''
    Returns the time in the given timezone by
    the shortcut given
    :param timezone:
    :return:
    '''
    timezones_dict = {'PDT': 'PST8PDT',
                      'PST': 'PST8PDT',
                      'UTC': 'Etc/UTC',
                      'CET': 'CET'}

    if timezone.upper() in timezones_dict:
        extension = timezones_dict[timezone.upper()]

    url = 'http://worldtimeapi.org/api/timezone/{}'.format(extension)

    r = requests.get(url)
    json_data = json.loads(r.content.decode('utf-8'))
    full_time = json_data['datetime'].split('T')[1]
    short_time = ':'.join(full_time.split(':')[:2])
    return short_time
