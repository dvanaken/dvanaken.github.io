# # Publications markdown generator for academicpages
# 
# Takes a TSV of publications with metadata and converts them for use with [academicpages.github.io](academicpages.github.io). This is an interactive Jupyter notebook, with the core python code in publications.py. Run either from the `markdown_generator` folder after replacing `publications.tsv` with one that fits your format.
# 

# ## Data format
# 
# The TSV needs to have the following columns: pub_date, title, venue, excerpt, citation, site_url, and paper_url, with a header at the top. 
# 
# - `excerpt` and `paper_url` can be blank, but the others must have values. 
# - `pub_date` must be formatted as YYYY-MM-DD.
# - `url_slug` will be the descriptive part of the .md file and the permalink URL for the page about the paper. The .md file will be `YYYY-MM-DD-[url_slug].md` and the permalink will be `https://[yourdomain]/publications/YYYY-MM-DD-[url_slug]`



import csv
import json
import os


# ## Import TSV
# 
# Pandas makes this easy with the read_csv function. We are using a TSV, so we specify the separator as a tab, or `\t`.
# 
# I found it important to put this data in a tab-separated values format, because there are a lot of commas in this kind of data and comma-separated values can get messed up. However, you can modify the import statement, as pandas also has read_excel(), read_json(), and others.

PUBS_INPUT_FILE = "publications.json"

PUBS_OUTPUT_DIR = "../_publications"  # output directory


def html_escape(text):
    """Produce entities within text."""
    # ## Escape special characters
    # 
    # YAML is very picky about how it takes a valid string, so we are replacing single and
    # double quotes (and ampersands) with their HTML encoded equivilents. This makes them
    # look not so readable in raw format, but they are parsed and rendered nicely.
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
    }
    return "".join(html_escape_table.get(c,c) for c in text)


def load_file(filename=PUBS_INPUT_FILE):
    ext = filename.rsplit(".", 1)[-1]

    if ext == "json":
        with open(filename, "r") as f:
            publications = json.load(f)

    elif ext in ("csv", "tsv"):
        sep = "," if ext == "csv" else "\t"
        publications = []
        with open(filename, "r", newline="") as f:
            reader = csv.reader(f, delimiter=sep)
            header = next(reader)

            for row in reader:
                publications.append(dict(zip(header, row)))

    else:
        raise Exception(f"Unsupported file type: {filename}")

    return publications


def process_publication(
    **kwargs,
):
    basename = f"{kwargs['date']}-{kwargs['urlslug']}"
    md_filename = f"{basename}.md"
    kwargs["permalink"] = f"/publications/{basename}"
    kwargs["collection"] = "publications"

    md = ["---"]

    keys = (
        "title",
        "collection",
        "permalink",
        "date",
        "authors",
        "venue",
        "paperurl",
        "pubtype",
    )

    for key in keys:
        if key in kwargs:
            value = html_escape(kwargs[key])
            if key != "date":
                value = f"'{value}'"
            md.append(f"{key}: {value}")
        else:
            assert key in ("pubtype",), key

    md.append("---")
    md = "\n".join(md)

    return md, md_filename



def main():
    os.makedirs(PUBS_OUTPUT_DIR, exist_ok=True)

    publications = load_file()

    for entry in publications:

        md, md_filename = process_publication(**entry)

        with open(os.path.join(PUBS_OUTPUT_DIR, md_filename), "w") as f:
            f.write(md)


if __name__ == "__main__":
    main()

