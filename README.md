# PubMedSearcher

Save information of pubmed articles as a JSON file.

# Command-line Usage

Use `dump-articles -h` to get all options.

# Term Syntax

We use a scheme-expression-like syntax to represent terms. For Example,

`(And (Or (Title/Abstract complication) (Title/Abstract adverse events)) (Or (Title/Abstract esophageal stenting) (Title/Abstract stent placement for esophageal cancer)))`

is transformed to

`(('complication'[Title/Abstract] OR 'adverse events'[Title/Abstract]) AND ('esophageal stenting'[Title/Abstract] OR 'stent placement for esophageal cancer'[Title/Abstract]))`.