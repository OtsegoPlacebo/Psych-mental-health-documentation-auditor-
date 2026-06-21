
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Psych Mental Health Documentation Auditor",
    page_icon="🧠",
    layout="wide"
)

DISCLAIMER = """
Educational HIM/behavioral health documentation portfolio project only. This tool does not provide clinical,
legal, billing, compliance, or final coding advice. It is designed to demonstrate documentation quality review
concepts for counseling, psychology, and mental health records.
"""

PRIVACY_NOTE = """
Behavioral health records may require special privacy handling. Under HIPAA, psychotherapy notes receive
special protections when kept separate from the medical record. Substance use disorder treatment records may
also be subject to 42 CFR Part 2 protections. This app is an educational demonstration only.
"""

SAMPLE_CASES = {
    "Individual Therapy - Anxiety": {
        "note": "Client attended individual therapy for anxiety. Client reports increased worry at work. CBT techniques discussed. Client denied suicidal ideation. Follow up scheduled for next week.",
        "diagnosis": "Generalized anxiety disorder",
        "service": "Individual psychotherapy"
    },
    "Depression Follow-Up": {
        "note": "Client reports low mood and poor sleep. Discussed coping skills. Client will continue journaling. No safety concerns reported.",
        "diagnosis": "Depression",
        "service": "Counseling session"
    },
    "Family Counseling": {
        "note": "Family attended session to discuss communication issues. Therapist facilitated discussion and reviewed conflict resolution strategies. Family agreed to practice active listening.",
        "diagnosis": "Family relational problem",
        "service": "Family counseling"
    },
    "Crisis Risk Assessment": {
        "note": "Client reported feeling overwhelmed after relationship conflict. Suicide risk assessment completed. Client denied plan or intent. Safety plan reviewed. Crisis hotline and emergency instructions provided.",
        "diagnosis": "Adjustment disorder",
        "service": "Crisis assessment"
    },
    "Substance Use Counseling": {
        "note": "Client attended counseling for alcohol use concerns. Triggers discussed. Relapse prevention plan reviewed. Client agreed to attend support group. Follow up in two weeks.",
        "diagnosis": "Alcohol use disorder",
        "service": "Substance use counseling"
    }
}

CHECKS = {
    "Client presentation / reason for visit": ["client", "patient", "reports", "presented", "attended", "seen for"],
    "Session type / service provided": ["individual", "family", "group", "therapy", "counseling", "assessment", "psychotherapy"],
    "Symptoms or functional status": ["anxiety", "depression", "mood", "sleep", "worry", "functioning", "stress", "symptoms"],
    "Intervention or modality used": ["cbt", "dbt", "motivational", "intervention", "techniques", "psychoeducation", "facilitated", "coping"],
    "Client response / participation": ["client agreed", "participated", "engaged", "responded", "discussed", "reviewed"],
    "Progress toward treatment goals": ["progress", "goal", "goals", "improved", "continue", "practice", "journal"],
    "Risk assessment": ["suicidal", "suicide", "homicidal", "self-harm", "risk", "denied", "plan", "intent", "safety"],
    "Safety plan / crisis instructions": ["safety plan", "crisis", "hotline", "emergency", "return", "911", "instructions"],
    "Treatment plan / next steps": ["plan", "follow up", "scheduled", "continue", "next week", "two weeks", "homework"],
    "Consent / privacy sensitivity flag": ["consent", "confidential", "privacy", "release", "part 2", "substance use", "sud"]
}

