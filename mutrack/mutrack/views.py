"""
views.py

Top-level views module for the site.
"""

from django.shortcuts import render

def index(request):
    """Index view for the whole site.
    """
    return render(request, 'index.html')
