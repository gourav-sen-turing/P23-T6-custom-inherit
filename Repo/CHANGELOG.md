### 2.3.0 (10/14/2019)
- This release adds three new built-in styles, `numpy_with_merge`, `google_with_merge`, and `numpy_napoleon_with_merge`, which 
permit users to concatenate the respective sections of a parent's and child's docstrings.
Also added is the ability to configure `DocInheritMeta` so that special methods will have their docstrings inherited as well.
([#31](https://github.com/rsokl/custom_inherit/pull/31)). Big thanks to [@Boubsi](https://github.com/Boubsi) for these nice features!



### 2.2.2 (10/14/2019)
- This release does not contain any changes to the `custom-inherit` code base. Changes are made to some of the packaging files so that `custom-inherit` can be hosted on conda.

### 2.2.1 (10/06/2019)
- Dropping support for Python 3.3
- Adding support for Python 3.8
- This will be the final version of `custom_inherit` to support Python 2.7
- Minor code refactoring (formatting with black & isort)

### 2.2.0 (3/27/2018)
- Previously, the class docstring inherited only from the most immediate parent class that has a docstring. Now,
the "parent" docstring is accumulated by successively merging the accumulated string with the docstring of
the next-parent in the mro. This accumulated docstring is then merged with the docstring of the present class. This permits sensible class-docstring inheritance in cases of multiple inheritance.
- Minor code refactoring.

### 2.1.1 (2/15/2017)
- Added compatibility with Python 3.3 & 3.4

### 2.1.0 (1/8/2017)
- [Napoleon](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/index.html#id1) docstring specifications for Google and NumPy docstring formats are supported as defaults ('google' and 'numpy_napoleon').
- [reST section-delimited](http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#sections) docstring inheritance is supported via the default style 'reST'. 
- `custom_inherit` now has unit test coverage for the entire package (for Python 2.7, 3.5, 3.6).
- Import styles updated for compatibility with Jython 2.7.
- Improved documentation.

### 2.0.2
- custom_inherit.store no longer inherits from `dict`. Fixes bug in which `store.update` could be used
to circumvent the type-checking that the store enforces.

### 2.0.1
- Numpy-style section delimiters was fixed so that they are the appropriate length, and thus compatible with the numpy-style for sphinx.
- `doc_inherit` was refactored so that the signature of the decorated function is now preserved in Python(< 3.4). This was not an issue for newer versions of Python.

### 2.0.0
- A decorator, `doc_inherit` is now available for mediating docstring inheritance for a single function/method.property/etc.

- inheritance style functions can now be supplied directly to `style` arguments.

- Styles are now all managed through `custom_inherit.store`

- It is no longer necessary for users to implement styles by subclassing base inheritance classes from this package.

### 1.1.0
- Users no longer need to write a separate abstract base class version of their custom styles. This is now built on the fly within `DocInheritMeta`.

- Styles need only be logged in `custom_inherit.style_store.__all__` for the style to become available for use.

- The "numpy" inheritance style was updated to accommodate for situations in which method docstrings contain both "Raises" and "Returns"/"Yields" sections. 
