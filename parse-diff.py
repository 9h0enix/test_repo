

from pydriller import RepositoryMining
from unidiff import *

for commit in RepositoryMining('/home/tarun/testrepo/test_repo').traverse_commits():
    for modification in commit.modifications:
        diff = modification.diff
        

