from setuptools import setup, find_packages

setup(name='hahaHba',
      version=2.0,
      author='oimq',
      url='https://github.com/oimq/hahaHba',
      author_email='taep0q@gmail.com',
      description='Mode easily handle the elasticsearch module',
      packages=find_packages(),
      install_requires=['elasticsearch', 'tqdm'],
      zip_safe=False
      )