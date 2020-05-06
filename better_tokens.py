import json
# import clean_docstrings.clean as clean_docs
import argparse
import pathlib as pl
from clean_docstrings.clean import clean_java_docstring
from clean_docstrings.clean import clean_python_docstring
from clean_docstrings.clean import clean_go_docstring
from clean_docstrings.clean import clean_ruby_docstring
from clean_docstrings.clean import clean_php_docstring
from clean_docstrings.clean import clean_javascript_docstring


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


def parse_lines(lines: list, language: str):
    docstring_cleaner = None
    if language == "java":
        docstring_cleaner = clean_java_docstring
    elif language == "python":
        docstring_cleaner = clean_python_docstring
    elif language == "go":
        docstring_cleaner = clean_go_docstring
    elif language == "ruby":
        docstring_cleaner = clean_ruby_docstring
    elif language == "php":
        docstring_cleaner = clean_php_docstring
    elif language == "javascript":
        docstring_cleaner = clean_javascript_docstring
    else:
        assert False, "unknown language (known languages are: java, python, go, ruby, php, javascript)"

    for line in lines:
        file_dict = json.loads(line)
        file_dict["docstring_tokens_cleaned"] = docstring_cleaner(file_dict["docstring"])
        yield file_dict


if __name__ == '__main__':
    parser = argument_parser()
    args = parser.parse_args()
    main(args)
