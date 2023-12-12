import argparse
from functools import partial
import json
import multiprocessing as mp
import pathlib as pl

from clean_docstrings import clean


def argument_parser():
    parser = argparse.ArgumentParser(
        description="Parse docstrings in a .jsonl file and add a new field for the cleaned docstrings."
    )
    parser.add_argument("input", type=str, help="Input file.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-i", "--inplace", action="store_true", help="Change file inplace."
    )
    group.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Specify output file if not inplace. Otherwise prints to stdout.",
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        default=None,
        help="Programming language of the file or directory. Nedded for java.",
    )
    parser.add_argument(
        "--input-key",
        type=str,
        help="Name of the key containing the docstring.",
        default="docstring",
    )
    parser.add_argument(
        "--output-key",
        type=str,
        help="Name of the added key containing the cleaned docstring.",
        default="docstring_tokens_clean",
    )
    parser.add_argument(
        "--workers", type=int, help="Number of processes to use.", default=1
    )
    return parser


def main(args):
    input = pl.Path(args.input)

    output = None
    if args.output is not None:
        output = pl.Path(args.output)
    elif args.inplace:
        output = input.with_name(f".{input.name}.tmp")

    # open output filehandler
    output_f = None
    if output is not None:
        output_f = output.open("wt")

    func = partial(
        parse_line,
        language=args.language,
        input_key=args.input_key,
        output_key=args.output_key,
    )
    with mp.Pool(args.workers) as p, input.open("rt") as input_f:
        for out_line in p.imap(func, input_f, chunksize=25):
            print(out_line, file=output_f)

    # close output filehandler
    if output_f is not None:
        output_f.close()
    if args.inplace:
        output.replace(input)


def parse_line(line: str, language: str, input_key: str, output_key: str):
    line_dict = json.loads(line.strip())
    line_dict[output_key] = clean(
        docstring=line_dict[input_key],
        language=language,
        extract_summary=True,
        no_comment_delimiters=True,
        no_html_tags=True,
        no_urls=True,
        url_replacement="",
        tokenize=True,
        fix_unicode=True,
    )
    return json.dumps(line_dict, ensure_ascii=False)


def cli_main():
    parser = argument_parser()
    args = parser.parse_args()
    main(args)


if __name__ == "__main__":
    cli_main()
