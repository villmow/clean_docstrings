import unittest
from clean_docstrings import remove_comment_delimiters, remove_html_tags


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


class TestUtility(unittest.TestCase):
    def test_delimiters_compare_with_csn(self):
        docstring = """  /**
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
     * @return an Observable that emits the same sequence as whichever of the source ObservableSources first
     *         emitted an item or sent a termination notification
     * @see <a href="http://reactivex.io/documentation/operators/amb.html">ReactiveX operators documentation: Amb</a>
     */ """
        self.assertSequenceEqual(
            remove_comment_delimiters(docstring).strip(),
            strip_c_style_comment_delimiters(docstring).strip(),
        )
    def test_delimiters_no(self):
        """
        Nothing should happen if no delimiters are present
        """
        docstring = """ Mirrors the one ObservableSource in an Iterable of several ObservableSources that first either emits an item or sends
a termination notification.



Scheduler:
{@code amb} does not operate by default"""
        self.assertSequenceEqual(
            remove_comment_delimiters(docstring).strip(),
            docstring.strip(),
        )

    def test_html_tags_simple(self):
        docstring = """ some string 
        <p> 
        <img width="640" height="385" src="https://raw.github.com/wiki/ReactiveX/RxJava/images/rx-operators/amb.png" alt="">
        <dl>
        <dt><b>scheduler</b></dt>
        <dd>{@code amb} does not operate by default on a particular {@link Scheduler}.</dd>
        </dl>
        """

        stripped_docstring = remove_html_tags(docstring)
        
        # this should be removed
        self.assertNotIn("github", stripped_docstring, "HTML tags should have been removed")
        self.assertNotIn("640", stripped_docstring, "HTML tags should have been removed")
        self.assertNotIn("<p>", stripped_docstring, "HTML tags should have been removed")
        self.assertNotIn("<dl>", stripped_docstring, "HTML tags should have been removed")
        self.assertNotIn("</p>", stripped_docstring, "HTML tags should have been removed")
        self.assertNotIn("</dl>", stripped_docstring, "HTML tags should have been removed")
        
        # this should remain
        self.assertIn("scheduler", stripped_docstring, "This word should remain after stripping html tags")
        self.assertIn("some string", stripped_docstring, "This word should remain after stripping html tags")
        self.assertIn("{@code amb} does not operate by default on a particular {@link Scheduler}.", stripped_docstring, "This word should remain after stripping html tags")

    def test_html_tags_with_code(self):
        docstring = """ some string 
        <p> <b>scheduler</b>
       {@code i < 4} this should stay {@code i > 10}.
        """

        stripped_docstring = remove_html_tags(docstring)

        # this should be removed
        self.assertNotIn("<p>", stripped_docstring, "HTML tags should have been removed")
        self.assertNotIn("<b>", stripped_docstring, "HTML tags should have been removed")
        self.assertNotIn("</b>", stripped_docstring, "HTML tags should have been removed")

        # this should remain
        self.assertIn("scheduler", stripped_docstring, "This word should remain after stripping html tags")
        self.assertIn("some string", stripped_docstring, "This word should remain after stripping html tags")
        self.assertIn("this should stay", stripped_docstring, "This word should remain after stripping html tags")


if __name__ == '__main__':
    unittest.main()
