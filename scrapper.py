import configparser
from pydriller import *
import logging


def SetupLogger(filename):
    """
        set up logger
    """ 
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s-%(name)s-%(message)s')
    file_handler=logging.FileHandler(filename)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

SetupLogger('git-scrapper.log')

def parseCommitMsg(message):
    """
        Message Format

        JIRAID : MAV-1234
        Commiter: XYZ
        Reviewer: ABC
        Discription : This is a Dummy Format
        Compiletime : 10.30
    """
    logger = logging.getLogger(__name__)
    return {x.split(':')[0].strip().upper():x.split(':')[1].strip() for x in message.split('\n') if x.find(':') != -1}


def parseDiff(diff):
    pass



def main():
    
    parser = configparser.ConfigParser()
    parser.read('git-scrapper.ini')
    
    repo=parser['GIT-SCRAPPER']['repo'].strip()
    fromTag=parser['GIT-SCRAPPER']['fromTag'].strip()
    ToTag=parser['GIT-SCRAPPER']['ToTag'].strip()
    Outputfilename=parser['GIT-SCRAPPER']['OutputFile']
   
    if fromTag == '':
        fromTag = None
    if ToTag == '':
        ToTag = None
    
    
    logger = logging.getLogger(__name__)
    logger.info('Using Repo : {}'.format(repo))
    logger.info('From Tag   : {}'.format(fromTag))
    logger.info('To Tag     : {}'.format(ToTag))
    logger.info('Output     : {}'.format(Outputfilename)) 
    
    for c in RepositoryMining(repo,from_tag=fromTag,to_tag=ToTag,only_in_branch='master',only_no_merge=True,).traverse_commits():
        print('hash : {}, committer : {}'.format(c.hash,c.committer.name))
        parseCommitMsg(c.msg)
        
if __name__ == '__main__':
    main() 
