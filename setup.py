import os

from setuptools import find_packages, setup
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
    version='0.0.1',
    author="NTrash",
    author_email='yinghui0214@163.com',
    description="An out-of-the-box lightweight asynchronous crawler framework",
    python_requires=">=3.7",
    long_description=read("README.md"),
    license="MIT",
    install_requires=requires,
    packages=find_packages(),
    include_package_data=True,  # 自动包含受版本控制(svn/git)的数据文件
    zip_safe=False,
    classifiers=[
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],



)