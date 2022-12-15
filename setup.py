import os
import re

from setuptools import find_packages, setup

_version_re = re.compile(r"__version__\s+=\s+(.*)")

def read_version():
    regexp = re.compile(r'^__version__\W*=\W*"([\d.abrc]+)"')
    init_py = os.path.join(os.path.dirname(__file__), "traspider", "__init__.py")
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)

def read(file_name):
    with open(
        os.path.join(os.path.dirname(__file__), file_name), mode="r", encoding="utf-8"
    ) as f:
        return f.read()



requires = [
            "aiohttp",
            "aiomysql",
            "aiosignal",
            "aiostream",
            "async-timeout",
            "asyncio",
            "attrs",
            "chardet",
            "charset-normalizer",
            "colorama",
            "frozenlist",
            "idna",
            "loguru",
            "lxml",
            "multidict",
            "node-vm2==0.3.5",
            "PyMySQL",
            "win32-setctime",
            "yarl",
        ]

setup(
    name="traspider",
    version=read_version(),
    author="NTrash",
    author_email='yinghui0214@163.com',
    description="An out-of-the-box lightweight asynchronous crawler framework",
    python_requires=">=3.7",
    long_description=read("README.md"),
    license="MIT",
    install_requires=requires,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
    entry_points={"console_scripts": ["traspider = traspider.commands.cmdline:execute"]},
)