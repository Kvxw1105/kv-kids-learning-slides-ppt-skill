#!/usr/bin/env python3
import argparse, json, pathlib, hashlib

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('source')
    ap.add_argument('--out', required=True)
    ap.add_argument('--level', default='standard-finished')
    args=ap.parse_args()
    src=pathlib.Path(args.source)
    data=json.loads(src.read_text(encoding='utf-8')) if src.exists() else {}
    title=data.get('title') or data.get('speech_title') or data.get('topic') or 'Untitled child deck'
    art={
      'schema':'kv_kids_art_direction_v1',
      'delivery_level':args.level,
      'title':title,
      'core_emotion':'gentle wonder turning into warm confidence',
      'visual_metaphor':'a small flower becomes a stage companion for the child speaker',
      'signature_motif':'rounded watercolor flower-petal labels with soft green stems and pink accents',
      'palette_story':['cream paper','leaf green','soft rose','warm terracotta','sky blue'],
      'typography_voice':'English as warm display title, Chinese as equal companion line; no tiny subtitles',
      'page_rhythm':['establish','introduce','close-up','world opens','action','growth','emotion peak','clean farewell'],
      'forbidden_moves':['office rectangles','pure black Chinese title','random stickers','same layout for three consecutive slides','large blank area without visual role']
    }
    art['source_sha256']=hashlib.sha256(src.read_bytes()).hexdigest() if src.exists() else None
    pathlib.Path(args.out).write_text(json.dumps(art,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__': main()
