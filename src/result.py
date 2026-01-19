def severity_from_score(score):
    if score >= 10:
        return "Severe"
    elif score >= 5:
        return "Moderate"
    return "Mild"


def recommendations(severity):
    if severity == "Severe":
        return [
            "Seek professional mental health support",
            "Reach out to trusted family or friends",
            "Avoid isolation and harmful coping mechanisms"
        ]
    elif severity == "Moderate":
        return [
            "Practice stress management techniques",
            "Maintain regular sleep and routine",
            "Monitor symptoms regularly"
        ]
    else:
        return [
            "Maintain healthy habits",
            "Stay socially connected",
            "Practice mindfulness or relaxation"
        ]


def explain_result(risk, severity):
    return (
        f"The system predicts a {risk.upper()} mental health risk "
        f"with {severity.lower()} severity based on the provided inputs. "
        "This assessment is generated using patterns learned from social media data."
    )
