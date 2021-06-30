from distutils.core import setup

setup(name='clean_docstrings',
      packages=['clean_docstrings'],
      version='0.1b',
      python_requires='>=3.7',
      description='Utility functions to clean docstrings in various programming languages',
      author='Johannes Villmow',
      author_email='johannes.villmow@hs-rm.de',
      url='https://github.com/villmow/clean_docstrings',
      download_url='',  # FIXME
      license='Apache License 2.0',
      entry_points={
            'console_scripts': [
                  'clean-docs-jsonl = clean_docstrings.cli.clean_jsonl:cli_main',
            ],
      },
      install_requires=[
            "clean_text",
            "beautifulsoup4"
      ],
      keywords=['source code', 'comment', 'cleaning', 'comment cleaning'],  # Keywords that define your package best
      classifiers=[
            'Development Status :: 4 - Beta',  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
            'Intended Audience :: Developers',  # Define that your audience are developers
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: Apache License',
            'Programming Language :: Python :: 3',
      ],
)