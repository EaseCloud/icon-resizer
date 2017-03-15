#!/usr/bin/python

import json
import sys
import os.path
from getopt import getopt, GetoptError
from subprocess import call


# Options Process

opt_input = 'icon.png'
opt_output = 'output'

help_text = """
resize.py -i <icon.png> -o <outpuy_dir>

options:

  -i --input: The input png file
  -o --output: The output directory
""";

try:
    opts, args = getopt(sys.argv[1:], 'hi:o:', ['help', 'input=', 'output='])
    print opts
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(help_text)
        elif opt in ('-i', '--input'):
            opt_input = arg
        elif opt in ('-o', '--output'):
            opt_output = arg
        else:
            'Option "{}" not supported'.format(opt)
            sys.exit(2)
except GetoptError:
    print(help_text)
    sys.exit(2)



# iOS icons

data = json.load(open('Contents.json'))

for img in data.get('images'):
    scale = img.get('scale')
    size = img.get('size')
    base_size = size[:size.find('x')]
    #img_size = int(int(scale[:-1]) * float(base_size))
    #file_name = 'icon-{}.png'.format(img_size)
    file_name = 'icon-{}.png'.format(size)
    # file_name = 'icon-{}@{}.png'.format(base_size, scale)

    dirname = opt_output + '/ios'

    call(['mkdir', '-p', dirname])
    call(['cp', 'Contents.json', dirname])

    cmd = [
        'convert', 
        opt_input,
        '-resize',
        size,
        os.path.join(dirname, file_name)
    ]
    print(' '.join(cmd))
    call(cmd)

