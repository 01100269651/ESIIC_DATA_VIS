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
grouped_data = df.groupby('fact_nm')['fin_val_tot'].sum().reset_index()
grouped_data = grouped_data.sort_values(by='fin_val_tot', ascending=False)
st.title("📊 تقرير الرسوم")

plt.figure(figsize=(12, 8), facecolor='black')
colors = sns.color_palette('Set1', len(grouped_data))
# Group fin_val_tot by fact_nm and sum the values
grouped_data = df.groupby('fact_nm')['fin_val_tot'].sum().reset_index()
# Sort by fin_val_tot descending for better visual emphasis
grouped_data.sort_values(by='fin_val_tot', ascending=True, inplace=True)

# Reshape the Arabic labels for proper display
reshaped_labels = [get_display(arabic_reshaper.reshape(label)) for label in grouped_data['fact_nm']]

# Create an explode effect to highlight the largest slice

# Set up the figure with an improved style
plt.figure(figsize=(10, 10) , facecolor='black')

sns.set(style="darkgrid", font="Arial", font_scale=1.2)

ax,fig = plt.subplots(figsize=(12, 12), facecolor='black')
ax.set_facecolor('black')

wedges, texts, autotexts = plt.pie(
    grouped_data['fin_val_tot'],
    labels=reshaped_labels,
 
    autopct='%1.1f%%',
    startangle=90,
    counterclock=True,
    colors=plt.cm.seismic(np.linspace(0, 1, len(grouped_data))),
    labeldistance=1.1,
    textprops={'fontsize': 20, 'family': 'Arial', 'color': 'white'},
    wedgeprops={'edgecolor': 'white', 'linewidth': 2},
    shadow=True
)

# Add a white circle in the middle to create a donut effect
centre_circle = plt.Circle((0, 0), 0.70, fc='black')
plt.gcf().gca().add_artist(centre_circle)

# Add a descriptive title that includes the total inventory value
total_val = grouped_data['fin_val_tot'].sum()
title_text = f"{get_display(arabic_reshaper.reshape('أرصدة المصانع في شركة السكر ' + " "+ date_title))}"
plt.title(title_text, size=28, fontweight='bold', color='white', family='Arial', pad=20)


plt.text(0.45, 0.6, 'ESIIC',
         transform=plt.gcf().transFigure,  # بالنسبة للشكل كله
         fontsize=60,
         color='white',
         alpha=0.5,           # شفافية
         ha='center',
         va='center',
         rotation=30,         # ميل بسيط للناحية اليمنى
         fontweight='bold',
         family='arial')



# ----------------------------
watermark_text = get_display(arabic_reshaper.reshape("قطاع نظم المعلومات"))
plt.text(0.5, 0.5, watermark_text,
         transform=plt.gcf().transFigure,  # بالنسبة للشكل كله
         fontsize=60,
         color='white',
         alpha=0.5,           # شفافية
         ha='center',
         va='center',
         rotation=30,         # ميل بسيط للناحية اليمنى
         fontweight='bold')

plt.tight_layout()
st.pyplot(plt)



