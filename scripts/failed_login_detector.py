from pathlib import Path
import re
from collections import Counter

log_file = Path(__file__).parent.parent / "logs" / "authentication.log"

with open(log_file, "r") as file:
    logs = file.readlines()

failed_logins = []
usernames = []
source_ips = []

for line in logs:
    if "Failed password" in line:
        failed_logins.append(line)

        user_match = re.search(
            r"Failed password for (?:invalid user )?(\S+)", line
        )

        ip_match = re.search(
            r"from (\d{1,3}(?:\.\d{1,3}){3})", line
        )

        if user_match:
            usernames.append(user_match.group(1))

        if ip_match:
            source_ips.append(ip_match.group(1))

print("=== SSH SECURITY ANALYSIS ===")
print(f"Failed login attempts: {len(failed_logins)}")

print("\nTargeted usernames:")
for username, count in Counter(usernames).most_common():
    print(f"  {username}: {count}")

print("\nSource IP addresses:")
for ip, count in Counter(source_ips).most_common():
    print(f"  {ip}: {count}")

# Detection threshold
FAILED_LOGIN_THRESHOLD = 5

print("\n=== DETECTION RESULTS ===")

ip_counts = Counter(source_ips)

for ip, count in ip_counts.items():
    if count >= FAILED_LOGIN_THRESHOLD:
        print(
            f"[WARNING] {ip} generated {count} failed login attempts."
        )

# Correlate authentication events in chronological order
failed_by_account = Counter()

print("\n=== CORRELATED AUTHENTICATION ALERTS ===")

for line in logs:

    # Process failed authentication events
    if "Failed password" in line:
        user_match = re.search(
            r"Failed password for (?:invalid user )?(\S+)", line
        )

        ip_match = re.search(
            r"from (\d{1,3}(?:\.\d{1,3}){3})", line
        )

        if user_match and ip_match:
            username = user_match.group(1)
            ip = ip_match.group(1)

            failed_by_account[(username, ip)] += 1

    # Process successful authentication events
    elif "Accepted password" in line:
        success_match = re.search(
            r"Accepted password for (\S+) from "
            r"(\d{1,3}(?:\.\d{1,3}){3})",
            line
        )

        if success_match:
            username = success_match.group(1)
            ip = success_match.group(2)

            previous_failures = failed_by_account[(username, ip)]

            if previous_failures > 0:
                print(
                    f"[HIGH ALERT] Successful login for '{username}' "
                    f"from {ip} after {previous_failures} previous "
                    f"failed attempts against the same account."
                )