def evaluate_note(note, diagnosis, service):
    note_lower = note.lower()
    present = []
    missing = []

    for element, keywords in CHECKS.items():
        if any(keyword in note_lower for keyword in keywords):
            present.append(element)
        else:
            missing.append(element)

    score = max(0, 100 - (len(missing) * 7))

    if score >= 90:
        risk = "Low Risk"
    elif score >= 70:
        risk = "Moderate Risk"
    else:
        risk = "High Risk"

    documentation_concerns = []
    compliance_privacy_flags = []
    provider_queries = []
    improvement_suggestions = []

    if not diagnosis.strip():
        documentation_concerns.append("Diagnosis or clinical impression is missing.")
    elif len(diagnosis.split()) <= 2:
        documentation_concerns.append("Diagnosis may need more specificity or supporting clinical detail.")

    if not service.strip():
        documentation_concerns.append("Service type is missing.")

    if "Symptoms or functional status" in missing:
        provider_queries.append("Please clarify symptoms, functional status, or presenting concern.")
        improvement_suggestions.append("Document symptoms and how they affect functioning.")

    if "Intervention or modality used" in missing:
        provider_queries.append("Please document the intervention, modality, or counseling technique used.")
        improvement_suggestions.append("Include modality such as CBT, DBT, motivational interviewing, psychoeducation, or supportive therapy when appropriate.")

    if "Client response / participation" in missing:
        provider_queries.append("Please clarify client response, engagement, or participation during the session.")
        improvement_suggestions.append("Document how the client responded to the intervention.")

    if "Progress toward treatment goals" in missing:
        provider_queries.append("Please clarify progress toward treatment goals.")
        improvement_suggestions.append("Connect the session note to the treatment plan or measurable goals.")

    if "Risk assessment" in missing:
        documentation_concerns.append("Risk assessment documentation may be incomplete.")
        provider_queries.append("Please document suicide/self-harm/homicide risk screening when clinically appropriate.")
        improvement_suggestions.append("Include risk assessment language, especially for depression, crisis, trauma, or safety-related visits.")

    if "Safety plan / crisis instructions" in missing:
        improvement_suggestions.append("Add safety plan, crisis resources, or return precautions when risk concerns are present.")

    if "Treatment plan / next steps" in missing:
        documentation_concerns.append("Treatment plan or follow-up documentation may be incomplete.")
        provider_queries.append("Please document next steps, follow-up timing, homework, or treatment plan updates.")
        improvement_suggestions.append("Include treatment plan, follow-up schedule, and assigned therapeutic activities.")

    if any(term in note_lower for term in ["substance", "alcohol", "drug", "opioid", "sud"]):
        compliance_privacy_flags.append("Possible SUD-related documentation. Review whether 42 CFR Part 2 protections apply.")
    if any(term in note_lower for term in ["psychotherapy notes", "process notes", "private notes"]):
        compliance_privacy_flags.append("Psychotherapy/process notes may require separation from the designated medical record.")
    if "Consent / privacy sensitivity flag" in missing:
        compliance_privacy_flags.append("No consent/privacy documentation detected by the rule-based review; verify requirements based on setting and record type.")

    if not documentation_concerns:
        documentation_concerns.append("No major documentation concern detected by the rule-based review.")
    if not compliance_privacy_flags:
        compliance_privacy_flags.append("No special privacy flag detected by the rule-based review.")
    if not provider_queries:
        provider_queries.append("No provider query suggested based on current rule checks.")
    if not improvement_suggestions:
        improvement_suggestions.append("Documentation appears generally complete based on current rule checks.")

    return {
        "audit_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "score": score,
        "risk": risk,
        "present": present,
        "missing": missing,
        "documentation_concerns": documentation_concerns,
        "privacy_flags": compliance_privacy_flags,
        "provider_queries": provider_queries,
        "improvement_suggestions": improvement_suggestions
    }

