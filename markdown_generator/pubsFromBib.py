#!/usr/bin/env python
# coding: utf-8

# # Publications markdown generator for academicpages
# 
# Takes a set of bibtex of publications and converts them for use with [academicpages.github.io](academicpages.github.io). This is an interactive Jupyter notebook ([see more info here](http://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/what_is_jupyter.html)). 
# 
# The core python code is also in `pubsFromBibs.py`. 
# Run either from the `markdown_generator` folder after replacing updating the publist dictionary with:
# * bib file names
# * specific venue keys based on your bib file preferences
# * any specific pre-text for specific files
# * Collection Name (future feature)


from pybtex.database.input import bibtex
import pybtex.database.input.bibtex 
from time import strptime
import string
import html
import os
import re

bibfile = "publications.bib"
base_path = "https://danavanaken.com"
website_owner = "Dana Van Aken"

def clean_text(s_):
    return s_.replace("{", "").replace("}","").replace("\\","")

def html_escape(s_):
    """Produce entities within text."""
    html_escape_table_ = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
    }
    return "".join(html_escape_table_.get(c_,c_) for c_ in s_)


parser = bibtex.Parser()
bibdata = parser.parse_file(bibfile)

#loop through the individual references in a given bibtex file
for bib_id, entry in bibdata.entries.items():
    b = entry.fields

    pub_year = f"{b['year']}"
    pub_date = f"{pub_year}-01-01"
    
    #strip out {} as needed (some bibtex entries that maintain formatting)
    title = clean_text(b["title"])

    url_slug = title.replace(" ","-")    
    url_slug = re.sub("\\[.*\\]|[^a-zA-Z0-9_-]", "", url_slug)
    url_slug = url_slug.replace("--","-")

    base_filename = (f"{pub_year}-{url_slug}").replace("--", "-")
    #base_filename = clean_text(f"/files/{bib_id}")
    #base_filename = re.sub("\\[.*\\]|[^a-zA-Z0-9_-]", "", base_filename)
    md_filename = f"{base_filename}.md"

    permalink = clean_text(f"/files/{bib_id}.pdf")
    url = f"{base_path}{permalink}"
    title = html_escape(title)
    venue = html_escape(clean_text(b["booktitle"]))

    #citation authors - todo - add highlighting for primary author?
    authors = []
    for author in entry.persons["author"]:
        name = " ".join(author.first_names + author.middle_names + \
            author.last_names) 
        if name == website_owner:
            name = f"<strong>{name}</strong>"
        authors.append(name)
    authors = ", ".join(authors)

    #Build Citation from text
    citation = html_escape(f"{authors}.\n<i>{venue}<\i>, {pub_year}.")

    ## YAML variables
    md = "\n".join((
        "---",
        f"title: '{title}'",
        "collection: publications",
        f"permalink: {permalink}",
        f"date: {pub_date}",
        #f"year: {pub_year}",
        f"venue: '{venue}'",
        f"paper_url: '{url}'",
        f"citation: '{citation}'",
        "---",
    ))

    md_filename = os.path.basename(md_filename)

    with open(f"../_publications/{md_filename}", 'w') as f:
        f.write(md)
    #print(f'SUCCESSFULLY PARSED {bib_id}: \"', b["title"][:60],"..."*(len(b['title'])>60),"\"")
    print(f"SUCCESSFULLY PARSED {bib_id}:\n{md}\n")

