# setup.py
from setuptools import setup
from Cython.Build import cythonize
import numpy

print("Setting UP GrenzVel...")

setup(
    name="GrenzVel",
    ext_modules=cythonize("GrenzVel.pyx", compiler_directives={"language_level": "3"}),
    include_dirs=[numpy.get_include()]
)
