# app.py - Application Web Partagée (SaaS) Kâtib Oumoumi
import streamlit as st
from config_portails import PORTAILS
from ocr_engine import extract_document_data
from bot_rpa import start_cloud_autofill, submit_with_captcha
from PIL import Image
import os

st.set_page_config(
    page_title="Portail Kâtib Oumoumi Cloud",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration de la typographie arabe
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: 700; height: 3em; }
    .reportview-container .main .block-container { max-width: 1200px; }
</style>
""", unsafe_allow_html=True)

# Barre latérale : Informations Cabinet et CNDP
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=70)
    st.markdown("### مكتب الكاتب العمومي الذكي")
    st.caption("منصة سحابية مركزية لمعالجة وأتمتة الإجراءات الإدارية")
    st.divider()
    st.success("🔒 معالجة آمنة خاضعة لمقتضيات القانون 09-08 (CNDP)")
    st.info("💡 **طريقة العمل :**\n1. رفع الوثائق واستخراج المعطيات\n2. مراجعة وتعديل الحقول\n3. ملء المنصة تلقائياً\n4. التحقق البشري من الكود")

st.title("⚖️ منصة الأتمتة الإدارية الشاملة (Kâtib Co-Pilot Cloud)")

# Initialisation des états de session
if "client_data" not in st.session_state:
    st.session_state.client_data = {}
if "rpa_session" not in st.session_state:
    st.session_state.rpa_session = None

col1, col2 = st.columns([1, 1.2], gap="large")

# --- COLONNE GAUCHE : DÉPÔT ET OCR ---
with col1:
    st.subheader("1. تحميل وثائق المرتفق (OCR الذكي)")
    
    uploaded_file = st.file_uploader(
        "اسحب صورة بطاقة التعريف الوطنية أو الوثيقة الإدارية :",
        type=["png", "jpg", "jpeg", "pdf"]
    )

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="معاينة الوثيقة المرفوعة", use_container_width=True)
        
        if st.button("🔍 بدء استخراج المعطيات من الوثيقة"):
            with st.spinner("⏳ جاري الفحص والتعرف الرقمي على الحقول..."):
                st.session_state.client_data = extract_document_data(uploaded_file)
                st.toast("✅ تم استخراج البيانات بنجاح!", icon="🎉")
    else:
        if st.button("⚡ ملء بيانات تجريبية فورية (Démo)"):
            st.session_state.client_data = extract_document_data(None)
            st.rerun()

# --- COLONNE DROITE : CONTRÔLE HUMAIN & RPA ---
with col2:
    st.subheader("2. مراجعة المعطيات وتحديد الخدمة (Supervision)")

    service_key = st.selectbox(
        "حدد الإجراء الإداري المراد تنفيذه :",
        options=list(PORTAILS.keys()),
        format_func=lambda k: PORTAILS[k]["nom"]
    )
    service_cfg = PORTAILS[service_key]

    c = st.session_state.client_data

    # Formulaire de révision humaine
    f1, f2 = st.columns(2)
    with f1:
        cnie = st.text_input("رقم البطاقة الوطنية (CNIE) :", value=c.get("cnie", ""))
        nom_fr = st.text_input("الاسم بالفرنسية :", value=c.get("nom_fr", ""))
        tel = st.text_input("الهاتف :", value=c.get("tel", ""))
    with f2:
        birthdate = st.text_input("تاريخ الازدياد :", value=c.get("birthdate", ""))
        nom_ar = st.text_input("الاسم بالعربية :", value=c.get("nom_ar", ""))
        extra = st.text_input("بيانات إضافية / اللوحة :", value=c.get("extra", ""))

    adresse = st.text_input("العنوان المصرح به :", value=c.get("adresse", ""))

    payload = {
        "cnie": cnie, "nom_ar": nom_ar, "nom_fr": nom_fr,
        "birthdate": birthdate, "adresse": adresse, "tel": tel,
        "extra": extra, "idcs": c.get("idcs", ""), "rib": c.get("rib", "")
    }

    st.markdown("<br>", unsafe_allow_html=True)

    # Bouton de lancement
    if st.button("🚀 ملء الاستمارة في المنصة الحكومية تلقائياً"):
        with st.spinner("⚡ الروبوت يتصل بالمنصة ويملأ الحقول في السيرفر..."):
            result = start_cloud_autofill(service_cfg, payload)
            
            if result.get("status") == "WAITING_HUMAN_VALIDATION":
                st.session_state.rpa_session = result
                st.success(f"✅ تم ملء {result['filled_fields']} حقول بنجاح!")
            else:
                st.error(f"حدث خطأ أثناء الاتصال: {result.get('message')}")

# --- ZONE INFÉRIEURE : ÉTAPE HUMAN-IN-THE-LOOP (CAPTCHA & FINALISATION) ---
if st.session_state.rpa_session:
    st.divider()
    st.subheader("3. التحقق البشري والمصادقة النهائية (Validation Sécurisée)")
    
    st.warning("🛡️ يتطلب النظام الحكومي إدخال رمز التحقق البشري لتأكيد الطلب وحفظه.")
    
    res_col1, res_col2 = st.columns([1.5, 1])
    
    with res_col1:
        captcha_img = st.session_state.rpa_session.get("captcha_image")
        if captcha_img and os.path.exists(captcha_img):
            st.image(captcha_img, caption="لقطة مباشرة من شاشة الموقع الحكومي", use_container_width=True)

    with res_col2:
        captcha_input = st.text_input("أدخل رمز التحقق الظاهر في الصورة (أو رمز SMS) :", placeholder="ex: 8945")
        
        if st.button("✅ تأكيد الإرسال النهائي واستخراج الوصل"):
            if captcha_input:
                with st.spinner("⏳ جاري تأكيد الطلب واستخراج الوصل الرسمي..."):
                    res = submit_with_captcha(st.session_state.rpa_session["playwright_session"], captcha_input)
                    if res.get("status") == "SUCCESS":
                        st.balloons()
                        st.success("🎉 اكتملت العملية بنجاح تام!")
                        if os.path.exists(res["receipt"]):
                            st.image(res["receipt"], caption="الوصل الرسمي الصادر من الإدارة", use_container_width=True)
                            with open(res["receipt"], "rb") as file:
                                st.download_button("📥 تحميل الوصل الرسمي للزبون", data=file, file_name="recu_officiel.png", mime="image/png")
                    else:
                        st.error("تعذر تأكيد الرمز، يرجى إعادة المحاولة.")
            else:
                st.warning("يرجى كتابة الرمز أولاً.")