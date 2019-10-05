from django.shortcuts import render
import logging


logger = logging.getLogger('console')


def index(request):
    return render(request, 'index.html')