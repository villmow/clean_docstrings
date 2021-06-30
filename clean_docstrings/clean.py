import re

from bs4 import BeautifulSoup
from cleantext import replace_urls, fix_bad_unicode

from typing import Optional, List

##########################
# delimiters
##########################
RE_C_STYLE_COMMENT_DELIMITERS = re.compile(
    r"(^\s*[/]?\s*[\*]+[ \t]*/?)|(^\s*//)|(\s*[/]?\s*[\*]+[ \t]*/?$)",
    flags=re.MULTILINE
)
def remove_comment_delimiters(comment: str) -> str:
    return RE_C_STYLE_COMMENT_DELIMITERS.sub("", comment)


##########################
# html tags
##########################
def remove_html_tags(text: str) -> str:
    try:
        soup = BeautifulSoup(text, features="html.parser")
        return soup.get_text()
    except TypeError as e:
        raise e


##########################
# javadoc tags
##########################
# matches javadoc tags, but allows spaces between the tags
RE_JAVADOC_TAGS = re.compile(r'{[ \t]*@[ \t]*((author)|(version)|(since)|(see)|(serial)|(serialField)|(return)|'
                             r'(exception)|(throws)|(deprecated)|(inheritDoc)|(link)|(linkPlain)|(value)|(docRoot)|'
                             r'(literal)|(code)|(param))([^}]*)}')
RE_JAVADOC_TAGS_WO_BRACKETS = re.compile(r'@((author)|(version)|(since)|(see)|(serial)|(serialField)|(return)|'
                                         r'(exception)|(throws)|(deprecated)|(inheritDoc)|(link)|(linkPlain)|(value)|'
                                         r'(docRoot)|(literal)|(code)|(param))')
def _remove_javadoc_tags(text: str, keep_inside: bool = True) -> str:
    """
    Removes java doc tags that have the form {@javadocTag "something < inside" }
    :param text:
    :param keep_inside: Keeps the value inside
    :return:
    """
    text = RE_JAVADOC_TAGS.sub(r"\20" if keep_inside else "", text)
    text = RE_JAVADOC_TAGS_WO_BRACKETS.sub("", text)
    return text


def remove_doctags(text: str, keep_inside: bool = True, language: Optional[str] = None):
    return _remove_javadoc_tags(text, keep_inside)


##########################
# summary
##########################
def _docstring_summary_default(docstring: str) -> str:
    """
    This function was taken from codesearchnet.

    Get the first lines of the documentation comment up to the empty lines.
    """
    if '\n\n' in docstring:
        return docstring.split('\n\n')[0]
    elif '@' in docstring:
        return docstring[:docstring.find('@')]  # This usually is the start of a JavaDoc-style @param comment.
    return docstring


def _docstring_summary_javadoc(doc_string: str) -> str:

    if "\n\n" in doc_string:
        return doc_string.split("\n\n")[0]
    elif "@param" in doc_string:
        return doc_string.split("@param")[0]
    return doc_string


def extract_docstring_summary(docstring: str, language: Optional[str] = None) -> str:
    """
    Requires a docstring that has block comment delimiters removed.

    Extracting the summary may differ from language to language. We
    default to codesearchnets extraction, but implement better
    language specific extractions if we notice issues (Currently only java).

    :param docstring:
    :param language:
    :return:
    """
    if language == "java":
        return _docstring_summary_javadoc(docstring)

    return _docstring_summary_default(docstring)


##########################
# urls
##########################
def remove_urls(text: str, replace_with: str = None) -> str:
    """ Removes URLS from text"""
    return replace_urls(text, replace_with=replace_with)


###########################
# tokenize
##########################
DOCSTRING_REGEX_TOKENIZER = re.compile(
    r"[^\s,'\"`.():\[\]=*;>{\}+-/\\]+|\\+|\.+|\(\)|{\}|\[\]|\(+|\)+|:+|\[+|\]+|{+|\}+|=+|\*+|;+|>+|\++|-+|/+"
)  # taken from codesearchnet

def tokenize_csn(text: str) -> List[str]:
    """ Uses the regex from codesearchnet. """
    return re.findall(DOCSTRING_REGEX_TOKENIZER, text)


###########################
# main function
##########################
def clean(
    docstring: str, language: Optional[str] = None,
    extract_summary: bool = True,
    no_comment_delimiters: bool = True,
    no_html_tags: bool = True,
    no_doctags: bool = True,
    no_urls: bool = True, url_replacement: str = "<URL>",
    tokenize: bool = False,
    fix_unicode: bool = True
):
    if no_comment_delimiters:
        docstring = remove_comment_delimiters(docstring)
    if extract_summary:
        docstring = extract_docstring_summary(docstring, language=language)
    if fix_unicode:
        docstring = fix_bad_unicode(docstring)
    if no_urls:
        docstring = remove_urls(docstring, replace_with=url_replacement)
    if no_html_tags and docstring:
        try:
            docstring = remove_html_tags(docstring)
        except TypeError as e:
            # ignore type errors
            pass

    if no_doctags:
        docstring = remove_doctags(docstring, keep_inside=True, language=language)
    if tokenize:
        docstring = tokenize_csn(docstring)
    return docstring


