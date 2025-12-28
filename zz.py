import  pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import arabic_reshaper
from matplotlib import font_manager
import sys
import seaborn as sns

import warnings as warnings 
from bidi.algorithm import get_display


df= pd.read_csv(r"goodmst112025.csv" )
df['fact_nm'] = df['factor_no']
warnings.filterwarnings('ignore')

total = df['fin_val_tot'].sum()
date_title = f"\n نوفمبر 2025 \n إجمالي أرصدة المصانع: {total:.2f} ألف جنيه "


df['fact_nm']=df['fact_nm'].replace({51: 'المركز الطبي'})
df['fact_nm']=df['fact_nm'].replace({52: 'مركزى قوص'})
df['fact_nm']=df['fact_nm'].replace({14: 'الاستخلاص'})
df['fact_nm']=df['fact_nm'].replace({15: 'الكيماويات'})
df['fact_nm']=df['fact_nm'].replace({19: 'النقل'})
df['fact_nm']=df['fact_nm'].replace({23: 'فينوس'})
df['fact_nm']=df['fact_nm'].replace({25: 'المعدات'})
df['fact_nm']=df['fact_nm'].replace({35: 'سكر ابوقرقاص'})
df['fact_nm']=df['fact_nm'].replace({36: 'تقطير ابوقرقاص'})
df['fact_nm']=df['fact_nm'].replace({37: 'بنجر ابوقرقاص'})
df['fact_nm']=df['fact_nm'].replace({40: 'نجع حمادى'})
df['fact_nm']=df['fact_nm'].replace({45: 'دشنا'})
df['fact_nm']=df['fact_nm'].replace({50: 'قوص'})
df['fact_nm']=df['fact_nm'].replace({55: 'ارمنت'})
df['fact_nm']=df['fact_nm'].replace({56: 'علف '})
df['fact_nm']=df['fact_nm'].replace({60: 'ادفو'})
df['fact_nm']=df['fact_nm'].replace({65: 'سكر كوم امبو'})
df['fact_nm']=df['fact_nm'].replace({66: 'خشب كوم امبو'})
df['fact_nm']=df['fact_nm'].replace({75: 'سكر وتكرير جرجا'})
df['fact_nm']=df['fact_nm'].replace({3: 'العطور'})
df['fact_nm']=df['fact_nm'].replace({4: 'التقطير'})
df['fact_nm']=df['fact_nm'].replace({5: 'التكرير'})
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import arabic_reshaper
from bidi.algorithm import get_display

st.title("📊 تقرير الرسوم")

plt.figure(figsize=(12, 8), facecolor='black')
colors = sns.color_palette('Set1', len(grouped_data))

plt.pie(
    grouped_data['fin_val_tot'],
    labels=reshaped_labels,
    colors=colors,
    autopct='%1.1f%%',
    startangle=90,
    textprops={'fontsize': 14, 'fontweight': 'bold', 'color': 'white'}
)

st.pyplot(plt)


