from django.shortcuts import render


def heat_refresh(request, heat_id=None):
    if heat_id is not None:
        ajax_url = '/heatjs/{}'.format(heat_id)
    else:
        ajax_url = '/heatjs/'
    data_header = ['Position', 'Kart', 'Laps', 'Lap Time', 'Raced Time', 'Diff', 'Gap', 'Best Lap Time', 'Best Lap']
    context = {
            'data_header': data_header,
            'heat_id': heat_id,
            'ajax_url': ajax_url,
            }
    return render(request, 'ref.html', context)
