from setuptools import setup

setup(name='receiptor',
      version='0.2',
      description="A Telegram bot that sends you the ingredients of a recipe from foodsdictionary.co.il",
      url='http://github.com/assli100/receiptor',
      author='Matan Assli',
      author_email='matanasslizada@gmail.com',
      license='GPL',
      packages=['receiptor'],
      python_requires='>=3.9',
      zip_safe=False,
      install_requires=['python-telegram-bot>=21,<23', 'beautifulsoup4', 'requests'],
      entry_points={'console_scripts': ['receiptor=receiptor.main:main']})
