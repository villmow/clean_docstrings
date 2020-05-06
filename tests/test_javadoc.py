import unittest
from clean_docstrings import *


class TestJavadoc(unittest.TestCase):
    def test_sample1(self):
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
        cleaned_docs = clean_java_docstring(docstring)
        for cleaned_doc in cleaned_docs:
            print(cleaned_doc)

    def test_remove_links(self):

        docstring = "This is {@link Link1}. " \
                    "This is a malformed @link Link2. " \
                    "This is a malformed {@ link Link3}. " \
                    "This is a malformed { @ link Link4}. "

        print(docstring)
        print("#" * 20)
        cleaned_doc = remove_javadoc_tags(docstring, keep_inside=True)
        print(cleaned_doc)
        self.assertIn("Link1", cleaned_doc)
        self.assertIn("Link2", cleaned_doc)
        self.assertIn("Link3", cleaned_doc)
        self.assertIn("Link4", cleaned_doc)
        self.assertNotIn("@link", cleaned_doc, "All @links should have been removed")
        self.assertNotIn("@ link", cleaned_doc, "All @links should have been removed")

        cleaned_doc = remove_javadoc_tags(docstring, keep_inside=False)
        self.assertNotIn("Link1", cleaned_doc)
        self.assertNotIn("Link3", cleaned_doc)
        self.assertNotIn("Link4", cleaned_doc)
        self.assertIn("Link2", cleaned_doc)  # we won't match this

    def test_remove_code(self):

        docstring = "Liefert eine @code Geldbetrag} zurueck, dessen Wert <code>x % divisor</code> entspricht. " \
                    "@return {@code this % mod}."

        print(docstring)
        cleaned_doc = remove_javadoc_tags(docstring, keep_inside=True)
        print("#" * 20)
        print(cleaned_doc)
        self.assertIn("Geldbetrag", cleaned_doc)
        self.assertIn("divisor", cleaned_doc)
        self.assertIn("this", cleaned_doc)
        self.assertIn("%", cleaned_doc)
        self.assertNotIn("@code", cleaned_doc, "All @code should have been removed")
        self.assertNotIn("<code>", cleaned_doc, "All <code> should have been removed")

        cleaned_doc = remove_javadoc_tags(docstring, keep_inside=False)
        print("#" * 20)
        print(cleaned_doc)
        self.assertNotIn("Geldbetrag", cleaned_doc)
        self.assertNotIn("divisor", cleaned_doc)
        self.assertNotIn("this", cleaned_doc)
        self.assertNotIn("mod", cleaned_doc)
        self.assertNotIn("@code", cleaned_doc, "All @code should have been removed")
        self.assertNotIn("<code>", cleaned_doc, "All <code> should have been removed")


if __name__ == '__main__':
    unittest.main()
