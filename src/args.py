import argparse
import ui

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fields', default=None, help='fields to be processed. Comma-separated list of field names.')
    parser.add_argument('-o', '--output', default=None, help='output JSON file path where the processed data will be saved.')
    parser.add_argument('-t', '--term', default=None, help='the query string used to filter articles.')
    parser.add_argument('-u', '--ui', default=None, action='store_true', help='open a CLI form to build a query string.')
    parser.add_argument('-n', '--number', type=int, default=None, help='the maximum number of articles being fetched.')
    parser.add_argument('-d', '--dry-run', default=None, action='store_true', help='the term is compiled and printed. Nothing else will be done.')
    args = parser.parse_args()
    fields = None
    if args.fields:
        fields = [field.strip() for field in args.fields.split(',')]
    output = args.output
    term = args.term
    ui = args.ui
    number = args.number
    dry_run = args.dry_run

    if term and ui:
        raise Exception("Both -t/--term and -u/--ui are provided.")
    if not term and not ui:
        raise Exception("Neither -t/--term nor -u/--ui is provided.")
    if not output and not dry_run:
        raise Exception("An output file path is required.")
    if not isinstance(number, int) and not dry_run:
        raise Exception("The maximum number of results is required.")

    return (fields, output, term, ui, number, dry_run)
    