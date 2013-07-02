from distutils.core import setup

setup(
  name='LocalBitTorrentFileFinder',
  version='0.3alpha2',
  packages=['localbff',],
  scripts=['bin/localbff',],
  author='Doug McGeehan',
  author_email='djmvfb@mst.edu',
  url='https://bitbucket.org/torik/local-bittorrent-file-finder/wiki/Home',
  license='Python Software Foundation License',
  description='Hot, sexy, local BFFs want you to reseed your shit.',
  long_description=open('README.txt').read(),
  requires=[
    "argparse (>=1.2.1)",
    "bencode (==1.0)",
  ],
)
