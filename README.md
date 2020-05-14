# clean-docstrings

Offers cleaning of docstrings in most programming languages (e.g. documentations of methods, classes).

Features:
 - Extracts summary
 - Removes URLs
 - Removes HTML
 - Removes Javadoc Tags (when language is set to "java")
 
Install this package by cloning this repo and executing
 ```bash
pip install clean-docstrings 
```

## Usage

To use it from Python:
```python
from clean_docstrings import clean
docstring = """/**
     * Mirrors the one ObservableSource in an Iterable of several ObservableSources that first either emits an item or sends
     * a termination notification.
     * <p>
     * <img width="640" height="385" src="https://raw.github.com/wiki/ReactiveX/RxJava/images/rx-operators/amb.png" alt="">
     * <dl>
     *  <dt><b>Scheduler:</b></dt>
     *  <dd>{@code amb} does not operate by default on a particular {@link Scheduler}.</dd>
     * </dl>
     *
     * @param <T> the common element type
     * @param sources
     *            an Iterable of ObservableSource sources competing to react first. A subscription to each source will
     *            occur in the same order as in the Iterable.
     * @return an Observable that emits the same @link sequence as whichever of the source ObservableSources first
     *         emitted an item or sent a termination notification
     * @see <a href="http://reactivex.io/documentation/operators/amb.html">ReactiveX operators documentation: Amb</a>
     */ """
clean(docstring, language="java", extract_summary=False,   no_comment_delimiters = True, no_html_tags = True, no_urls = True, url_replacement = "", tokenize = True, fix_unicode = True)
>>> ['Mirrors', 'the', 'one', 'ObservableSource', 'in', 'an', 'Iterable', 'of', 'several', 'ObservableSources', 'that', 'first', 'either', 'emits', 'an', 'item', 'or', 'sends', 'a', 'termination', 'notification', '.', 'Scheduler', ':', 'amb', 'does', 'not', 'operate', 'by', 'default', 'on', 'a', 'particular', 'Scheduler', '.', 'the', 'common', 'element', 'type', 'sources', 'an', 'Iterable', 'of', 'ObservableSource', 'sources', 'competing', 'to', 'react', 'first', '.', 'A', 'subscription', 'to', 'each', 'source', 'will', 'occur', 'in', 'the', 'same', 'order', 'as', 'in', 'the', 'Iterable', '.', 'an', 'Observable', 'that', 'emits', 'the', 'same', 'sequence', 'as', 'whichever', 'of', 'the', 'source', 'ObservableSources', 'first', 'emitted', 'an', 'item', 'or', 'sent', 'a', 'termination', 'notification', 'ReactiveX', 'operators', 'documentation', ':', 'Amb']
>>> clean(docstring, language="java", extract_summary=True,   no_comment_delimiters = True, no_html_tags = True, no_urls = True, url_replacement = "", tokenize = True, fix_unicode = True)
['Mirrors', 'the', 'one', 'ObservableSource', 'in', 'an', 'Iterable', 'of', 'several', 'ObservableSources', 'that', 'first', 'either', 'emits', 'an', 'item', 'or', 'sends', 'a', 'termination', 'notification', '.', 'Scheduler', ':', 'amb', 'does', 'not', 'operate', 'by', 'default', 'on', 'a', 'particular', 'Scheduler', '.']
>>> clean(docstring, language="java", extract_summary=True,   no_comment_delimiters = True, no_html_tags = True, no_urls = True, url_replacement = "", tokenize = False, fix_unicode = True)
'\nMirrors the one ObservableSource in an Iterable of several ObservableSources that first either emits an item or sends\na termination notification.\n\n\n\nScheduler:\n amb does not operate by default on a particular  Scheduler.\n'
```

This package installs a shell script: `clean-docs-jsonl` that can be used from command line to clean all docstrings in
a `.jsonl` file. This script is consistent with the preprocessing in codesearchnet, but additionally cleans
doctags, html and urls.

```bash
>>> clean-docs-jsonl --help                                                                                                          
usage: clean-docs-jsonl [-h] [-i | -o OUTPUT] [-l LANGUAGE]
                        [--input-key INPUT_KEY] [--output-key OUTPUT_KEY]
                        [--workers WORKERS]
                        input

Parse docstrings in a .jsonl file and add a new field for the cleaned
docstrings.

positional arguments:
  input                 Input file.

optional arguments:
  -h, --help            show this help message and exit
  -i, --inplace         Change file inplace.
  -o OUTPUT, --output OUTPUT
                        Specify output file if not inplace. Otherwise prints
                        to stdout.
  -l LANGUAGE, --language LANGUAGE
                        Programming language of the file or directory. Nedded
                        for java.
  --input-key INPUT_KEY
                        Name of the key containing the docstring.
  --output-key OUTPUT_KEY
                        Name of the added key containing the cleaned
                        docstring.
  --workers WORKERS     Number of processes to use.
```