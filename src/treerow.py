import re
import sys
from pathlib import Path
import logging, logging.config

# set logger
logging.config.fileConfig('logging_release.conf')
logger = logging.getLogger('log_treerow')



class TreeRow:
    """An Entry in a line"""
    p_entry = re.compile(r'^([├└─│ ]*)(.*)$')
    scale_space = 4

    def __init__(self, depth, name, ext):
        self.depth = depth
        self.name = name
        self.ext = ext
        self.full_name = name + ext
        
        logger.debug(
            "init: depth: {} full: '{}' name: '{}' ext: '{}'".format(
                self.depth, self.full_name, self.name, self.ext))

        assert self.full_name == self.name + self.ext, 'full name not right'

    def __repr__(self):
        return f"TreeRow({self.depth}, '{self.name}', '{self.ext}')"

    def __str__(self):
        return f"({self.depth}, '{self.name}', '{self.ext}')"

    def __eq__(self, other):
        if self.depth == other.depth and self.name ==  other.name and self.ext == other.ext:
            return True
        return False
        
    def is_file(self):
        return True if self.ext != '' else False

    def is_dir(self):
        return True if self.ext == '' else False

    @classmethod
    def from_str(cls, iStr):
        # replace any \t to 4 spaces
        iStr = re.sub(r'\t', ' ' * 4, iStr)

        # if no space in front, must be (relative) root dir
        if not iStr.startswith(' '):
            # iStr should be name of root dir, with no ext
            return cls(0, iStr, '')

        # not (relative) root dir
        m1 = re.match(TreeRow.p_entry, iStr)
        # m1.group(1) -> '    '; m1.group(2) -> 'name.ext'

        prefix = m1.group(1)

        # check indention is legal
        if len(prefix) % TreeRow.scale_space:
            # will not run if 0
            print('Error: Please check indentation')
            print('       At line:', iStr)
            sys.exit(1)

        depth = int(len(prefix) / TreeRow.scale_space)
        full_name = Path(m1.group(2))
        ext = ''.join(full_name.suffixes)
        name = full_name.name.replace(ext, '')

        return cls(depth, name, ext)

    @staticmethod
    def set_scale_space(x):
        TreeRow.scale_space = x


def main():
    pass

if __name__ == '__main__':
    main()
