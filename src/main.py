# -*- coding: utf-8 -*-
import args
import core
import pymed
import json
import path
import os.path
import term

# https://stackoverflow.com/questions/57053378/query-pubmed-with-python-how-to-get-all-article-details-from-query-to-pandas-d

accessors = {
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
    (fields, output, term_str, num) = args.parse_args()
    if fields is None:
        fields = list(accessors.keys())
    
    json_code = None
    with open(os.path.join(path.SRC_PATH, "json/parser.json"), "r") as f:
        json_code = f.read().rstrip()

    parsed_term = core.run(json_code)(term_str, term.cons_term, lambda s: s=="(", lambda s: s==")", lambda s: s.isspace(), Exception)
    if isinstance(parsed_term, Exception):
        raise parsed_term
    real_term = term.render_term(parsed_term)
    print(f"Compiled term: {real_term}")

    results = []
    pubmed = pymed.PubMed(tool='PubMedSearcher', email='myemail@ccc.com')
    articles = pubmed.query(real_term, max_results=num)
    for article in articles:
        d = article.toDict()
        r = {}
        for field in fields:
            r[field] = d[field]
        results.append(r)
    
    with open(output, "w") as f:
        f.write(json.dumps(results, indent=4))


if __name__ == "__main__":
    main()
