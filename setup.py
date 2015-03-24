from setuptools import setup

#http://docs.python.org/2/distutils/setupscript.html

setup(
    name='heroics',
    version='0.1.1',

    author='dev',
    author_email='dev@agutong.com',
    url='http://git.agutong.com/dev/heroics',

    license='LICENSE',
    description='heroics',
    long_description=open('README.md').read(),

    packages=[
      'heroics',
    ],

    package_data = {
        #'heroics': ['config/*.yml'],
    },

    data_files=[
        #('/etc/init.d', ['bin/init-heroics'])
    ],

    scripts=[
        'bin/heroics-py'
    ],

    install_requires=[
        #"Django >= 1.1.1",
    ],

    dependency_links=[
        #zip/tar urls
    ]
)
