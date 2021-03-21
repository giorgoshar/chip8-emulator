# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-statements
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=unused-import

import sys
import os
import os.path

REGEX_COMMENT = r''

with open('./GREET.ASM', 'r') as fp:
    for line in fp:
        print(line, end='')