def create_report(note, diagnosis, service, result):
    lines = []
    lines.append("PSYCH MENTAL HEALTH DOCUMENTATION AUDITOR REPORT")
    lines.append("=" * 60)
    lines.append(f"Audit Date: {result['audit_date']}")
    lines.append(f"Diagnosis/Clinical Impression: {diagnosis}")
    lines.append(f"Service Type: {service}")
    lines.append(f"Documentation Quality Score: {result['score']}/100")
    lines.append(f"Risk Level: {result['risk']}")
    lines.append("")
    lines.append("NOTE REVIEWED")
    lines.append("-" * 60)
    lines.append(note)
    lines.append("")
    lines.append("PRESENT DOCUMENTATION ELEMENTS")
    lines.append("-" * 60)
    lines.extend([f"- {x}" for x in result["present"]] or ["- None detected"])
    lines.append("")
    lines.append("MISSING DOCUMENTATION ELEMENTS")
    lines.append("-" * 60)
    lines.extend([f"- {x}" for x in result["missing"]] or ["- None detected"])
    lines.append("")
    lines.append("DOCUMENTATION CONCERNS")
    lines.append("-" * 60)
    lines.extend([f"- {x}" for x in result["documentation_concerns"]])
    lines.append("")
    lines.append("PRIVACY / COMPLIANCE FLAGS")
    lines.append("-" * 60)
    lines.extend([f"- {x}" for x in result["privacy_flags"]])
    lines.append("")
    lines.append("SUGGESTED CLINICIAN QUERIES")
    lines.append("-" * 60)
    lines.extend([f"- {x}" for x in result["provider_queries"]])
    lines.append("")
    lines.append("IMPROVEMENT SUGGESTIONS")
    lines.append("-" * 60)
    lines.extend([f"- {x}" for x in result["improvement_suggestions"]])
    lines.append("")
    lines.append("DISCLAIMER")
    lines.append("-" * 60)
    lines.append(DISCLAIMER.strip())
    return "\n".join(lines)

st.sidebar.title("Project Menu")
page = st.sidebar.radio(
    "Choose a section",
    ["Run Audit", "Sample Cases", "Scoring Rubric", "Privacy Notes", "Portfolio Summary"]
)

st.sidebar.markdown("---")
st.sidebar.info("Created by Janyce Viero | HIM + Behavioral Health + AI Portfolio Project")

st.title("🧠 Psych Mental Health Documentation Auditor")
st.caption("Counseling, psychology, and behavioral health note review for documentation quality")
st.warning(DISCLAIMER)

if page == "Run Audit":
    st.header("Run Behavioral Health Documentation Audit")

    selected_case = st.selectbox("Load a sample case or choose blank input", ["Blank Input"] + list(SAMPLE_CASES.keys()))

    if selected_case != "Blank Input":
        default_note = SAMPLE_CASES[selected_case]["note"]
        default_diagnosis = SAMPLE_CASES[selected_case]["diagnosis"]
        default_service = SAMPLE_CASES[selected_case]["service"]
    else:
        default_note = ""
        default_diagnosis = ""
        default_service = ""

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Mental Health Documentation Input")
        note = st.text_area("Counselor / Psychologist Note", value=default_note, height=260)
        diagnosis = st.text_input("Diagnosis or Clinical Impression", value=default_diagnosis)
        service = st.text_input("Service Type", value=default_service)
        run = st.button("Run Mental Health Audit", type="primary")

    with col2:
        st.subheader("Audit Dashboard")

        if run:
            result = evaluate_note(note, diagnosis, service)

            m1, m2, m3 = st.columns(3)
            m1.metric("Quality Score", f"{result['score']}/100")
            m2.metric("Risk Level", result["risk"])
            m3.metric("Missing Elements", len(result["missing"]))

            st.progress(result["score"] / 100)

            st.markdown("### Documentation Elements")
            df = pd.DataFrame({
                "Element": result["present"] + result["missing"],
                "Status": ["Present"] * len(result["present"]) + ["Missing"] * len(result["missing"])
            })
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.markdown("### Documentation Concerns")
            for item in result["documentation_concerns"]:
                st.warning(item)

            st.markdown("### Privacy / Compliance Flags")
            for item in result["privacy_flags"]:
                st.info(item)

            st.markdown("### Suggested Clinician Queries")
            for item in result["provider_queries"]:
                st.write(f"- {item}")

            st.markdown("### Improvement Suggestions")
            for item in result["improvement_suggestions"]:
                st.success(item)

            report_text = create_report(note, diagnosis, service, result)
            st.download_button(
                label="Download Mental Health Audit Report",
                data=report_text,
                file_name="psych_mental_health_documentation_audit_report.txt",
                mime="text/plain"
            )
        else:
            st.info("Enter documentation and click Run Mental Health Audit.")

