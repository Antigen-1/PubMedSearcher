import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fields', default=None, help='Fields to be processed. Comma-separated list of field names.')
    parser.add_argument('-o', '--output', required=True, help='Output JSON file path where the processed data will be saved.')
    parser.add_argument('-t', '--term', required=True, help='The query string used to filter articles.')
    parser.add_argument('-n', '--number', type=int, required=True, help='The number of articles being fetched.')
    args = parser.parse_args()
    fields = None
    if args.fields:
        fields = [field.strip() for field in args.fields.split(',')]
    output = args.output.strip()
    term = args.term.strip()
    number = args.number
    return (fields, output, term, number)
    