import json
import re
from bs4 import BeautifulSoup
from cleantext import clean

import argparse
import pathlib as pl

# TODO: more testing, give directory instead of file as option, output_file=input file?, test regex's more, ...


def argument_parser():
    parser = argparse.ArgumentParser(description="creates better_docstring_tokens from docstring")
    parser.add_argument('-i', '--input_file', type=str, help="Input file", required=True)
    parser.add_argument('-o', '--output_file', type=str, help="Output file", required=True)
    parser.add_argument('-l', '--language', type=str, help="language", default="java")
    return parser


def main(args):
    # input = pl.Path(args.input_dir)
    # output = pl.Path(args.output_dir)
    with open(args.input_file, mode="rt") as input:
        lines = input.readlines()
    with open(args.output_file, mode="wt") as output:
        for line in lines:
            dic = json.loads(line)
            docstring = dic["docstring"]

            if args.language == "java":
                docstring = remove_comment_delimiters(docstring)

            summary = get_summary(docstring)
            summary = remove_html_tags(summary)

            if args.language == "java":
                summary = remove_javadoc_tags(summary)

            summary = remove_urls(summary)
            tokens = get_tokens(summary)
            print(f"{dic['docstring']}\nnew token:\n{tokens}\nold tokens:\n{dic['docstring_tokens']}\n\n")
            """dic["better_docstring_tokens"] = tokens
            result = json.dumps(dic)
            output.write(result + "\n")"""


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


"""
@author
@version
@since
@see
@serial
@serialField
@return
@exception
@throws
@deprecated
{@inheritDoc}
{@link reference}
{@linkPlain reference}
{@value}
{@docRoot}
{@literal}
{@code}
"""
BAD_JAVADOC_TAGS_REGEX = \
    re.compile(r"@((author)|(version)|(since)|(see)|(serial)|(serialField)|(return)|(exception)|(throws)|(deprecated)|"
               r"(inheritDoc)|(link)|(linkPlain)|(value)|(docRoot)|(literal)|(code))")


def remove_javadoc_tags(summary: str) -> str:
    return BAD_JAVADOC_TAGS_REGEX.sub("", summary)


def remove_urls(summary: str) -> str:
    return clean(summary, no_urls=True, replace_with_url="")


DOCSTRING_REGEX_TOKENIZER = \
    re.compile(r"[^\s,'\"`.():\[\]=*;>{\}+-/\\]+|\\+|\.+|\(\)|{\}|\[\]|\(+|\)+|:+|\[+|\]+|{+|\}+|=+|\*+|;+|>+|\++|-+|/+")


def get_tokens(summary: str) -> list:
    return re.findall(DOCSTRING_REGEX_TOKENIZER, summary)


if __name__ == '__main__':
    parser = argument_parser()
    args = parser.parse_args()
    main(args)