elif page == "Sample Cases":
    st.header("Sample Case Library")
    st.write("These cases are fictional and designed for portfolio demonstration.")

    rows = []
    for name, data in SAMPLE_CASES.items():
        result = evaluate_note(data["note"], data["diagnosis"], data["service"])
        rows.append({
            "Case": name,
            "Diagnosis": data["diagnosis"],
            "Service": data["service"],
            "Score": result["score"],
            "Risk": result["risk"],
            "Missing Elements": len(result["missing"])
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    case_name = st.selectbox("Select a case", list(SAMPLE_CASES.keys()))
    st.write("**Note:**")
    st.write(SAMPLE_CASES[case_name]["note"])
    st.write("**Diagnosis:**", SAMPLE_CASES[case_name]["diagnosis"])
    st.write("**Service:**", SAMPLE_CASES[case_name]["service"])

elif page == "Scoring Rubric":
    st.header("Scoring Rubric")
    st.write("The score begins at 100. Each missing documentation element subtracts 7 points.")

    rubric = pd.DataFrame({
        "Score Range": ["90-100", "70-89", "0-69"],
        "Risk Level": ["Low Risk", "Moderate Risk", "High Risk"],
        "Meaning": [
            "Documentation is generally complete based on selected behavioral health review elements.",
            "Documentation has gaps that may require clarification or improvement.",
            "Documentation has significant gaps that may affect continuity of care, compliance, or documentation support."
        ]
    })
    st.dataframe(rubric, use_container_width=True, hide_index=True)

    st.markdown("### Review Elements")
    for element in CHECKS.keys():
        st.write(f"- {element}")

elif page == "Privacy Notes":
    st.header("Behavioral Health Privacy Notes")
    st.info(PRIVACY_NOTE)

    st.markdown("""
    ### Key Concepts for Portfolio Demonstration

    **Progress notes** usually belong in the medical record and may include diagnosis, symptoms,
    functional status, treatment plan, prognosis, progress, session time, modality, and clinical test results.

    **Psychotherapy notes** are a special HIPAA category when they document or analyze the contents
    of counseling conversations and are kept separate from the medical record.

    **Substance use disorder records** may require additional protections under 42 CFR Part 2.

    This project does not determine legal obligations. It flags areas where a human HIM, compliance,
    or behavioral health professional should review documentation and privacy requirements.
    """)

elif page == "Portfolio Summary":
    st.header("Portfolio Summary")

    st.markdown("""
    ### Project Name
    **Psych Mental Health Documentation Auditor**

    ### Project Description
    Developed an AI-assisted behavioral health documentation review tool that evaluates counseling,
    psychology, and mental health notes for documentation completeness, treatment plan support,
    risk assessment, privacy sensitivity, and clinician query opportunities.

    ### Problem Addressed
    Behavioral health documentation must support quality care, continuity, compliance, treatment planning,
    and privacy requirements while avoiding unnecessary or improperly handled sensitive information.

    ### Tools Used
    - Python
    - Streamlit
    - Pandas
    - Health Information Management concepts
    - Behavioral health documentation review logic
    - AI-inspired rule-based workflow design

    ### Skills Demonstrated
    - Health Information Management
    - Behavioral health documentation awareness
    - Documentation integrity
    - HIPAA privacy awareness
    - 42 CFR Part 2 awareness
    - Quality assurance
    - AI workflow design
    - Data dashboard development
    """)
