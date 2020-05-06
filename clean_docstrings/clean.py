import re

from bs4 import BeautifulSoup
from cleantext import clean


# delimiters
RE_C_STYLE_COMMENT_DELIMITERS = re.compile(
    r"^\s*[/]?\s*[\*]+[ \t]*/?",
    flags=re.MULTILINE
)


def remove_comment_delimiters(comment: str) -> str:
    return RE_C_STYLE_COMMENT_DELIMITERS.sub("", comment)


def strip_c_style_comment_delimiters(comment: str) -> str:
    """ This function was taken from codesearchnet """
    comment_lines = comment.split('\n')
    cleaned_lines = []
    for l in comment_lines:
        l = l.strip()
        if l.endswith('*/'):
            l = l[:-2]
        if l.startswith('*'):
            l = l[1:]
        elif l.startswith('/**'):
            l = l[3:]
        elif l.startswith('//'):
            l = l[2:]
        cleaned_lines.append(l.strip())
    return '\n'.join(cleaned_lines)


# html tags
def remove_html_tags(text: str) -> str:
    soup = BeautifulSoup(text, features="html.parser")
    return soup.get_text()


# matches javadoc tags, but allows spaces between the tags
RE_JAVADOC_TAGS = re.compile(r'{[ \t]*@[ \t]*((author)|(version)|(since)|(see)|(serial)|(serialField)|(return)|'
                             r'(exception)|(throws)|(deprecated)|(inheritDoc)|(link)|(linkPlain)|(value)|(docRoot)|'
                             r'(literal)|(code))([^}]*)}')
RE_JAVADOC_TAGS_WO_BRACKETS = re.compile(r'@((author)|(version)|(since)|(see)|(serial)|(serialField)|(return)|'
                                         r'(exception)|(throws)|(deprecated)|(inheritDoc)|(link)|(linkPlain)|(value)|'
                                         r'(docRoot)|(literal)|(code))')


def remove_javadoc_tags(text: str, keep_inside: bool = True) -> str:
    """
    Removes java doc tags
    :param text:
    :param keep_inside:
    :return:
    """
    text = RE_JAVADOC_TAGS.sub(r"\19" if keep_inside else "", text)
    text = RE_JAVADOC_TAGS_WO_BRACKETS.sub("", text)
    return text


def get_docstring_summary(docstring: str) -> str:
    """
    This function was taken from codesearchnet
    Get the first lines of the documentation comment up to the empty lines.
    """
    if '\n\n' in docstring:
        return docstring.split('\n\n')[0]
    elif '@' in docstring:
        return docstring[:docstring.find('@')]  # This usually is the start of a JavaDoc-style @param comment.
    return docstring


def get_java_doc_summary(doc_string: str) -> str:

    if "\n\n" in doc_string:
        return doc_string.split("\n\n")[0]
    elif "@param" in doc_string:
        return doc_string.split("@param")[0]
    return doc_string


def remove_urls(summary: str) -> str:
    return clean(summary, no_urls=True, replace_with_url="", lower=False, to_ascii=False)


DOCSTRING_REGEX_TOKENIZER = \
    re.compile(
        r"[^\s,'\"`.():\[\]=*;>{\}+-/\\]+|\\+|\.+|\(\)|{\}|\[\]|\(+|\)+|:+|\[+|\]+|{+|\}+|=+|\*+|;+|>+|\++|-+|/+"
    )


def get_tokens(summary: str) -> list:
    return re.findall(DOCSTRING_REGEX_TOKENIZER, summary)


def clean_generic_docstring(docstring: str):
    docstring = remove_comment_delimiters(docstring)
    summary = get_docstring_summary(docstring)
    summary = remove_html_tags(summary)
    summary = remove_urls(summary)
    tokens = get_tokens(summary)

    return tokens


def clean_python_docstring(docstring: str):
    return clean_generic_docstring(docstring)


def clean_ruby_docstring(docstring: str):
    return clean_generic_docstring(docstring)


def clean_php_docstring(docstring: str):
    return clean_generic_docstring(docstring)


def clean_go_docstring(docstring: str):
    return clean_generic_docstring(docstring)


def clean_javascript_docstring(docstring: str):
    return clean_generic_docstring(docstring)


def clean_java_docstring(docstring: str):
    docstring = remove_comment_delimiters(docstring)
    summary = get_java_doc_summary(docstring)
    summary = remove_html_tags(summary)

    summary = remove_javadoc_tags(summary)

    summary = remove_urls(summary)
    tokens = get_tokens(summary)
    return tokens
