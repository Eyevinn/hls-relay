from os.path import dirname, abspath, join, exists
from setuptools import setup

install_reqs = [req for req in open(abspath(join(dirname(__file__), 'requirements.txt')))]

setup(
    name = "hlsrelay",
    version = "0.0.1",
    author = "Jonas Birme",
    author_email = "jonas.birme@eyevinn.se",
    description = "A tool to pull live HLS stream from one origin and push to another origin",
    long_description="",
    license = "MIT",
    install_requires=install_reqs,
    url = "https://github.com/Eyevinn/hls-relay",
    packages = ['hlsrelay' ],
    entry_points = {
        'console_scripts': [
            'hls-relay=hlsrelay:main'
        ]
    }
)

