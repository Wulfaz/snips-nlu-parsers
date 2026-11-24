from __future__ import print_function

import io
import os
import sys

import shutil

from setuptools import setup, find_packages

packages = [p for p in find_packages() if "tests" not in p]

PACKAGE_NAME = "snips_nlu_parsers"
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
PACKAGE_PATH = os.path.join(ROOT_PATH, PACKAGE_NAME)
README = os.path.join(ROOT_PATH, "README.rst")
VERSION = "__version__"

RUST_EXTENSION_NAME = 'snips_nlu_parsers.dylib.libsnips_nlu_parsers_rs'
CARGO_ROOT_PATH = os.path.join(ROOT_PATH, 'ffi')
CARGO_FILE_PATH = os.path.join(CARGO_ROOT_PATH, 'Cargo.toml')
CARGO_TARGET_DIR = os.path.join(CARGO_ROOT_PATH, 'target')
os.environ['CARGO_TARGET_DIR'] = CARGO_TARGET_DIR

with io.open(os.path.join(PACKAGE_PATH, VERSION)) as f:
    version = f.readline()

with io.open(README, "rt", encoding="utf8") as f:
    readme = f.read()

required = [
    "future>=0.16,<2",
    "pathlib>=1.0,<2.0; python_version < '3.4'",
]

# The Rust library is loaded with ctypes (Binding.NoBinding): it does not link
# against Python, so one wheel per platform serves every Python 3 version.
# Set SNIPS_PREBUILT_DYLIB to a cross-compiled lib*.so to package it as a
# py3-none-<platform> wheel (use --plat-name), without building Rust here.
PREBUILT_DYLIB = os.environ.get("SNIPS_PREBUILT_DYLIB")
cmdclass = {}
setup_kwargs = {}
if PREBUILT_DYLIB:
    shutil.copy(PREBUILT_DYLIB,
                os.path.join(PACKAGE_PATH, "dylib", "lib%s_rs.so" % PACKAGE_NAME))
    rust_extensions = []
    try:
        from setuptools.command.bdist_wheel import bdist_wheel
    except ImportError:
        from wheel.bdist_wheel import bdist_wheel

    from setuptools.dist import Distribution

    class BinaryDistribution(Distribution):
        # Platform wheel: files go to the wheel root (platlib)
        def has_ext_modules(self):
            return True

    class PlatformWheel(bdist_wheel):
        def get_tag(self):
            _, _, plat = bdist_wheel.get_tag(self)
            return "py3", "none", plat

    cmdclass["bdist_wheel"] = PlatformWheel
    setup_kwargs["distclass"] = BinaryDistribution
else:
    from setuptools_rust import Binding, RustExtension

    rust_extensions = [RustExtension(
        RUST_EXTENSION_NAME, CARGO_FILE_PATH, debug="develop" in sys.argv,
        args=["--verbose"] if "--verbose" in sys.argv else None,
        binding=Binding.NoBinding)]

setup(name=PACKAGE_NAME,
      description="Python wrapper of the snips-nlu-parsers Rust crate",
      long_description=readme,
      version=version,
      license="Apache-2.0",
      author="Adrien Ball",
      author_email="adrien.ball@snips.ai",
      classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
      ],
      rust_extensions=rust_extensions,
      cmdclass=cmdclass,
      package_data={PACKAGE_NAME: ["dylib/*"]},
      install_requires=required,
      packages=packages,
      include_package_data=True,
      zip_safe=False,
      **setup_kwargs)
