**Activate Env**
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip freeze > requirements.txt

**Create Super Admin**
python manage.py createsuperuser

**Start a local web server**  <br />
python manage.py runserver
python3 manage.py runserver

**Make Migration, If you modify anything in modals**<br />
python manage.py makemigrations

**Migate the modal changes to database**<br />
python manage.py migrate

**Root User Credentials**<br />
admin/12345
darjitailormade@gmail.com

admin/Darji@dm!n

**Create migration for specific app**
./manage.py makemigrations <myapp>

**API for Users**

- Login
- register
- forget password
- mobile number verification


**API Documentation**<br />
https://documenter.getpostman.com/view/5902920/2s83zgsPrb

**This will keep the pycaceh files and remove from git**
git rm -r **/__pycache__  --cached 