import json
import re
from bs4 import BeautifulSoup
from cleantext import clean

import argparse
import pathlib as pl

# TODO: more testing(generics in java, other languages than java, python),
#  test regex's more, lower cases tokens not sure how or if it is a problem, ...


def argument_parser():
    parser = argparse.ArgumentParser(description="creates better_docstring_tokens from docstring")
    parser.add_argument('-i', '--input', type=str, help="Input file", required=True)
    parser.add_argument('-o', '--output_file', type=str, help="Output file (can only be chosen when input is a file")
    parser.add_argument('-l', '--language', type=str, help="language", default="java")
    return parser


def main(args):
    input = pl.Path(args.input)
    if input.is_dir():
        input_files = input.glob('**/*.jsonl')
        parse_files(input_files, args.language)

    elif args.output_file:
        output_path = pl.Path(args.output_file)
        parse_files([input], args.language, output_path)

    else:
        parse_files([input], args.language)


def get_language(file_name: str):
    languages = ["java", "python", "go", "ruby", "php", "javascript"]
    for language in languages:
        if language in file_name:
            return language
    assert False, "Can't detect language"


def parse_files(input, language: str, output_file: pl.Path = None):
    for file_path in input:
        print(f"parsing {file_path}")
        with file_path.open(mode="rt") as file:
            lines = file.readlines()

        if not language:
            language = get_language(file_path.stem)

        if output_file is None:
            output_path = file_path
        else:
            output_path = output_file

        with output_path.open(mode="wt") as output:
            parsed_lines = parse_lines(lines, language)
            for dic in parsed_lines:
                json_line = json.dumps(dic) + "\n"
                output.write(json_line)


def parse_lines(lines: list, lang: str):
    for line in lines:
        dic = json.loads(line)
        docstring = dic["docstring"]

        if lang == "java":
            docstring = remove_comment_delimiters(docstring)

        summary = get_summary(docstring)
        summary = remove_html_tags(summary)

        if lang == "java":
            summary = remove_javadoc_tags(summary)

        summary = remove_urls(summary)
        tokens = get_tokens(summary)
        dic["better_docstring_tokens"] = tokens
        # print(f"{dic['docstring']}\nnew token:\n{tokens}\nold tokens:\n{dic['docstring_tokens']}\n\n")
        yield dic


# delimiters
RE_C_STYLE_COMMENT_DELIMITERS = re.compile(
    r"^\s*[/]?\s*[\*]+[ \t]*/?",
    flags=re.MULTILINE
)


def remove_comment_delimiters(comment: str) -> str:
    return RE_C_STYLE_COMMENT_DELIMITERS.sub("", comment)


def get_summary(doc_string: str) -> str:

    if "\n\n" in doc_string:
        return doc_string.split("\n\n")[0]
    elif "@param" in doc_string:
        return doc_string.split("@param")[0]
    return doc_string


# html tags
def remove_html_tags(text: str) -> str:
    soup = BeautifulSoup(text, features="html.parser")
    return soup.get_text()


BAD_JAVADOC_TAGS_REGEX = \
    re.compile(r"@((author)|(version)|(since)|(see)|(serial)|(serialField)|(return)|(exception)|(throws)|(deprecated)|"
               r"(inheritDoc)|(link)|(linkPlain)|(value)|(docRoot)|(literal)|(code))")


def remove_javadoc_tags(summary: str) -> str:
    return BAD_JAVADOC_TAGS_REGEX.sub("", summary)


def remove_urls(summary: str) -> str:
    return clean(summary, no_urls=True, replace_with_url="")


DOCSTRING_REGEX_TOKENIZER = \
    re.compile(
        r"[^\s,'\"`.():\[\]=*;>{\}+-/\\]+|\\+|\.+|\(\)|{\}|\[\]|\(+|\)+|:+|\[+|\]+|{+|\}+|=+|\*+|;+|>+|\++|-+|/+"
    )


def get_tokens(summary: str) -> list:
    return re.findall(DOCSTRING_REGEX_TOKENIZER, summary)


if __name__ == '__main__':
    parser = argument_parser()
    args = parser.parse_args()
    main(args)
