# csb-FlawedWebApp

Flaws & Fixes:

1. Broken Access Control
- Someone else can view & edit your super secret

2. Injection:
- Malicious code can be inserted into the super secret

3. Insecure Design:
- There is a password recovery option that relies on the “questions and answers" model which is prohibited by the OWASP Top 10.
- Fix could be a mandatory email detail for accounts to which password recovery link is sent to reset the current password.

4. Security Misconfiguration
- Accessing someone else's page/secret will give an error log revealing sensitive information.
- Fix would be to take this possibility into account, alter business logic accordingly and redirect to 403 page instead.

5. Identification and Authentication Failures
- Any form of password is allowed when creating new users.

6. Security Logging and Monitoring Failures
- No logs collected about changing of super secret.