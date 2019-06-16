#
# Diff parsing logic
# Diff info : Added are to new file
#             Removed are from old file version
#             changed are represented as removed from old and added to new
# Task : We have to identify : Truly added,Truly removed and Truly changed
# Get List of Added & Removed lines
# NOTE : we are only doing it for ini files and the context will have to theirs
# For INI files
# Added will be a list of lines "lAdded"
# Removed will be a list of lines "lRemoved"
# Need a "MAP" for which will store (Section+Property_Key : Property_Value)
# Output will be "lTrulyAdded" "lTrulyRemoved" "lTrulyChanged"
# Iterated over lAdded : 
#       3 types of cases : 
#         1. Comments (starting with #) 
#         2. Sections (in the brakets [] ) 
#         3. Properties (Key = Value So they will have a '=' in between them)
#       If Comments : Ignore them, 
#       If Section  : Create a Section + Property_key Key and against it store Property_value
#       If Property : Create a Section + Property_key Key and against it store Property_value
# Now we have a list of structs that store the added information 
# Iterate over lRemoved
#       3 types of cases for removal:
#         1. Comments (starting with #) : Ignore them
#         2. Sections (in the brakets [])
#         3. Properties (Key = value so they will have a '=' in between them)
#       if Comments are removed : Ignore them
#       if Sections  is removed : add to truly removed list
#       if Property is removed : check if the same Section + Property combination is present already in Map
#                                           if Yes : Mark it to Truly Changed & Remove entry form map
#                                           if No  : Mark it to Truly Removed & Remove entry from map
#
# Once both list have been iterated what is left in the Map are Truly Added Entries in the ini file
# 
#

import git 
from unidiff import PatchSet

#comments on unidiff library
#Objects : Discription
#Line    : single diff line
#Hunk    : Each of the modified blocks of a file. @@ %d,%d %d,%d @@
#PatchedFile : Patch updated file, it is a list of Hunks.
#PatchSet: List of Patchedfile


import os

#from cStringIO import StringIO (this only works for python 2.x)
from io import StringIO


def parseDiff(diff_index):
  for diff in diff_index.iter_change_type('M'):
    if diff.a_path[-4:] == ".ini":
      diffs.append(diff)

  if diffs:
    for d in diffs:
      a_path = "--- " + d.a_rawpath.decode('utf-8')
      b_path = "+++ " + d.b_rawpath.decode('utf-8')

      # Get detailed info
      patchset = PatchSet(a_path + os.linesep + b_path + os.linesep + d.diff.decode('utf-8'))

      for hunk in patchset[0]:
        lAdded = [x for x in hunk.target_lines() if x.is_added and x.value[0] != '#' and x.value != '\n']
        lRemoved = [x for x in hunk.source_lines() if x.is_removed and x.value[0] != '#' and x.value != '\n']
        fx = lambda l : [x.value for x in l]
        print('ADDED')
        print(fx(lAdded))
        print('REMOVED')
        print(fx(lRemoved))
        
  



commit_sha1 = 'b431f7312a22cd0f5a0c280da2ab2fc216054eb2'
repo_directory_address = "/home/tarun/testrepo/test_repo"

repository = git.Repo(repo_directory_address)
commit = repository.commit(commit_sha1)
prev_commit_sha1 = commit_sha1 + '~1'
prev_commit = repository.commit(prev_commit_sha1)

diffs = []
diff_index = commit.diff(prev_commit, create_patch=True)
parseDiff(diff_index)
