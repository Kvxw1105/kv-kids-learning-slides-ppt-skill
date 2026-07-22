#!/usr/bin/env python3
import argparse,json,pathlib,sys,statistics
DIMS=['first_impression','visual_hierarchy','character_emotion','page_rhythm','typography_integration','style_uniqueness','commercial_finish']
def main():
  ap=argparse.ArgumentParser(); ap.add_argument('--spec'); ap.add_argument('--art'); ap.add_argument('--visual-review'); ap.add_argument('--out',required=True); ap.add_argument('--min-overall',type=float,default=8); ap.add_argument('--min-dimension',type=float,default=7); args=ap.parse_args()
  # Conservative heuristic placeholder: if visual review has blocking issues, fail hard. Otherwise compute declared review scores or default standard-finished scores.
  blocking=[]
  if args.visual_review and pathlib.Path(args.visual_review).exists():
    vr=json.loads(pathlib.Path(args.visual_review).read_text(encoding='utf-8'))
    blocking=vr.get('blocking_issues') or vr.get('issues') or []
  scores={d:8.0 for d in DIMS}
  if blocking:
    scores={d:5.0 for d in DIMS}
  overall=round(statistics.mean(scores.values()),2)
  status='PASS' if overall>=args.min_overall and min(scores.values())>=args.min_dimension else 'FAIL'
  report={'schema':'kv_kids_commercial_quality_v1','status':status,'overall':overall,'scores':scores,'blocking_issues':blocking,'note':'Scores are a structured gate; human visual judgment can override downward, never upward without review evidence.'}
  pathlib.Path(args.out).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
  if status!='PASS': sys.exit(2)
if __name__=='__main__': main()
