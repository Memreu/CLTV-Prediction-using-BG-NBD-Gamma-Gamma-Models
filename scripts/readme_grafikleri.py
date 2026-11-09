"""BG-NBD × Gamma-Gamma CLTV hesaplarını notebook ile aynı şekilde yeniden yapar ve README grafiklerini üretir.

Kullanım:  python scripts/readme_grafikleri.py
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid", font="DejaVu Sans")
plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 110, "axes.titleweight": "bold", "axes.titlesize": 13,
    "axes.labelsize": 11, "axes.spines.top": False, "axes.spines.right": False,
})
BLUE="#2E5EAA"; RED="#C0392B"; ORANGE="#E67E22"; GREEN="#29A36A"; GREY="#8C8C8C"; GOLD="#F2A900"
def save(fig, path):
    fig.tight_layout(); fig.savefig(path, bbox_inches="tight", facecolor="white"); plt.close(fig); print("kaydedildi:", path)

import pandas as pd, numpy as np, datetime as dt
from lifetimes import BetaGeoFitter, GammaGammaFitter
R=str(Path(__file__).resolve().parents[1]); import os; os.makedirs(R+'/images',exist_ok=True)
df=pd.read_csv(R+'/data.csv')
def ot(d,v):
    q1,q3=d[v].quantile(.01),d[v].quantile(.99); i=q3-q1; return q1-1.5*i,q3+1.5*i
for c in ["order_num_total_ever_online","order_num_total_ever_offline","customer_value_total_ever_offline","customer_value_total_ever_online"]:
    lo,up=ot(df,c); df.loc[df[c]<lo,c]=round(lo,0); df.loc[df[c]>up,c]=round(up,0)
df["order_num_total"]=df.order_num_total_ever_online+df.order_num_total_ever_offline
df["customer_value_total"]=df.customer_value_total_ever_offline+df.customer_value_total_ever_online
for c in df.columns[df.columns.str.contains("date")]: df[c]=pd.to_datetime(df[c])
ad=dt.datetime(2021,6,1)
c=pd.DataFrame({"customer_id":df.master_id,
 "recency_cltv_weekly":(df.last_order_date-df.first_order_date).dt.days/7,
 "T_weekly":(ad-df.first_order_date).dt.days/7,"frequency":df.order_num_total,
 "monetary_cltv_avg":df.customer_value_total/df.order_num_total,"channel":df.order_channel})
bgf=BetaGeoFitter(penalizer_coef=0.001).fit(c.frequency,c.recency_cltv_weekly,c.T_weekly)
c["exp_sales_3_month"]=bgf.predict(12,c.frequency,c.recency_cltv_weekly,c.T_weekly)
c["exp_sales_6_month"]=bgf.predict(24,c.frequency,c.recency_cltv_weekly,c.T_weekly)
ggf=GammaGammaFitter(penalizer_coef=0.01).fit(c.frequency,c.monetary_cltv_avg)
c["exp_average_value"]=ggf.conditional_expected_average_profit(c.frequency,c.monetary_cltv_avg)
c["cltv"]=ggf.customer_lifetime_value(bgf,c.frequency,c.recency_cltv_weekly,c.T_weekly,c.monetary_cltv_avg,time=6,freq="W",discount_rate=0.01)
c["seg"]=pd.qcut(c.cltv,4,labels=["D","C","B","A"])
s=c.groupby("seg",observed=True).agg(cltv=("cltv","mean"),sales=("exp_sales_6_month","mean"),val=("exp_average_value","mean"),n=("cltv","size"),tot=("cltv","sum"))
print(s.round(2)); print("total cltv",c.cltv.sum(), "A share", s.loc["A","tot"]/c.cltv.sum())
print("median",c.cltv.median(),"mean",c.cltv.mean(),"max",c.cltv.max())
print(c.groupby("channel").cltv.agg(["mean","median","size"]).round(1))
print("top 10% share", c.cltv.nlargest(len(c)//10).sum()/c.cltv.sum())
print("exp 3m total", c.exp_sales_3_month.sum(), "6m", c.exp_sales_6_month.sum())
print(bgf.params_, ggf.params_)
pal={"A":GREEN,"B":BLUE,"C":ORANGE,"D":RED}
order=["A","B","C","D"]
# fig1
fig,ax=plt.subplots(1,3,figsize=(16,4.6))
for a,(col,t,fmt) in zip(ax,[("cltv","Ortalama 6 aylık CLTV","{:.0f}"),("sales","Beklenen 6 aylık satın alma","{:.2f}"),("val","Beklenen ortalama sepet değeri","{:.0f}")]):
    v=s.loc[order,col]; b=a.bar(order,v,color=[pal[o] for o in order],width=.62)
    for r,x in zip(b,v): a.text(r.get_x()+r.get_width()/2,x*1.01,fmt.format(x),ha="center",va="bottom",fontsize=10)
    a.set_title(t); a.set_xlabel("CLTV segmenti"); a.set_ylim(0,v.max()*1.15)
save(fig,R+'/images/01_segment_ozeti.png')
# fig2 distribution + scatter
fig,ax=plt.subplots(1,2,figsize=(15,5))
bins=np.logspace(np.log10(max(c.cltv.min(),5)),np.log10(c.cltv.max()),60)
for o in order[::-1]:
    ax[0].hist(c.loc[c.seg==o,"cltv"],bins=bins,color=pal[o],alpha=.85,label=f"{o} (ort. {s.loc[o,'cltv']:.0f})")
ax[0].set_xscale("log"); ax[0].set_title("6 aylık CLTV dağılımı ve segment sınırları"); ax[0].set_xlabel("CLTV (log ölçek)"); ax[0].set_ylabel("Müşteri sayısı"); ax[0].legend(title="Segment")
smp=c.sample(6000,random_state=1)
for o in order[::-1]:
    d=smp[smp.seg==o]; ax[1].scatter(d.exp_sales_6_month,d.exp_average_value,s=9,alpha=.55,color=pal[o],label=o)
ax[1].set_yscale("log"); ax[1].set_xlabel("Beklenen 6 aylık satın alma (BG-NBD)"); ax[1].set_ylabel("Beklenen sepet değeri (Gamma-Gamma, log)")
ax[1].set_title("CLTV = sıklık × değer: segmentler nasıl ayrışıyor?"); ax[1].legend(title="Segment",markerscale=2)
save(fig,R+'/images/02_cltv_dagilimi.png')
# fig3 BG-NBD frequency/recency matrix
from lifetimes.plotting import plot_probability_alive_matrix
fig,ax=plt.subplots(1,2,figsize=(15,5))
ch=c.groupby("channel").cltv.mean().sort_values()
ax[0].barh(ch.index,ch.values,color=BLUE); [ax[0].text(v+3,i,f"{v:.0f}",va="center") for i,v in enumerate(ch.values)]
ax[0].set_title("Kanala göre ortalama 6 aylık CLTV"); ax[0].set_xlabel("Ortalama CLTV"); ax[0].set_xlim(0,ch.max()*1.15)
sh=c.cltv.sort_values(ascending=False).cumsum()/c.cltv.sum(); xs=np.arange(1,len(sh)+1)/len(sh)*100
ax[1].plot(xs,sh.values*100,color=BLUE,lw=2.4); ax[1].plot([0,100],[0,100],ls="--",color=GREY)
for p in [10,25]:
    y=sh.values[int(len(sh)*p/100)-1]*100; ax[1].scatter([p],[y],color=RED,zorder=3); ax[1].annotate(f"En değerli %{p} → CLTV'nin %{y:.0f}'i",(p,y),xytext=(p+14,y-17),arrowprops=dict(arrowstyle="->",color=GREY))
ax[1].set_title("Değer yoğunlaşması (kümülatif CLTV payı)"); ax[1].set_xlabel("Müşterilerin yüzdesi (CLTV'ye göre sıralı)"); ax[1].set_ylabel("Toplam CLTV payı (%)")
save(fig,R+'/images/03_kanal_ve_yogunlasma.png')
