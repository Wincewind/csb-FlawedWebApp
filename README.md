# csb-FlawedWebApp
The flawed web app I have created for this project is a fairly simple one. Its only functionalities are the creation of new accounts, recovery of a user’s password, logging in/out, and storing and editing of a “super-secret” that should only be visible to the account’s owner. Below are listed the flaws I purposely included in the application as well as fixes. 


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

### 1: Identification and Authentication Failure 
[flawedsite/views.py#L41](flawedsite/views.py#L41)

In this flaw, the user is allowed to create an account with any sort of password. According to OWASP, permitting any sort of default or weak passwords is considered an authentication weakness. 
The fix for this flaw starts at [flawedsite/views.py#L33](flawedsite/views.py#L33) and can be applied by setting identification_and_authentication_failure_fix inside the function to True. In this fix, the settings.py’s AUTH_PASSWORD_VALIDATORS are utilized to validate the user password before saving the model. In case there are validation errors, the creation of a new user and account is terminated, and an error message is displayed in the browser explaining what details in the password are still lacking. 
This doesn’t of course cover all issues with the app's identification and authentication since a missing MFA is also considered a weakness. 
 
### 2: Broken Access Control 
[flawedsite/views.py#L60](flawedsite/views.py#L60)

In this flaw, users can view and edit each other's super-secrets even though this should be possible for only their own. Viewing can simply be done if one can guess someone else’s user primary key, at which point one can just navigate to /secret/<uid> rather than clicking the link on the home page that loads your secret. For editing someone’s secret, I exempted the csrf to make it a bit easier. To test this, you can use the test_bac.py script that will require a logged-in session’s sessionid and csfrtoken from cookies, or on the secret page, inspect the new secret form elements and change the id in the form action before submitting a new secret. 
The fix consists of removing the @csrf_exempt decorator and setting the bac_fix to True. This will compare the session’s user details to the uid in the URL parameters and raise a PermissionDenied exception if they don’t match. With this, any access to secrets other than one's own should be fixed. 
 
### 3: Injection 
[flawedsite/views.py#L69](flawedsite/views.py#L69)

In this flaw, an account’s secret is updated without any sanitation, which leaves it vulnerable to SQL injection. For example, you can test inputting 
You´ve been hacked!'; --
As your secret and see how this affects other accounts. 
Fix for this starts at [flawedsite/views.py#L65](flawedsite/views.py#L65), where the secret is updated using the Account model rather than a query using string concatenation. The fix can be applied by setting the injection_fix to True. 
 
### 4: Security Logging and Monitoring Failure 
[flawedsite/settings.py#L128](flawedsite/settings.py#L128) 

Regarding earlier flaws 2 and 3, there is a log created of which user has edited who's secret and to what value. If this were recorded in a separate log file, this issue could then have been investigated using this file and the culprit of possible misuse could be found. Since the django logging functionality is commented out in the settings.py, this doesn’t happen. 
The fix would be to comment the logging back in, at which point the secret edits would be recorded in logs/debug.log file with a timestamp detail as well. 
 
### 5: Cryptographic Failure 
[flawedsite/models.py#L14](flawedsite/models.py#L14)

According to OWASP description, insecure storage and transmission of sensitive data, like personal information, is considered a cryptographic failure. This flaw consists of storing the users’ social security number details in plain text.  
To fix this, we’re using django-cryptography library’s encrypt function in the models to strengthen the security of the data when stored. The function also decrypts the information when it’s accessed, although I doubt this by itself secures much of the data’s transmission. The fix can be applied by assigning True to cryptographic_failure_fix in models.py. 
 
### 6: Insecure Design 
[flawedsite/views.py#L78-L114](flawedsite/views.py#L78-L114)

One of the forms of insecure design according to OWASP, is the use of outdated “questions and answers” model of credential recovery. The linked functions enable the user to change their password by answering their password recovery question correctly. The questions, however, are extremely simple and make guessing someone else’s answer easy and are therefore not secure at all. 
OWASP advises replacing this sort of functionality with something more secure, and the fix I’ve come up with is sending a temporary password to the user’s email, that they can use to log in. As you can see, however, the fix doesn’t contain any actual mailing functionality and, in its place, I’ve just included a print statement to imitate it. Due to the fix being hypothetical, I’ve included this flaw and fix as more of an extra. Note that the message sent to the user’s client does not reveal if the email that was provided was linked to an actual account or not. This way the app won’t give out information to hackers who might be testing the functionality to find out valid emails. 
The fix can be enabled by assigning insecure_design_fix to True in urls.py: [flawedsite/urls.py#L23](flawedsite/urls.py#L23)
