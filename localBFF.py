import sys
import logging
import argparse
from libLocalBFF.LocalBitTorrentFileFinder import LocalBitTorrentFileFinder

parser = argparse.ArgumentParser(description='Find the local files that are described in a BitTorrent metafile.')
parser.add_argument('-v', '--verbosity',
  help="level of console logging",
  dest='console_verbosity',
  choices=['DEBUG','INFO','ERROR','WARNING','CRITICAL'],
  default="INFO")
parser.add_argument('-l', '--log-verbosity',
  help="level of log file verbosity",
  dest='file_verbosity',
  choices=['DEBUG','INFO','ERROR','WARNING','CRITICAL'],
  default="INFO")
parser.add_argument('metafile', metavar='/path/to/torrentFile.torrent',
  help='a BitTorrent metafile')
parser.add_argument('contentDirectory', metavar='/path/to/contentDirectory',
  help='directory where files might be located')
args = parser.parse_args()

metafilePath = args.metafile.decode('utf-8')
contentDirectory = args.contentDirectory.decode('utf-8')

console_loglevel = args.console_verbosity
console_loglevel_num = getattr(logging, console_loglevel.upper(), None)
file_loglevel = args.file_verbosity
file_loglevel_num = getattr(logging, file_loglevel.upper(), None)

if not isinstance(console_loglevel_num, int):
  raise ValueError('Invalid console log level: %s' % console_loglevel)
if not isinstance(file_loglevel_num, int):
  raise ValueError('Invalid file log level: %s' % file_loglevel)

logging.basicConfig( level=file_loglevel_num,
  format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
  datefmt='%m-%d %H:%M',
  filename='/tmp/localBFF.log',
  filemode='w')

console = logging.StreamHandler()
console.setLevel(console_loglevel_num)
formatter = logging.Formatter('%(message)s')
console.setFormatter(formatter)
logging.getLogger('localBFF').addHandler(console)

service = LocalBitTorrentFileFinder( metafilePath=metafilePath, contentDirectory=contentDirectory )

service.processMetafile()

service.gatherAllFilesFromContentDirectory()

service.connectFilesInMetafileToPossibleMatchesInContentDirectory()

service.positivelyMatchFilesInMetafileToPossibleMatches()

for matchedFile in service.files:
  output = ""
  metafilePayloadFilePath = matchedFile.getPathFromMetafile()
  
  if matchedFile.status == 'NOT_CHECKED':
    output = "File not checked"
  elif matchedFile.status == 'MATCH_FOUND':
    output = matchedFile.getMatchedPathFromContentDirectory()
  elif matchedFile.status == 'CHECKED_WITH_NO_MATCH':
    output = "No matches found"
  
  print metafilePayloadFilePath + "\t->\t" + output
