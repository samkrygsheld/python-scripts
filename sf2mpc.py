#!/usr/bin/python3

import os, pathlib, sys, argparse
from PIL import Image, ImageDraw, ImageEnhance, ImageOps

def sf2mpcOF(image, output, dir, type, bcolor):
    # Remove old border
    image = image.crop((33,36,638,898))

    # Resize
    image = image.resize((678,972), Image.ANTIALIAS)

    # Add new border
    image = ImageOps.expand(image,border=72,fill=bcolor)

    return image

def sf2mpcMF(image, output, dir, type, bcolor):
    # Remove old border
    image = image.crop((26,26,646,910))

    # Resize
    image = image.resize((690,984), Image.ANTIALIAS)

    # Add new border
    image = ImageOps.expand(image,border=66,fill=bcolor)

    # Cover the copyright text
    draw = ImageDraw.Draw(image)

    if 'creature' in type:
        draw.rectangle([(476,1024), (740, 1049)], fill = (23,20,15) )
    else:
        draw.rectangle([(480,1008), (740, 1040)], fill = (23,20,15) )

    # Round off the top corners
    draw.line((66, 66, 74, 66), fill=bcolor)
    draw.line((66, 67, 72, 67), fill=bcolor)
    draw.line((66, 68, 69, 68), fill=bcolor)
    draw.line((66, 69, 68, 69), fill=bcolor)
    draw.line((66, 70, 68, 70), fill=bcolor)
    draw.line((66, 71, 67, 71), fill=bcolor)
    draw.line((66, 72, 67, 72), fill=bcolor)
    draw.line((66, 73, 66, 73), fill=bcolor)

    draw.line((747, 66, 755, 66), fill=bcolor)
    draw.line((749, 67, 756, 67), fill=bcolor)
    draw.line((752, 68, 757, 68), fill=bcolor)
    draw.line((753, 69, 758, 69), fill=bcolor)
    draw.line((753, 70, 759, 70), fill=bcolor)
    draw.line((754, 71, 760, 71), fill=bcolor)
    draw.line((754, 72, 761, 72), fill=bcolor)
    draw.line((755, 73, 762, 73), fill=bcolor)

    return image

def sf2mpc(input, output, dir, frame, type, bcolor):
    image = Image.open(input)

    # Adjust brightness
    image = ImageEnhance.Brightness(image).enhance(1.07)

    if 'modern' in frame:
        image = sf2mpcMF(image, output, dir, type, bcolor)
    else:
        image = sf2mpcOF(image, output, dir, type, bcolor)

    # Save new image
    if not os.path.exists(dir):
        os.makedirs(dir)

    if output.endswith('.png'):
        image.save(dir + output)
    else:
        image.save(dir + output + '.png')

def main():
    parser = argparse.ArgumentParser(description='Converts a scryfall image to MPC.')
    parser.add_argument("-a", "--all", help="convert all images in current directory", action='store_true')
    parser.add_argument("-i", "--input", help="input file")
    parser.add_argument("-o", "--output", default='out.png', help="output file")
    parser.add_argument("-dir", "--dir", default='./out/', help="output directory")
    parser.add_argument("-f", "--frame", default='spell', help='frame type (original, modern, full)')
    parser.add_argument("-t", "--type", default='spell', help='card type (creature, other)')
    parser.add_argument("-b", "--bcolor", default='black', help='border color')

    if len(sys.argv[1:])==0:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()

    if (args.all):
        for image in pathlib.Path('./').glob('*.jpg'):
            sf2mpc(image, image.stem + ".png", args.dir, args.frame, args.type, args.bcolor)    
    else:
        sf2mpc(args.input, args.output, args.dir, args.frame, args.type, args.bcolor)

if __name__== "__main__":
  main()

