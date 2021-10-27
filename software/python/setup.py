from setuptools import setup, find_packages

setup(
    name='TorqueLimitedSimplePendulum',
    author='Underactuated Lab DFKI Robotics Innovation Center Bremen',
    version='1.0.0',
    url="https://github.com/dfki-ric-underactuated-lab",
    packages=find_packages(),
    install_requires=[
        # general
        'numpy',
        'pyyaml',
        'pandas',
        'argparse',
        'scipy',
        'sympy',

        # reinforcement learning
        'tensorflow',
        'stable_baselines3'
    ],
    classifiers=[
          'Development Status :: 5 - Stable',
          'Environment :: Console',
          'Intended Audience :: Academic Usage',
          'Programming Language :: Python',
          ],
)
