from setuptools import setup , find_packages

install_requires = []

dev_requires = [
  'pip-tools~=4.5',
  'pytest~=6.1',
]

setup(
  name='trustpilot-anagram-challenge',
  version='0.0.1',
  author='Piotr Kubicki',
  author_email='pkubicki44@gmail.com',
  description='Solution for Trustpilot anagram challenge',
  packages=find_packages(),
  include_package_data=True,
  platforms='any',
  install_requires=install_requires,
  setup_requires=['pytest-runner'],
  tests_require=dev_requires,
  extras_require={
    'dev': dev_requires,
  }
)
