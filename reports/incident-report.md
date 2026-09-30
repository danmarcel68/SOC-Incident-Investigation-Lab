# SOC Incident Investigation Report

## Incident Summary

A series of repeated SSH authentication failures was observed against `WEB-SRV-01` from the external IP address `203.0.113.45`.

The source attempted multiple usernames, including `admin`, `administrator`, `root`, `test`, `ubuntu`, and `daniel`.

A total of 11 failed authentication attempts occurred. The account `daniel` experienced three consecutive failed logins, followed by a successful authentication from the same source IP 18 seconds later.

Following the successful login, the session executed privileged commands using `sudo`, performed system reconnaissance, downloaded an external shell script, made the script executable, and executed it.

## Key Findings

- Source IP: `203.0.113.45`
- Failed authentication attempts: `11`
- Targeted usernames: `admin`, `administrator`, `root`, `test`, `ubuntu`, `daniel`
- Most frequently targeted username: `admin` with 4 attempts
- Failed attempts against `daniel`: `3`
- Successful login account: `daniel`
- Successful login time: `2026-09-30 09:14:07`
- Time between final failed login and successful authentication: `18 seconds`
- Secondary external IP observed: `198.51.100.27`

## Post-Authentication Activity

After authentication, the following activity was observed:

- Verified privileged access using `whoami`
- Read `/etc/passwd`
- Searched the filesystem for `.conf` files
- Downloaded `update.sh` from `198.51.100.27`
- Saved the script to `/tmp/update.sh`
- Added executable permissions using `chmod +x`
- Executed `/tmp/update.sh`

## Initial Assessment

The activity is assessed as a likely system compromise.

The combination of repeated failed SSH attempts, a successful login from the same source IP, immediate privileged activity, system reconnaissance, and execution of a remotely downloaded script is strongly inconsistent with normal user behavior.

Further analysis would be required to determine the contents and impact of `update.sh`.