from django.shortcuts import render
import markdown2
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
    markdown_text = markdown2.markdown(unconverted_html)
    
    if unconverted_html is None:
        return render (request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown_text
        })

