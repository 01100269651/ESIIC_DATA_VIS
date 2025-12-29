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
grouped_data = df.groupby('fact_nm')['fin_val_tot'].sum().reset_index()
grouped_data = grouped_data.sort_values(by='fin_val_tot', ascending=True)

st.set_page_config(layout="wide")
st.title("📊 تقرير المصانع التفاعلي")

# ===== مثال بيانات (استبدلها ببياناتك) =====
# df = pd.read_excel("data.xlsx")


# إنشاء عمود للعرض (رقم المصنع + الاسم)
df['factory_display'] = df['factor_no'].astype(str) + ' - ' + df['fact_nm']

# selectbox يعرض الرقم والاسم
selected_factory = st.selectbox(
    "اختر المصنع",
    df['factory_display'].unique()
)

# استخراج رقم المصنع المختار فقط
factor_no  = int(selected_factory.split(' - ')[0])

grouped_data = (
    df.query('factor_no == @factor_no')
    .groupby('good_nm')['fin_val_tot']
    .sum()
    .reset_index()
    .sort_values(by='fin_val_tot', ascending=True)
)

reshaped_labels = [
    get_display(arabic_reshaper.reshape(str(label)))
    for label in grouped_data['good_nm']
]

# ===== مؤشرات سريعة =====
st.divider()
col_m1, col_m2 = st.columns(2)
with col_m1:
    st.metric("عدد بنود المخزون", len(grouped_data))
with col_m2:
    st.metric(
        "إجمالي الأرصدة",
        f"{grouped_data['fin_val_tot'].sum():,.0f}"
    )

st.divider()

# ===== الرسومات =====
col1, col2 = st.columns(2)

# ---- Pie Chart ----
with col1:
    st.subheader("📌 توزيع الأرصدة")

    fig1, ax1 = plt.subplots(figsize=(6, 6), facecolor='black')
    colors1 = sns.color_palette('tab20', len(grouped_data))

    ax1.pie(
        grouped_data['fin_val_tot'],
        labels=reshaped_labels,
        colors=colors1,
        autopct='%1.1f%%',
        startangle=90,
        
        textprops={'fontsize': 12, 'fontweight': 'bold', 'color': 'white'}
    )
    st.pyplot(fig1)

# ---- Bar Chart ----
with col2:
    st.subheader("📌 مقارنة الأرصدة")
   

    fig2, ax2 = plt.subplots(figsize=(6, 6))
    sns.barplot(
        x='fin_val_tot',
        y=reshaped_labels,
        data=grouped_data,
        palette='Set2',
        ax=ax2
    )
    ax2.set_xlabel("القيمة")
    ax2.set_ylabel("")
    st.pyplot(fig2)

st.divider()

# ===== جدول =====
st.subheader("📋 جدول البيانات")
st.dataframe(grouped_data, use_container_width=True)


st.pyplot(plt)










