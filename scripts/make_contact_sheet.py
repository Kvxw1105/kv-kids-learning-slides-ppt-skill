#!/usr/bin/env python3
import argparse, math
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
def main():
 p=argparse.ArgumentParser(); p.add_argument('images'); p.add_argument('output'); p.add_argument('--cols',type=int,default=4); a=p.parse_args(); files=sorted([x for x in Path(a.images).iterdir() if x.suffix.lower() in {'.png','.jpg','.jpeg','.webp'}])
 if not files: raise SystemExit('no images')
 thumbs=[]
 for i,f in enumerate(files,1):
  im=Image.open(f).convert('RGB'); im.thumbnail((400,225)); canvas=Image.new('RGB',(420,260),'white'); canvas.paste(im,((420-im.width)//2,10)); ImageDraw.Draw(canvas).text((10,238),f'{i:02d} {f.name}',fill='black'); thumbs.append(canvas)
 rows=math.ceil(len(thumbs)/a.cols); sheet=Image.new('RGB',(a.cols*420,rows*260),(235,235,235))
 for i,im in enumerate(thumbs): sheet.paste(im,((i%a.cols)*420,(i//a.cols)*260))
 sheet.save(a.output); print(a.output)
if __name__=='__main__': main()
