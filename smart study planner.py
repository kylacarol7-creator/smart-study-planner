print("smart study planner")
FILE = "study_log.txt"


def classify_session(d):
    if d < 30: return "Short"
    if d <= 90: return "Medium"
    return "Long"


def add_session(sessions):
    subject = input("Subject: ").strip()
    topic = input("Topic: ").strip()
    date = input("Date/day: ").strip()
    while True:
        try:
            d = float(input("Duration (min): "))
            if d > 0:
                break
            print("Must be positive.")
        except ValueError:
            print("Enter a valid number.")
    sessions.append({"subject": subject, "topic": topic, "date": date, "duration": d})
    print("Added.\n")


def print_row(s):
    print(f"{s['subject']:<12}{s['topic']:<15}{s['date']:<12}{s['duration']:<6}{classify_session(s['duration'])}")


def view_sessions(sessions):
    if not sessions:
        print("No sessions logged.\n"); return
    print(f"{'Subject':<12}{'Topic':<15}{'Date':<12}{'Min':<6}Type")
    for s in sessions: print_row(s)
    print()


def search_by_subject(sessions, subject):
    matches = [s for s in sessions if s["subject"].lower() == subject.lower()]
    if not matches:
        print(f"No sessions for '{subject}'.\n"); return
    for s in matches: print_row(s)
    print(f"Total: {sum(s['duration'] for s in matches)} min\n")


def study_statistics(sessions):
    if not sessions:
        print("No sessions logged.\n"); return
    totals = {}
    for s in sessions:
        totals[s["subject"]] = totals.get(s["subject"], 0) + s["duration"]
    weakest = min(totals, key=totals.get)
    longest = max(sessions, key=lambda s: s["duration"])
    print(f"Total: {sum(totals.values()) / 60:.2f} hrs")
    for subj, mins in totals.items():
        print(f"  {subj}: {mins / 60:.2f} hrs")
    print(f"Weakest subject: {weakest}")
    print(f"Longest session: {longest['subject']} - {longest['topic']} ({longest['duration']} min)\n")


def save_sessions(sessions):
    with open(FILE, "w") as f:
        for s in sessions:
            f.write(f"{s['subject']}|{s['topic']}|{s['date']}|{s['duration']}\n")
    print("Saved. Goodbye!")


def load_sessions():
    sessions = []
    try:
        with open(FILE, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 4:
                    subj, top, date, dur = parts
                    sessions.append({"subject": subj, "topic": top, "date": date, "duration": float(dur)})
    except FileNotFoundError:
        pass
    return sessions


def main():
    sessions = load_sessions()
    menu = "1. Add session\n2. View all\n3. Search by subject\n4. Statistics\n5. Save and exit"
    actions = {
        "1": lambda: add_session(sessions),
        "2": lambda: view_sessions(sessions),
        "3": lambda: search_by_subject(sessions, input("Subject: ").strip()),
        "4": lambda: study_statistics(sessions),
    }
    while True:
        print(menu)
        choice = input("Choice: ").strip()
        if choice == "5":
            save_sessions(sessions)
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Invalid choice.\n")


if __name__ == "__main__":
    main()