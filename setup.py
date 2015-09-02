from setuptools import setup, Command, find_packages
from setuptools.command.install import install
import os, glob, stat, sys

class ChmodXCommand(install):
    """Make /etc/init.d/gplayweb executable"""
    def run(self):
        install.run(self)
        # Make service executable
        st = os.stat('/etc/init.d/gplayweb')
        os.chmod('/etc/init.d/gplayweb', st.st_mode | stat.S_IEXEC)

templates = [f for f in glob.glob(os.path.join('templates','*'))]
fonts = [f for f in glob.glob(os.path.join('static/fonts','*'))]
css = [f for f in glob.glob(os.path.join('static/css','*'))]

setup(name='GPlayWeb',
        version='0.1.3.2',
        description='GPlayWeb, A GPlayCli web interface',
        author="Matlink",
        author_email="matlink@matlink.fr",
        url="https://github.com/matlink/gplayweb",
        license="AGPLv3",
        cmdclass={
            'install': ChmodXCommand,
        },
        scripts=['gplayweb'],
        data_files=[
            ['/etc/gplayweb/', ['gplayweb.conf.example']],
            ['/etc/init.d/', ['init_script/gplayweb']],
            ['/usr/share/gplayweb/templates', templates],
            ['/usr/share/gplayweb/static/css', css],
            ['/usr/share/gplayweb/static/fonts', fonts],
        ],
        install_requires=[
            'gplaycli',
            'tornado',
        ],
    )

