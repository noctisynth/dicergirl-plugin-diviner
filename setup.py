import setuptools
import sys

from pathlib import Path

sys.path.append(str((Path("dicergirl").resolve() / "plugins")))

import diviner

setuptools.setup(
    name="dicergirl-plugin-diviner",
    version=diviner.__version__,
    author="苏向夜 <fu050409@163.com>",
    author_email="fu050409@163.com",
    description="DicerGirl 占卜插件",
    url="https://gitee.com/unvisitor/dicergirl-plugin-diviner/",
    project_urls={
        "Bug Tracker": "https://gitee.com/unvisitor/dicergirl-plugin-diviner/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    license="Apache-2.0",
    packages=["dicergirl.plugins.diviner"],
    install_requires=[
        "dicergirl",
    ],
    python_requires=">=3",
)
