from django.shortcuts import render


def heat(request, heat_id=None, kart_id=None):
    if heat_id is not None:
        ajax_url = '/livejs/{}'.format(heat_id)
    else:
        ajax_url = '/livejs/'
    context = {
            'heat_id': heat_id,
            'ajax_url': ajax_url,
            'race_lib': 'live.js',
            'timer_lib': 'timer.js',
            }
    return render(request, 'race.html', context)
