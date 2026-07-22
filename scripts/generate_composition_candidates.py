#!/usr/bin/env python3
import argparse,json,pathlib
PROTOS=['full-bleed-hero-title-island','character-and-speech-bubble','object-closeup-with-petal-tags','diagonal-action','triptych-growth','emotion-closeup','storybook-window','constellation-labels']
def main():
  ap=argparse.ArgumentParser(); ap.add_argument('spec'); ap.add_argument('--art'); ap.add_argument('--out',required=True); args=ap.parse_args()
  spec=json.loads(pathlib.Path(args.spec).read_text(encoding='utf-8'))
  slides=spec.get('slides', spec if isinstance(spec,list) else [])
  candidates=[]
  for i,sl in enumerate(slides):
    sid=sl.get('slide_id') or sl.get('id') or f'S{i+1:02d}'
    role=sl.get('role','story')
    opts=[]
    for j,p in enumerate(PROTOS[i%len(PROTOS):i%len(PROTOS)+3] or PROTOS[:3]):
      opts.append({'candidate':chr(65+j),'prototype':p,'score':{'eye_path':8-j,'hierarchy':8,'emotion':7+j%2,'readability':8,'novelty':7},'reason':f'Candidate {chr(65+j)} varies rhythm for {role}.'})
    candidates.append({'slide_id':sid,'role':role,'candidates':opts,'selected':opts[0]['candidate']})
  pathlib.Path(args.out).write_text(json.dumps({'schema':'kv_kids_composition_candidates_v1','slides':candidates},ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__': main()
