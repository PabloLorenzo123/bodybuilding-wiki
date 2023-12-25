from flask import request, redirect, url_for, render_template, flash, abort
from . import search
from .search_json import create_table


@search.route('/', methods=['GET', 'POST'])
def search_results():
    q = request.args.get('q')
    if not q:
        flash('You need to type something in the search bar.')
        return
    else:
        results = create_table(q)
        
        return render_template('search/results.html', results=results)