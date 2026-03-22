"""
advisor.py - AI decision engine and natural language text generation
Analyzes predicted usage and generates personalized advice
"""


def classify_risk(predicted_gb):
    """
    Classify data usage risk level.

    Returns:
        tuple: (risk_level str, threshold_gb float)
    """
    if predicted_gb < 3:
        return "Low", 3
    elif predicted_gb < 8:
        return "Medium", 8
    else:
        return "High", None


def identify_drivers(daily_hours, streams_video, num_downloads, social_media_hours):
    """Identify the biggest contributors to data usage."""
    drivers = []

    if streams_video and daily_hours > 2:
        drivers.append("video streaming")
    if num_downloads >= 5:
        drivers.append("frequent downloads")
    if social_media_hours >= 3:
        drivers.append("heavy social media use")
    if daily_hours >= 8:
        drivers.append("long daily internet sessions")

    return drivers


def generate_advice(predicted_gb, risk_level, drivers, daily_hours, streams_video, num_downloads, social_media_hours):
    """
    Generate natural language advice based on usage analysis.

    Returns:
        str: Personalized advice paragraph
    """
    driver_text = ""
    if drivers:
        driver_text = f" due to {', '.join(drivers)}"

    lines = []

    # Opening summary
    if risk_level == "Low":
        lines.append(
            f"Great news! Your estimated data usage is {predicted_gb} GB, which is well within a healthy range."
        )
        lines.append("You're managing your internet consumption efficiently.")
    elif risk_level == "Medium":
        lines.append(
            f"Your estimated data usage is {predicted_gb} GB{driver_text}. "
            "This is moderate — you're doing okay, but there's room to optimize."
        )
    else:
        lines.append(
            f"Your estimated data usage is {predicted_gb} GB{driver_text}. "
            "This is quite high and may lead to data cap issues or increased costs."
        )

    # Specific suggestions
    suggestions = []

    if streams_video:
        suggestions.append(
            "Switch video streaming quality to 480p or 720p instead of HD/4K — "
            "this alone can cut streaming data usage by up to 70%."
        )
    if num_downloads >= 5:
        suggestions.append(
            f"You're downloading {num_downloads} files per day. "
            "Try batching downloads during off-peak hours or using a download manager to avoid duplicates."
        )
    if social_media_hours >= 3:
        suggestions.append(
            f"You spend {social_media_hours} hours on social media daily. "
            "Disabling auto-play videos in apps like Instagram, TikTok, and Facebook can save significant data."
        )
    if daily_hours >= 8:
        suggestions.append(
            f"With {daily_hours} hours of daily usage, consider setting screen time limits "
            "or scheduling offline periods to reduce background data consumption."
        )

    if not suggestions:
        suggestions.append(
            "Keep up your current habits. You can further optimize by enabling data-saver modes in your browser and apps."
        )

    lines.append("\nSuggestions:")
    for i, s in enumerate(suggestions, 1):
        lines.append(f"  {i}. {s}")

    return "\n".join(lines)


def whatif_simulation(daily_hours, streams_video, num_downloads, social_media_hours):
    """
    Run what-if scenarios to show impact of behavior changes.

    Returns:
        list of dict: Each scenario with description and predicted GB
    """
    from model import predict_usage

    scenarios = []
    baseline = predict_usage(daily_hours, streams_video, num_downloads, social_media_hours)

    if streams_video:
        no_stream = predict_usage(daily_hours, 0, num_downloads, social_media_hours)
        scenarios.append({
            "scenario": "If you stop video streaming",
            "predicted_gb": no_stream,
            "savings_gb": round(baseline - no_stream, 2)
        })

    if num_downloads > 0:
        half_downloads = predict_usage(daily_hours, streams_video, num_downloads // 2, social_media_hours)
        scenarios.append({
            "scenario": f"If you halve your downloads ({num_downloads} → {num_downloads // 2})",
            "predicted_gb": half_downloads,
            "savings_gb": round(baseline - half_downloads, 2)
        })

    if social_media_hours > 1:
        less_social = predict_usage(daily_hours, streams_video, num_downloads, max(social_media_hours - 1, 0))
        scenarios.append({
            "scenario": "If you reduce social media by 1 hour",
            "predicted_gb": less_social,
            "savings_gb": round(baseline - less_social, 2)
        })

    if daily_hours > 2:
        less_time = predict_usage(max(daily_hours - 2, 1), streams_video, num_downloads, social_media_hours)
        scenarios.append({
            "scenario": "If you reduce daily internet time by 2 hours",
            "predicted_gb": less_time,
            "savings_gb": round(baseline - less_time, 2)
        })

    return scenarios


def analyze(daily_hours, streams_video, num_downloads, social_media_hours):
    """
    Full agentic analysis pipeline.

    Returns:
        dict with predicted_gb, risk_level, advice, and whatif scenarios
    """
    from model import predict_usage

    predicted_gb = predict_usage(daily_hours, streams_video, num_downloads, social_media_hours)
    risk_level, _ = classify_risk(predicted_gb)
    drivers = identify_drivers(daily_hours, streams_video, num_downloads, social_media_hours)
    advice = generate_advice(predicted_gb, risk_level, drivers, daily_hours, streams_video, num_downloads, social_media_hours)
    whatif = whatif_simulation(daily_hours, streams_video, num_downloads, social_media_hours)

    return {
        "predicted_gb": predicted_gb,
        "risk_level": risk_level,
        "advice": advice,
        "whatif_scenarios": whatif
    }
