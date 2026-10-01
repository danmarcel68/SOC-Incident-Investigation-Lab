\# SOC Incident Investigation Lab



\## Overview



This project demonstrates a simulated Security Operations Center (SOC) investigation involving suspicious SSH authentication activity against a Linux web server.



The investigation begins with repeated failed authentication attempts from a single external IP address and progresses to a successful account login, privileged command execution, system reconnaissance, external file transfer, and execution of a downloaded script.



The goal of this project was to practice analyzing authentication logs, identifying indicators of compromise, reconstructing an attack timeline, mapping observed behavior to MITRE ATT\&CK, and developing a Python-based detection script.



> \*\*Note:\*\* This is a simulated cybersecurity lab. The IP addresses used in the dataset are documentation addresses and do not represent actual malicious systems.



\---



\## Scenario



A SOC alert identified an unusual number of failed SSH authentication attempts against:



\*\*Asset:\*\* `WEB-SRV-01`



Initial investigation identified repeated login attempts from:



`203.0.113.45`



The activity targeted several usernames before successfully authenticating to the `daniel` account.



Further investigation was conducted to determine whether the activity represented normal user behavior or a potential compromise.



\---



\## Investigation Process



The investigation included:



1\. Reviewing raw SSH authentication logs

2\. Counting failed authentication attempts

3\. Identifying targeted usernames

4\. Extracting suspicious source IP addresses

5\. Correlating failed and successful authentication events

6\. Reviewing activity following successful authentication

7\. Identifying indicators of compromise

8\. Mapping observed behavior to MITRE ATT\&CK

9\. Developing Python detection logic to automate authentication analysis



\---



\## Key Findings



The analysis identified:



\- \*\*11 failed SSH authentication attempts\*\*

\- \*\*6 usernames targeted\*\*

\- All failed attempts originated from `203.0.113.45`

\- `admin` was targeted 4 times

\- `daniel` was targeted 3 times

\- `daniel` successfully authenticated 18 seconds after the final failed attempt

\- Privileged commands were executed using `sudo`

\- `/etc/passwd` was accessed

\- Configuration files were searched

\- `update.sh` was downloaded from `198.51.100.27`

\- The downloaded script was given executable permissions

\- `/tmp/update.sh` was executed



Based on the available evidence, the activity was assessed as a \*\*likely system compromise\*\*.



\---



\## Authentication Analysis



PowerShell was used to analyze failed authentication events, targeted accounts, and source IP activity.



!\[Failed Login Analysis](screenshots/01-failed-login-analysis.png)



!\[Source IP Analysis](screenshots/02-source-ip-analysis.png)



\---



\## Python Detection



A Python script was developed to automate analysis of the SSH authentication logs.



The detector:



\- Counts failed authentication attempts

\- Extracts targeted usernames

\- Identifies source IP addresses

\- Flags IP addresses exceeding a failed-login threshold

\- Correlates failed authentication attempts with subsequent successful authentication

\- Tracks username and source-IP combinations

\- Processes authentication events chronologically



Example detection:



```text

\[WARNING] 203.0.113.45 generated 11 failed login attempts.



\[HIGH ALERT] Successful login for 'daniel' from 203.0.113.45 after 3 previous failed attempts against the same account.

