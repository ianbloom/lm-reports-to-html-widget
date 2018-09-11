from setuptools import setup

setup(name='personalprojects',
      version='1.0',
      description='Post LoMo reports as HTML Table in LoMo text widget',
      url='https://github.com/ianbloom/lm-reports-to-html-widget',
      author='ianbloom',
      author_email='ian.bloom@gmail.com',
      license='MIT',
      packages=['api_func'],
      install_requires=[
          'requests',
          'pandas'
      ],
      zip_safe=False)