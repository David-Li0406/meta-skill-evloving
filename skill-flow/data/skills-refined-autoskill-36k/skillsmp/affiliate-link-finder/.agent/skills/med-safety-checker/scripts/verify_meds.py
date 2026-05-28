import sys
import json

# Mock database of safety info
# TODO: Connect this to OpenFDA API for real-time data
SAFE_DATA = {
    "adderall": {
        "severity": "high",
        "warning": "Avoid Vitamin C 1 hour before/after. May cause insomnia if taken late."
    },
    "citicoline": {
        "severity": "medium",
        "warning": "May increase dopamine levels. Monitor for overstimulation if combined with stimulants."
    },
    "ritalin": {
        "severity": "medium",
        "warning": "Take with food to reduce stomach upset."
    },
    "magnesium": {
        "severity": "low",
        "warning": "Best taken in the evening for sleep support."
    }
}

def check_med(name):
    name = name.lower().strip()
    result = SAFE_DATA.get(name)
    
    if result:
        return json.dumps({
            "found": True,
            "medication": name,
            "data": result
        }, indent=2)
    else:
        return json.dumps({
            "found": False,
            "medication": name,
            "message": "No specific warnings found in local database. Consult a doctor."
        }, indent=2)

if __name__ == "__main__":
    med_name = sys.argv[1] if len(sys.argv) > 1 else ""
    # Print result to stdout for easy parsing
    print(check_med(med_name))
