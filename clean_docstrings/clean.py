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
RE_JAVADOC_LINK = re.compile(r'{[ \t]*@[ \t]*link([^}]*)}')
RE_JAVADOC_LINK_WO_BRACKETS = re.compile(r'@[ \t]*link')
def remove_javadoc_links(text: str, keep_inside: bool = True) -> str:
    """
    Removes {@link Whatever} link tags
    :param text:
    :param keep_inside:
    :return:
    """
    text = RE_JAVADOC_LINK.sub(r"\1" if keep_inside else "", text)
    text = RE_JAVADOC_LINK_WO_BRACKETS.sub("", text)
    return text

RE_JAVADOC_CODE = re.compile(r'{[ \t]*@[ \t]*code(.*?)}')
RE_JAVADOC_CODE_HTML = re.compile(r'<\s*code\s*>(.*?)<\s*/\s*code\s*>')
RE_JAVADOC_CODE_WO_BRACKETS = re.compile(r'@[ \t]*code')
def remove_javadoc_code(text: str, keep_inside: bool = True) -> str:
    """
    Removes {@link Whatever} link tags
    :param text:
    :param keep_inside:
    :return:
    """
    text = RE_JAVADOC_CODE.sub(r"\1" if keep_inside else "", text)
    text = RE_JAVADOC_CODE_HTML.sub(r"\1" if keep_inside else "", text)
    text = RE_JAVADOC_CODE_WO_BRACKETS.sub("", text)
    return text


def remove_javadoc_tags(text: str) -> str:
    text = remove_javadoc_links(text)


def clean_javadoc(javadoc: str) -> str:
    javadoc = remove_comment_delimiters(javadoc)

    javadoc = remove_javadoc_links(javadoc, keep_inside=True)

    javadoc = remove_html_tags(javadoc)

    return javadoc