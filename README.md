# csb-FlawedWebApp

## How to setup and run locally (tested in Uni Linux environment, some steps/commands might be different on Windows or Mac):
1.  Clone the repository or download it as a zip:
```bash
git clone https://github.com/Wincewind/csb-FlawedWebApp.git
```

2.  In the project folder, create a virtual environment and activate it
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```

3.  Install required modules in the virtual env
```bash
pip install -r requirements.txt
```

4.  Create the db for the app's backend with command
```bash
python manage.py migrate
```

5.  Create .env file for the environment variables and assign appropriate values for them

The values in example.env should work if it's just renamed to ".env", but generating your own secure SECRET_KEY is **highly** recommended!

6.  (Optional) Load default data to the db with command
```bash
python manage.py loaddata data.json
```
The data to be loaded can be viewed and edited in flawedsite/fixtures/data.json.
This default data will create 3 users:
```bash
1. username: mike       password: Swordfish
2. username: hacker5000 password: 12345
3. username: sarah      password: password
```

7.  The app should now be ready to go. You can start it with command
```bash
python manage.py runserver
```



## Flaws & Fixes:

### 1. Broken Access Control
- Someone else can view & edit your super secret

### 2. Injection:
- Malicious code can be inserted into the super secret

### 3. Insecure Design:
- There is a password recovery option that relies on the “questions and answers" model which is prohibited by the OWASP Top 10.
- Fix could be a mandatory email detail for accounts to which password recovery link is sent to reset the current password.

### 4. Security Misconfiguration
- Accessing someone else's page/secret will give an error log revealing sensitive information.
- Fix would be to take this possibility into account, alter business logic accordingly and redirect to 403 page instead.

### 5. Identification and Authentication Failures
- Any form of password is allowed when creating new users.

### 6. Security Logging and Monitoring Failures
- No logs collected about changing of super secret.
