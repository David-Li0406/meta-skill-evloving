import json

def generate_firestore_schema():
    """
    Generates the Firestore NoSQL schema structure for the application.
    Adapted from SQL concepts for Flutter/Firebase context.
    """
    
    schema = {
        "collection": "users",
        "document": "{userId}",
        "subcollections": {
            "logs": {
                "document": "{dateString}", # YYYY-MM-DD
                "fields": {
                    "id": "String (UUID)",
                    "med_name": "String",
                    "actual_time": "Timestamp (ServerTime)",
                    "scheduled_time": "Timestamp",
                    "status": "String (enum: Taken, Skipped, Late)",
                    "confidence_score": "Integer (1-5)" # Critical for ADHD self-doubt tracking
                }
            }
        },
        "indexes": [
            "logs/{dateString}/status ASC",
            "logs/{dateString}/actual_time DESC"
        ]
    }
    
    return json.dumps(schema, indent=2)

if __name__ == "__main__":
    print(generate_firestore_schema())
