# -*- coding: utf-8 -*-
"""Resume content for Alexander Van Ness — the only file to edit for wording changes."""

NAME = "Alexander Van Ness"
CONTACT = "Avanness213@gmail.com · (216) 224-1918 · Cleveland, Ohio · avanness213.github.io"
TARGET = "PATIENT SUCCESS · PATIENT ENGAGEMENT · HEALTHCARE CUSTOMER SUPPORT · CUSTOMER SUCCESS"

SUMMARY = (
    "Licensed Massage Therapist and healthcare business owner with 15+ years of building long-term client relationships, "
    "coordinating care, and driving retention. Understands individual needs, communicates with empathy, handles sensitive "
    "information with discretion, and turns difficult interactions into positive outcomes. Seeking a remote Patient Success "
    "or Customer Success role in healthcare technology or a health system."
)

CORE_SKILLS = [
    "Patient & Client Support · Customer Success · Relationship Management · Patient Engagement · Service Recovery",
    "Appointment Coordination · Conflict Resolution · Retention · Confidential Information · Remote Communication",
]

JOBS = [
    (
        "Nordic Health Massage (Lifelong Bodywork)",
        "Owner · Licensed Massage Therapist · 2011 – Present · Cleveland, OH",
        [
            "Built and sustained an independent healthcare practice for 15+ years on personalized care and repeat-client "
            "retention — many clients retained for a decade or more.",

            "Own the complete client experience: initial inquiry, scheduling, service delivery, follow-up, referrals, and "
            "ongoing care. Memberships, treatment packages, and proactive follow-up drive recurring revenue.",

            "Translate complex health and treatment information into clear, actionable guidance while maintaining "
            "boundaries and confidentiality — for elderly, hospice, oncology, and acute-injury clients as well as pro athletes.",

            "Developed specialized medical, sports, injury-recovery, and combat-sports services; built lasting referral "
            "relationships with athletes, trainers, martial artists, and wellness professionals.",

            "Independently manage scheduling, customer support, billing, marketing, online booking, and day-to-day operations.",
        ],
    ),
    (
        "Kia of Bedford",
        "Sales Consultant · 2016 – 2017 · Bedford, OH",
        [
            "Converted internet and telephone leads into appointments and sales through needs-based communication and "
            "consistent follow-up; earned repeat and referral business by addressing concerns directly and staying responsive.",
        ],
    ),
    (
        "Motorcars Honda",
        "Sales Consultant · 2007 – 2009 · Cleveland, OH",
        [
            "Developed new customer relationships by phone, internet, and in person; increased customer confidence by "
            "simplifying complex options and resolving concerns before they became objections.",
        ],
    ),
    (
        "BD's Mongolian Grill",
        "Grill Captain · Team Leader · 1999 – 2006 · Cleveland, OH",
        [
            "Hired, trained, and coached employees while maintaining customer satisfaction and daily operations; built the "
            "communication foundation — tonality, body language, conversational control — used in every role since.",
        ],
    ),
]

CREDENTIALS = [
    "Licensed Massage Therapist, State of Ohio · Medical & Sports Massage · Injury Recovery · IASTM Techniques",
    "Life Coaching Certification · Goal Development · Accountability · Communication · Execution Strategies",
]

TECHNOLOGY = [
    "Online Scheduling & Booking · Electronic Client Records · Microsoft Office · Google Workspace · Phone / Email / Text",
    "Website Management · Social Media · Digital Marketing · Remote Communication Tools · AI Tools & Applications",
]

BULLET = "–"


def all_text():
    parts = [NAME, CONTACT, TARGET, SUMMARY, "SUMMARY", "CORE SKILLS", "EXPERIENCE", "CREDENTIALS", "TECHNOLOGY", BULLET]
    parts += CORE_SKILLS
    for company, meta, bullets in JOBS:
        parts += [company, meta] + bullets
    parts += CREDENTIALS + TECHNOLOGY
    return parts
