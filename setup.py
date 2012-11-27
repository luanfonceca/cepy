from __future__ import print_function
import os.path
import re
from setuptools import setup


root = os.path.dirname(os.path.abspath(__file__))
package_name = 'cep'
try:
    p = __import__(package_name)
    package_version = p.__version__
except:
    package_version = 'UNKNOWN'


def read_requirements_file(rel_name):
    patn = re.compile('[<=>]')
    abs_name = os.path.join(root, rel_name)
    required = []
    try:
        req_file = open(abs_name, 'rb')
        for line in req_file:
            required.append(patn.split(line)[0])
        req_file.close()
    except IOError:
        pass  # ignore
    except Exception as e:
        print('Warning: failed to read requirements from', abs_name)
        print(e.__class__.__name__, e)
    return required

installation_requirements = read_requirements_file('requirements.txt')
testing_requirements = read_requirements_file('test-requirements.txt')

readme = ''
if not readme:
    for doc_name in ['README', 'readme.txt', 'readme.md', 'readme.rst']:
        if os.path.exists(os.path.join(root, doc_name)):
            readme_file = open(os.path.join(root, doc_name), 'rb')
            readme = '\n'.join(readme_file.readlines())
            readme_file.close()
            break

setup(
    name=package_name,
    version=package_version,
    #  url='<Your Repo/Project URL Here>',
    license='BSD',
    author='Luan Fonseca',
    author_email='luanfonceca@gmail.com',
    description='Just a mask for returning the address in json from Correios WebService',
    long_description=readme,
    packages=[package_name],
    zip_safe=False,
    platforms='any',
    install_requires=installation_requirements,
    tests_require=testing_requirements,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ],
    )

