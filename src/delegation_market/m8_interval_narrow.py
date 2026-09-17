from m8_interval import *
def cert_narrow(out):
 vs=[D('.31')+D('.04')*D(i)/12 for i in range(13)];hs=[D('.85')+D('.30')*D(i)/8 for i in range(9)];ls=[D('.06')+D('.08')*D(i)/4 for i in range(5)];agg={h:[None]*4 for h in range(2,7)}
 for i in range(12):
  for j in range(8):
   for k in range(4):
    v=(vs[i],vs[i+1]);eh=(hs[j],hs[j+1]);el=(ls[k],ls[k+1])
    for h in agg:
     rf,af=run(v,eh,el,h,'FPA');rs,ass=run(v,eh,el,h,'SPA');dr=sub(rf,rs);da=sub(ass,af);vals=(dr[0],dr[1],da[0],da[1]);a=agg[h]
     for n,val in enumerate(vals):a[n]=val if a[n]is None else(min(a[n],val)if n%2==0 else max(a[n],val))
 rows=[{'H':h,'revenue_gap':[str(a[0]),str(a[1])],'allocation_gap':[str(a[2]),str(a[3])],'certified':a[0]>0 and a[2]>0}for h,a in agg.items()]
 d={'box':{'v':['.31','.35'],'eta_high':['.85','1.15'],'eta_low':['.06','.14']},'subboxes':384,'rows':rows,'method':'Rule-generated matrices; 70-digit outward intervals; exhaustive 12x8x4 subdivision.'};out.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2));assert all(x['certified']for x in rows)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);cert_narrow(p.parse_args().output)
