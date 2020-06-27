from django.shortcuts import render


def heat(request, heat_id=None, kart_id=None):
    if heat_id is not None:
        ajax_url = '/heatjs/{}'.format(heat_id)
    else:
        ajax_url = '/heatjs/'
    context = {
            'heat_id': heat_id,
            'ajax_url': ajax_url,
            }
    return render(request, 'live.html', context)
