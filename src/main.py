# -*- coding: utf-8 -*-
import args
import core
import pymed
import sys
import json
import path
import os.path

# https://stackoverflow.com/questions/57053378/query-pubmed-with-python-how-to-get-all-article-details-from-query-to-pandas-d

constructors = {
    'pubmed_id': lambda a: a['pubmed_id'].partition('\n')[0],
    'title': lambda a: a['title'],
    'keywords': lambda a: a['keywords'],
    'journal': lambda a: a['journal'],
    'abstract': lambda a: a['abstract'],
    'conclusions': lambda a: a['conclusions'],
    'methods': lambda a: a['methods'],
    'results': lambda a: a['results'],
    'copyrights': lambda a: a['copyrights'],
    'doi': lambda a: a['doi'],
    'publication_date': lambda a: a['publication_date'].strftime('%Y-%m-%d'),
    'authors': lambda a: a['authors'],
}

def main():
    (fields, output, term, num) = args.parse_args()
    if fields is None:
        fields = list(constructors.keys())
    
    json_code = None
    with open(os.path.join(path.SRC_PATH, "json/dict.json"), "r") as f:
        json_code = f.read().rstrip()
    
    make_partial_dict = core.run(json_code)(constructors, Exception)

    results = []
    pubmed = pymed.PubMed(tool='PubMedSearcher', email='myemail@ccc.com')
    articles = pubmed.query(term, max_results=num)
    for article in articles:
        r = make_partial_dict(article.toDict(), fields)
        if isinstance(r, Exception):
            print(f"Error processing article: {r}", file=sys.stderr)
        results.append(r)
    
    with open(output, "w") as f:
        f.write(json.dumps(results, indent=4))


if __name__ == "__main__":
    main()
