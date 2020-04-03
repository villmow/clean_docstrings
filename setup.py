from distutils.core import setup

setup(name='clean_docstrings',
      version='0.1a',
      python_requires='>=3.7',
      description='Utility functions to clean docstrings in various languages',
      author='Johannes Villmow',
      author_email='johannes.villmow@hs-rm.de',
      license='gnu',
      packages=['clean_docstrings'],
      install_requires=[
            "clean_text",
      ]
)

