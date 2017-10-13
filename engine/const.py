import os
from pipeline.const import *

__THIS = os.path.dirname(__file__)


def join(*args):
    return os.path.abspath(os.path.join(*args))


HOME_ICON = "home"
PROJECT_LIST_ICON = "database"
PROJECT_ICON = "archive"
DATA_LIST_ICON = "file text"
DATA_ICON = "file"
ANALYSIS_LIST_ICON = "settings"
ANALYSIS_ICON = "setting"
RESULT_LIST_ICON = "bar chart"
RESULT_ICON = "line chart"
FIELD_VISIBLE = "visible"
FIELD_ORIGIN = "origin"
PROJECT_ORIGIN = "PROJECT"

GENERIC_TYPE = 0
SAMPLE_TYPE = 1
COLLECTION_TYPE = 2
TAR_FASTQ_GZ = 3

DATA_TYPES = dict(
    GENERIC_TYPE=GENERIC_TYPE, SAMPLE_TYPE=SAMPLE_TYPE, COLLECTION_TYPE=SAMPLE_TYPE,
    TAR_FASTQ_GZ=TAR_FASTQ_GZ
)

#
# To initialize test files run:
#
# make testfile
#

TEST_PROJECTS = [
    ("Sequencing run 1", "Lamar sequencing center"),
    ("Sequencing run 2", "Lamar sequencing center"),
    ("Sequencing run 3", "Lamar sequencing center"),
]

TEST_FILE_PATH = os.path.expandvars('tmp/sampleinfo.txt')
TEST_COLL_PATH = os.path.expandvars('tmp/data.tar.gz')
TEST_DATA = [
    ("Data Collection 1", "This file contains a collection of data", TEST_COLL_PATH, TAR_FASTQ_GZ),
    ("Data Collection 2", "This file contains a collection of data", TEST_COLL_PATH, TAR_FASTQ_GZ),
    ("Sample sheet 1", "This file contains a sample sheet describing the data in the directory", TEST_FILE_PATH,
     SAMPLE_TYPE),
    ("Sample sheet 2", "This file contains a sample sheet describing the data in the directory", TEST_FILE_PATH,
     SAMPLE_TYPE),
]

TEST_SPECS = [
    join(__THIS, '..', 'pipeline', 'qc', 'qc_spec.hjson'),
    join(__THIS, '..', 'pipeline', 'fastqc', 'fastqc_spec.hjson')
]
