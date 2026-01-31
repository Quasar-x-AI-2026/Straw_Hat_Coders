def reflection_prompt(view):
    if view == "daily":
        return [
            "Did anything specific happen on days where scores changed?",
            "How were your sleep and routine on those days?"
        ]

    if view == "weekly":
        return [
            "What patterns do you notice across weeks?",
            "Did workload or social interaction change?"
        ]

    if view == "yearly":
        return [
            "Looking long-term, what major phases stand out?",
            "Were there lifestyle or environment changes?"
        ]

    return []
