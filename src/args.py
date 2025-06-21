import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fields', default=None, help='Fields to be processed. Comma-separated list of field names.')
    parser.add_argument('-o', '--output', default=None, help='Output JSON file path where the processed data will be saved.')
    parser.add_argument('-t', '--term', required=True, help='The query string used to filter articles.')
    parser.add_argument('-n', '--number', type=int, default=None, help='The number of articles being fetched.')
    parser.add_argument('-d', '--dry-run', default=False, action='store_true', help='The term is compiled and printed. Nothing else will be done.')
    args = parser.parse_args()
    fields = None
    if args.fields:
        fields = [field.strip() for field in args.fields.split(',')]
    output = args.output
    term = args.term
    number = args.number
    dry_run = args.dry_run
    return (fields, output, term, number, dry_run)
    