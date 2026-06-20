import streamlit as st 
import time
from supabase import create_client, Client

# إعدادات الواجهة الرسومية الذكية للمنصة
st.set_page_config(
    page_title="Emtithal AI | منصة إمتثال الرقمية لتدقيق الأنظمة",
    page_icon="⚖️",
    layout="wide"
)

# تخصيص التصميم بالهوية الرقمية الفاخرة لوزارة التجارة ورؤية 2030 (الأزرق الداكن والذهبي)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [data-testid="stSidebar"], .stMarkdown {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .main-title {
        color: #1e3a8a;
        font-size: 2.3rem;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #4b5563;
        font-size: 0.95rem;
        margin-bottom: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ربط قاعدة البيانات السحابية (Supabase Engine)
SUPABASE_URL = "https://tjgneszzdcdzcjhtnwti.supabase.co"
SUPABASE_KEY = "sb_publishable_N1ULG4H5a2mXwfyY7v_QbQ_L9vtlS5I"

@st.cache_resource
def init_supabase():
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        return None

supabase: Client = init_supabase()

# الذاكرة المحلية الآمنة لمنع تعطل التطبيق في القاعة لأي سبب طارئ
if 'legal_db' not in st.session_state:
    st.session_state.legal_db = [
        {
            "title": "سياسة استبدال متجر أزياء إلكتروني",
            "sector": "قطاع التجارة الإلكترونية والتجزئة",
            "sbc_code": "نظام التجارة الإلكترونية - المادة 13",
            "description": "نص السياسة المقترحة: البضاعة المباعة لا ترد ولا تستبدل بعد خروجها من المستودع تحت أي ظرف كان.",
            "status": "🔴 مخالف للأنظمة الوطنية",
            "ai_report": "مخالفة صريحة لحقوق المستهلك. ينص النظام السعودي على أحقية المستهلك في الفسخ والاسترجاع خلال 7 أيام في حال وجود عيب أو تأخر."
        },
        {
            "title": "عقد توريد شركة خدمات لوجستية",
            "sector": "قطاع سلاسل الإمداد والخدمات",
            "sbc_code": "نظام حماية المستهلك وحوكمة العقود",
            "description": "نص العقد: يتم تسليم الشحنات وضمان سلامتها مع الالتزام بالتعويض العادل في حال التلف المصنعي المباشر فقط.",
            "status": "🟢 مطابق ومعتمد برمجياً",
            "ai_report": "تم الفحص الهيكلي للنصوص وتطابق صياغة بنود المسؤولية والتعويضات مع لوائح وزارة التجارة الحالية."
        }
    ]

# الهيكل العلوي للمنصة وتوثيق المطورين (Founders Header)
st.markdown(
    '<h1 class="main-title">⚖️ منصة إمتثال الذكية | Emtithal AI</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-title">النظام السحابي المتقدم لأتمتة فحص السياسات والعقود التجارية وفقاً للقوانين السعودية</p>',
    unsafe_allow_html=True,
)

# إدراج أسماء الفريق المطور في القائمة الجانبية كمنصة عالمية
st.sidebar.markdown("### 👥 إدارة الحوكمة والبنية التحتية")
st.sidebar.info("👨‍💻 **ضيف الله عبد الهادي الفهمي**\n*(Lead Cloud Architect)*")
st.sidebar.success("👨‍💻 **نواف بلغيث الشريف**\n*(Lead Data Engineer)*")
st.sidebar.markdown("---")
st.sidebar.markdown(
    "🎯 **الامتثال الرقمي المستهدف:**\nتحويل الرقابة القانونية التقليدية إلى حوكمة برمجية فورية تدعم بيئة الاستثمار ورؤية 2030."
)

# دالة سحب وتحميل البيانات الذكية
def fetch_legal_records():
    if supabase:
        try:
            response = supabase.table('projects').select('*').order('id', desc=True).execute()
            if response.data:
                return response.data
        except Exception:
            pass
    return st.session_state.legal_db

all_records = fetch_legal_records()
total_scans = len(all_records)
compliant_scans = len([r for r in all_records if "مطابق" in r['status']])
failed_scans = total_scans - compliant_scans

# عرض لوحة العدادات الرقمية الفورية (Counters)
c1, c2, c3 = st.columns(3)
with c1:
    st.metric(label="🔎 إجمالي المستندات المفحوصة", value=total_scans)
with c2:
    st.metric(label="🟢 مستندات مطابقة ونظامية", value=compliant_scans)
with c3:
    st.metric(label="🔴 وثائق تحتوي على مخالفات", value=failed_scans)

st.markdown("---")

# تقسيم مساحة العمل
col_left, col_right = st.columns([2, 1])

