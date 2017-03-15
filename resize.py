#!/usr/bin/python

import json
import re
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

    dirname = os.path.join(opt_output, 'ios')
    call(['mkdir', '-p', dirname])
    call(['cp', 'Contents.json', dirname])

    w, h = map(float, re.findall(r'^([\d.]+)x([\d.]+)$', img.get('size'))[0])
    scale = int(img.get('scale')[:-1])
    size = '{:.0f}x{:.0f}'.format(round(w * scale), round(h * scale))
    file_name = 'icon-{}.png'.format(size)

    cmd = [
        'convert', 
        opt_input,
        '-resize',
        size,
        os.path.join(dirname, file_name)
    ]
    print(' '.join(cmd))
    call(cmd)


# Android icons

data = [
    ('drawable-ldpi', 36),
    ('drawable-mdpi', 48),
    ('drawable-hdpi', 72),
    ('drawable-xhdpi', 96),
    ('drawable-xxhdpi', 144),
    ('drawable-xxxdpi', 192),
]

for scheme, size in data:

    dirname = os.path.join(opt_output, 'android', scheme)
    call(['mkdir', '-p', dirname])

    cmd = [
        'convert', 
        opt_input,
        '-resize',
        str(size),
        os.path.join(dirname, 'icon.png')
    ]
    print(' '.join(cmd))
    call(cmd)

