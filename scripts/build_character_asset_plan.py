#!/usr/bin/env python3
import argparse, json, pathlib
POSES=['greeting_wave','showing_flower','observing_flower','watering_action','waiting_thinking','surprise_discovery','happy_celebration','closing_thanks']
def main():
  ap=argparse.ArgumentParser(); ap.add_argument('art'); ap.add_argument('--out',required=True); args=ap.parse_args()
  art=json.loads(pathlib.Path(args.art).read_text(encoding='utf-8'))
  plan={'schema':'kv_kids_character_asset_plan_v1','title':art.get('title'),'character_id':'speaker_child_01','identity_lock':{'age':'4-6','hair':'brown hair with pink flower clip','outfit':'yellow top and denim overalls or user-provided outfit','style':'soft watercolor child illustration'},'required_poses':[{'pose':p,'usage':'one story node'} for p in POSES]}
  pathlib.Path(args.out).write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__': main()
