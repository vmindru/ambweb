from django.shortcuts import render


def control(request, heat_id=None):
    context = {}
    return render(request, 'control.html', context)
