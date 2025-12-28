import  pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import arabic_reshaper
from matplotlib import font_manager
import sys
import seaborn as sns

import warnings as warnings 
from bidi.algorithm import get_display
import streamlit as st

PASSWORD = "yaman"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    if st.session_state.password == PASSWORD:
        st.session_state.authenticated = True
    else:
        st.error("❌ كلمة السر غير صحيحة")

if not st.session_state.authenticated:
    st.title("🔐 تسجيل الدخول")
    st.text_input(
        "أدخل كلمة السر",
        type="password",
        key="password"
    )
    st.button("دخول", on_click=login)
    st.stop()   # ⛔ يوقف باقي الصفحة

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
factories = df['fact_nm'].unique()
num_factories = len(factories)

# تحديد عدد الصفوف والأعمدة للـsubplots
cols = 2
rows = (num_factories + cols - 1) // cols

fig, axes = plt.subplots(rows, cols, figsize=(24, 8 * rows), facecolor='black')

axes = axes.flatten()  # تحويلها لقائمة للتعامل بسهولة

sns.set_style("darkgrid")

for i, fact_name in enumerate(factories):
    ax = axes[i]
    ax.set_facecolor('black')

    # تجميع البيانات لكل مصنع
    grouped_data = df.query("fact_nm == @fact_name").groupby('good_nm')['fin_val_tot'].sum().reset_index()
    grouped_data = grouped_data.sort_values(by='fin_val_tot', ascending=True)

    reshaped_labels = [get_display(arabic_reshaper.reshape(lbl)) for lbl in grouped_data['good_nm']]

    # رسم الأعمدة
    bars = ax.bar(reshaped_labels, grouped_data['fin_val_tot'],
                  color=sns.color_palette('tab20', len(grouped_data)))

    # كتابة القيم فوق الأعمدة
    for bar, value in zip(bars, grouped_data['fin_val_tot']):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{int(value)}',
                ha='center', va='bottom', fontsize=10, fontweight='bold', color='white')

    # العنوان لكل مصنع
    total_million = int(grouped_data['fin_val_tot'].sum() / 1000)
    text = f"رصيد {fact_name} {total_million} مليون جنيه {date_title}"
    bidi_title = get_display(arabic_reshaper.reshape(text))
    ax.set_title(bidi_title, fontsize=14, color='white', fontweight='bold')

    ax.tick_params(axis='x', labelrotation=45, labelsize=10, colors='white')
    ax.tick_params(axis='y', colors='white')

# إخفاء أي subplot فاضي
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

# ----------------------------
# 2. إضافة العلامة المائية العامة
# ----------------------------
watermark_text = get_display(arabic_reshaper.reshape("قطاع نظم المعلومات"))
plt.text(0.5, 0.5, watermark_text,
         transform=plt.gcf().transFigure,
         fontsize=80, color='white', alpha=0.1,
         ha='center', va='center', rotation=30, fontweight='bold')

plt.text(0.48, 0.6, 'ESIIC',
         transform=plt.gcf().transFigure,
         fontsize=80, color='white', alpha=0.1,
         ha='center', va='center', rotation=30, fontweight='bold', family='Arial')

plt.tight_layout()

# Ensure we don't exceed the maximum image dimension (2^16-1) when saving.
# Calculate a safe DPI based on figure size in inches so width_px and height_px <= 65535.
max_pixel = 2**16 - 1  # 65535
fig_width_in, fig_height_in = fig.get_size_inches()

# Maximum dpi allowed for each axis
max_dpi_w = int(max_pixel / fig_width_in) if fig_width_in > 0 else 300
max_dpi_h = int(max_pixel / fig_height_in) if fig_height_in > 0 else 300
max_allowed_dpi = max(1, min(max_dpi_w, max_dpi_h))

desired_dpi = 900
safe_dpi = min(desired_dpi, max_allowed_dpi)

# Ensure a reasonable minimum DPI
safe_dpi = max(safe_dpi, 72)
st.pyplot(plt)






