from data import drivers_by_location

def search_location(user_input):
    suggestions = []

    for location in drivers_by_location:
        if user_input.lower() in location.lower():
            suggestions.append(location)

    return suggestions
