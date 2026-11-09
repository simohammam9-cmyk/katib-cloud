# config_portails.py - Configuration des plateformes marocaines

PORTAILS = {
    "narsa": {
        "nom": "🚗 نارسا - نقل ملكية المركبات والبطاقة الرمادية (NARSA)",
        "url": "https://transfert.narsa.gov.ma",
        "description": "نقل ملكية السيارات، الدراجات، وإيداع الملفات",
        "champs": {
            "cnie": ["#cin", "#cnie", "input[name*='cin']", "#identifiant"],
            "nom_fr": ["#nom", "input[name*='nom']", "#nom_demandeur"],
            "adresse": ["#adresse", "input[name*='adresse']"],
            "tel": ["#telephone", "#tel", "input[name*='phone']"],
            "extra": ["#immatriculation", "#matricule", "input[name*='immat']"]
        }
    },
    "daam": {
        "nom": "💰 الدعم الاجتماعي المباشر والسجل الموحد (Asdaam.ma)",
        "url": "https://www.asdaam.ma",
        "description": "التسجيل في برنامج الدعم المباشر للأسر",
        "champs": {
            "cnie": ["#cnie", "#num_cnie", "input[name*='cnie']"],
            "idcs": ["#idcs", "#identifiant_social", "input[name*='idcs']"],
            "birthdate": ["#date_naissance", "input[type='date']"],
            "tel": ["#gsm", "#tel", "input[name*='tel']"],
            "rib": ["#rib", "#compte_bancaire", "input[name*='rib']"]
        }
    },
    "passeport": {
        "nom": "📘 جواز السفر البيومتري المغربي (Passeport.ma)",
        "url": "https://www.passeport.ma",
        "description": "تعبئة طلب الحصول على أو تجديد جواز السفر",
        "champs": {
            "cnie": ["#cnie", "#cin", "input[name*='cin']"],
            "nom_ar": ["#nom_ar", "input[name*='nom_ar']"],
            "nom_fr": ["#nom_fr", "input[name*='nom_fr']"],
            "birthdate": ["#date_naiss", "input[name*='birth']"],
            "adresse": ["#adresse", "input[name*='adresse']"]
        }
    },
    "watiqa": {
        "nom": "📜 وثيقة - طلب عقود ورسوم الولادة (Watiqa.ma)",
        "url": "https://www.watiqa.ma",
        "description": "طلب مستخرجات ورسوم الحالة المدنية",
        "champs": {
            "cnie": ["#cin", "#cnie"],
            "nom_fr": ["#nom", "#demandeur"],
            "tel": ["#telephone", "#gsm"],
            "extra": ["#num_acte", "#registre"]
        }
    }
}