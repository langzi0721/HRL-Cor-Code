#!/usr/bin/env python3
"""Export exact text templates and FS60 grids for SI Tables S2/S4/S7/S10."""
import sys, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import pandas as pd
from hrlcor.data import load_dataset, DESCRIPTORS
from hrlcor.prompts import ED_PROMPTS,TEMPLATES,prompt_smiles,texts

def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'results')
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    frame=load_dataset()
    rows=[]
    for i in range(6):
        rows.append({'Configuration':f'ED{i}','Explicit_descriptors':'; '.join(DESCRIPTORS[i:]),
                     'Example_text_sent_to_API':texts(frame,f'qwen_ed{i}')[0]})
    pd.DataFrame(rows).to_csv(args.output/'S2_allocation_templates.csv',index=False)
    pd.DataFrame([{'Configuration':'ED3','Example_text_sent_to_API':texts(frame,'qwen_ed3')[0]},
                  {'Configuration':'SMILES','Example_text_sent_to_API':texts(frame,'qwen_smiles')[0]}]).to_csv(args.output/'S4_SMILES_templates.csv',index=False)
    pd.DataFrame([{'Template':x,'Example_text_sent_to_API':texts(frame,'qwen_ed3' if x=='A' else 'qwen_prompt_'+x)[0]}
                  for x in TEMPLATES]).to_csv(args.output/'S7_text_templates.csv',index=False)
    grids=json.loads((ROOT/'configs/hyperparameters.json').read_text())
    pd.DataFrame([{'Model':model,'Parameter':key,'Values':json.dumps(value)} for model,grid in grids.items() for key,value in grid.items()]).to_csv(args.output/'S10_hyperparameters.csv',index=False)
    print('Exported S2/S4/S7/S10 templates/grids, without any API calls:',args.output)

if __name__=='__main__':main()
