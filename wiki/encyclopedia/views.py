from urllib import request

from django.shortcuts import render, redirect
import markdown2, random
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entries = util.list_entries()   

    for entry in entries:
        if entry.lower() == title.lower():
            title = entry
            break  

    unconverted_html = util.get_entry(title)
    
    if unconverted_html is None:
        return render (request, "encyclopedia/error.html")

    markdown_text = markdown2.markdown(unconverted_html)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown_text
    })

def search(request):
    query = request.GET.get('q', '').strip()
    entries = util.list_entries()   

    for entry in entries:
        if query.lower() == entry.lower():
            return redirect('entry', title=entry)
        
    results = [] 
    for entry in entries:
        if query.lower() in entry.lower():
            results.append(entry)   

    return render(request, 'encyclopedia/search.html', {
        "query": query,
        "results": results
    })

def create(request):
    if request.method == 'POST':
        title = request.POST.get('title').strip()
        content = request.POST.get('content').strip()

        if util.get_entry(title) is not None:
            return render(request, 'encyclopedia/create.html', {
                "error_message": "An entry with this title already exists.",
                "title": title,
                "content": content
            })

        util.save_entry(title, content)
        return redirect('entry', title=title)
    return render(request, 'encyclopedia/create.html')

def edit(request, title):
    if request.method == 'POST':
        updated_content = request.POST.get('content').strip()
        util.save_entry(title, updated_content)
        return redirect('entry', title=title)
    else:
        content = util.get_entry(title)
        return render(request, 'encyclopedia/edit.html', {
            "title": title,
            "content": content
        })
    
def random_entry(request):
    entries = util.list_entries()
    random_entry = random   .choice(entries)
    return redirect('entry', title=random_entry)    