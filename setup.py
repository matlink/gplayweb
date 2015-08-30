from setuptools import setup, Command, find_packages
import os, glob

templates = [f for f in glob.glob(os.path.join('templates','*'))]
fonts = [f for f in glob.glob(os.path.join('static/fonts','*'))]
css = [f for f in glob.glob(os.path.join('static/css','*'))]

setup(name='GPlayWeb',
        version='0.1',
        description='GPlayWeb, A GPlayCli web interface',
        author="Matlink",
        author_email="matlink@matlink.fr",
        url="https://github.com/matlink/gplayweb",
        license="AGPLv3",

        scripts=['gplayweb'],
        data_files=[
            ['/etc/gplayweb/', ['gplayweb.conf.example']],
            ['/usr/share/gplayweb/templates', templates],
            ['/usr/share/gplayweb/static/css', css],
            ['/usr/share/gplayweb/static/fonts', fonts],
        ],
        install_requires=[
            'gplaycli',
            'tornado',
        ],
    )
