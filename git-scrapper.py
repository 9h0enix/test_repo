#
# a configuration file of type ini
# a git config parser
# pydriller
# input to the script would be given by config
# logger
# output Release-Details.txt
#

import configparser
from pydriller import *
import logging

def main():
    
    parser = configparser.ConfigParser()
    parser.read('git-scrapper.ini')
    
    #setting logger up 
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(levelname)s-%(name)s-%(message)s')
    
    file_handler=logging.FileHandler('git-scrapper.log')
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    repo=parser['GIT-SCRAPPER']['repo']
    fromTag=parser['GIT-SCRAPPER']['fromTag']
    ToTag=parser['GIT-SCRAPPER']['ToTag']
    Outputfilename=parser['GIT-SCRAPPER']['OutputFile']
   
    logger.info('Using Repo : {}'.format(repo))
    logger.info('From Tag   : {}'.format(fromTag))
    logger.info('To Tag     : {}'.format(ToTag))
    logger.info('Output     : {}'.format(Outputfilename)) 
    
    for c in RepositoryMining(repo,from_tag=fromTag,to_tag=ToTag,only_in_branch='master',only_no_merge=True,).traverse_commits():
        print('hash : {}, committer : {}'.format(c.hash,c.committer.name))
        
  
     

if __name__ == '__main__':
    main() 