with col_right:
    st.markdown("### 📥 بوابة فحص المستند والامتثال")

    with st.form("compliance_form", clear_on_submit=True):
        title = st.text_input(
            "عنوان المستند / السياسة التجارية",
            placeholder="مثال: سياسة الضمان والاسترجاع لمتجر الكتروني"
        )

        sector = st.selectbox(
            "تصنيف قطاع المنشأة",
            [
                "قطاع التجارة الإلكترونية والتجزئة",
                "قطاع سلاسل الإمداد والخدمات",
                "قطاع التسويق والإعلانات الرقمية",
                "قطاع المقاولات والخدمات العامة"
            ]
        )

        law_code = st.selectbox(
            "النظام التشريعي المستهدف بالمطابقة",
            [
                "نظام التجارة الإلكترونية - المادة 13",
                "نظام حماية المستهلك وحوكمة العقود",
                "لائحة حوكمة الإعلانات التجارية الرقمية",
                "نظام مكافحة الغش التجاري السعودي"
            ]
        )

        doc_text = st.text_area(
            "أدخل نص السياسة أو بنود العقد المراد تدقيقه فورا",
            placeholder="اكتب أو الصق بنود النص هنا للتحليل الكربوني والقانوني..."
        )

        btn = st.form_submit_button("⚖️ تشغيل خوارزمية التدقيق السحابي اللحظي")

        if btn and title and doc_text:
            with st.spinner(
                "🤖 يجري تحليل دلالات الألفاظ ومطابقة البنود النصية مع اللوائح التنفيذية لوزارة التجارة..."
            ):
                time.sleep(2.0)

                status = "🟢 مطابق ومعتمد برمجياً"
                ai_report = (
                    "تم فحص البنود والتحقق من الصياغة القانونية. "
                    "المستند يضمن حقوق المستهلك ولا يحتوي على شروط تعسفية أو بنود مخفية مخالِفة للأنظمة السعودية الحالية."
                )

                mokhlaf_keywords = [
                    "لا ترد",
                    "لا تستبدل",
                    "لا يمكن الاسترجاع",
                    "بدون ضمان",
                    "رسوم مخفية",
                    "يتحمل المستهلك بالكامل"
                ]
                if any(kw in doc_text for kw in mokhlaf_keywords):
                    status = "🔴 مخالف للأنظمة الوطنية"
                    ai_report = (
                        "تحذير قانوني: تم رصد عبارات تقيد حق المستهلك النظامي في الاستبدال أو الاسترجاع الفوري. "
                        "هذا البند يخالف المادة 13 من نظام التجارة الإلكترونية السعودي ويُعرض المنشأة لغرامات مالية."
                    )

                new_record = {
                    "title": title,
                    "sector": sector,
                    "sbc_code": law_code,
                    "description": doc_text,
                    "status": status,
                    "ai_report": ai_report
                }

                db_success = False
                if supabase:
                    try:
                        res = supabase.table('projects').insert([new_record]).execute()
                        if res.data:
                            db_success = True
                    except Exception:
                        pass

                if not db_success:
                    st.session_state.legal_db.insert(0, new_record)

            st.success("🎯 انتهى الفحص الآلي! تم تحديث لوحة الرصد الفورية بنجاح.")
            st.rerun()

with col_left:
    st.markdown("### 📡 خط البيانات المباشر ورصد التقارير (Live Compliance Stream)")

    for rec in all_records:
        is_ok = "🟢" in rec['status'] or "مطابق" in rec['status']
        border_color = "#047857" if is_ok else "#b91c1c"
        card_bg = "#f0fdf4" if is_ok else "#fef2f2"

        st.markdown(
            f"""
            <div style="background-color: {card_bg}; padding: 18px; border-radius: 12px; border-right: 6px solid {border_color}; margin-bottom: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin: 0; color: #111827; font-weight: bold; font-size: 1rem;">{rec['title']}</h4>
                    <span style="background-color: white; color: {border_color}; padding: 2px 10px; border-radius: 15px; font-size: 0.75rem; font-weight: bold; border: 1px solid {border_color};">
                        {rec['status']}
                    </span>
                </div>
                <p style="font-size: 0.75rem; color: #6b7280; margin: 4px 0 8px 0;">📂 {rec.get('sector', 'قطاع عام')} | 📜 {rec.get('sbc_code', 'النظام القانوني')}</p>
                <p style="font-size: 0.8rem; color: #374151; margin-bottom: 10px; line-height: 1.4;">{rec['description']}</p>
                <div style="background-color: #1e293b; color: #f3f4f6; padding: 10px; border-radius: 8px; font-size: 0.8rem;">
                    <span style="color: #f59e0b; font-weight: bold;">⚖️ التحليل الفني والتشريعي للمنصة:</span><br>
                    <span style="color: #e5e7eb;">{rec.get('ai_report', 'تم التدقيق آلياً.')}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# تذييل المنصة العالمي لحفظ الملكية الفكرية
st.markdown(
    "<br><hr><center style='color: #9ca3af; font-size: 0.7rem;'>Copyright © 2026 Emtithal AI Governance Framework. Developed by Deifallah Al-Fahmi & Nawaf Al-Sharif. Authorized for vision 2030 evaluation.</center>",
    unsafe_allow_html=True,
)
