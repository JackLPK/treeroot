import logging, logging.config
from treerow import TreeRow
from pathlib import Path
import sys

# set logger
logging.config.fileConfig('logging_release.conf')
logger = logging.getLogger('log_treeroot')

def show_help():
    print("""\
    treeroot
        Creates directory structure based on given sample file
        
    Example
        treeroot ../file_for_structure.txt
        creates directory structure in current directory.
        
        treeroot ../file_for_structure.txt at_this_new_directory
        creates directory structure in a new  directory.
        
    """)

def grow_tree(input_file_path):

    # read structure file, cleaned
    tree_rows = []
    tree_stack = []
    with open(input_file_path, 'r') as f:
        for line in f:
            # cleaning
            curr_line = line
            curr_line = curr_line.replace('\t', ' '*4)
            curr_line = curr_line.rstrip('\n ')
            if curr_line and ('//' not in curr_line):
                # appended line will not be empty or comment
                tree_rows.append(TreeRow.from_str(curr_line))
                
        logger.info('Finished reading structure file.')

    # start making
    make_this = None
    for i, curr_row in enumerate(tree_rows):
        prev_row = None if i == 0 else tree_stack[-1]

        if curr_row.is_dir():
            # 
            if i != 0 and prev_row.depth >= curr_row.depth:
                for _ in range(prev_row.depth - curr_row.depth + 1):
                    logger.debug(f'POP: {tree_stack[-1]}')
                    tree_stack.pop()

            logger.debug(f'PUSH: {curr_row}')
            tree_stack.append(curr_row)
            # 
            make_this = Path(*[_.name for _ in tree_stack])
            
        elif curr_row.is_file():
            # 
            if prev_row.depth >= curr_row.depth:
                for _ in range(prev_row.depth - curr_row.depth + 1):
                    logger.debug(f'POP: {tree_stack[-1]}')
                    tree_stack.pop()
            # 
            make_this = Path(*[_.name for _ in tree_stack], 
                            curr_row.full_name)
        
        
        logger.info(f"Making '{make_this}'")
        logger.debug(f"ts: {tree_stack}")
        # touch or mkdir
        try:
            if make_this.suffixes:
                # expect returned list holds extentions
                make_this.touch()
                pass
            else:
                make_this.mkdir(parents=True, exist_ok=True)
                pass
        except OSError as e:
            print(e)
            _s = 'Abort: File or Folder name contains illegal characters ...'
            print(_s)
            logger.error(_s)
            sys.exit(1)
    

def main():

    try:
        # get paths
        input_file_path = sys.argv[1]
    except IndexError:
        logger.info('No argvs provided')
        show_help()
    else:
        grow_tree(input_file_path)
        
    logger.info('DONE')
    print('DONE')

if __name__ == '__main__':
    main()
