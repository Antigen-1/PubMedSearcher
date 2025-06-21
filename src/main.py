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
    (fields, output, term_str, num, dry_run) = args.parse_args()
    if fields is None:
        fields = list(accessors.keys())
    
    real_term = term.compile_term(term_str)
    print(f"Compiled term: {real_term}")
    if dry_run:
        return
    if output is None:
        raise Exception("An output file path is required.")
    if num is None:
        raise Exception("An upper bound of the number of results is required.")

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
