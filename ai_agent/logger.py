import datetime

def log_query(user_id, query, result):
    timestamp = datetime.datetime.now().isoformat()
    with open("responses.log", "a") as f:
        f.write(f"[{timestamp}] USER: {user_id} | QUERY: {query} | RESULT: {result}\n")