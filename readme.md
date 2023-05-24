# Steps

1. setup
2. environments
3. run project

# Setup

```sh
python -m venv env # create environment
source env/bin/activate # activate environment

pip install -r requirements.txt # install all dependencies
```

# Environment

you must create .env file with this values:

```sh
DEV_HOST = [dev host]
DEV_SUBJECT_TOKEN= [dev subject token]
DEV_COMMISSION_TOKEN= [dev commission token]
DEV_ENROLLMENT_TOKEN= [dev enrollment token]
DEV_STAGE_MACHINE_TOKEN= [dev stage machine token]

QA_HOST = [qa enrollment token]
QA_SUBJECT_TOKEN = [qa enrollment token]
QA_COMMISSION_TOKEN = [qa enrollment token]
QA_ENROLLMENT_TOKEN= [qa enrollment token]
QA_STAGE_MACHINE_TOKEN= [qa enrollment token]

IS_LOCAL = [if send request to local enrollments then this value will be true]
ONLY_ENROLLMENTS = [only run enrollments without product, commissions and subjects (stage machine will run)]
PRODID = [ product id to enroll (only if ONLY_ENROLLMENTS is True) ]
```

# Run Project

## DEV [DEPRECTATED]

if you need to run in **dev** environment, you'll write this command

```
python main.py dev
```

<br />
<br />

## QA

if you need to run in **qa** environment, you'll write this command

```
python main.py qa
```

# Code

```python

# create subject
# createSubjects( [number of subject] )
sIDs = api.createSubjects(2)

# create Path
# createPath( [subjects ID] )
pathID = api.createPath(sIDs)

# create Product
# createProduct( [path ID], [Start date], [slot_to], [slot_from], [vacancy] )
prodID =  api.createProduct(pathID, '2022-03-29', "16:00:00","20:00:00",20)

# create Commission
# createCommission( [subject ID], [Start date], [End date], [Vacancy], [Cohort], [Start time], [End time] )
api.createCommission(sIDs[0], "2022-01-22T00:00:00Z", "2022-02-22T00:00:00Z",1,"A", "16:00:00", "20:00:00")

# create User enrollment
# createCommission( [product ID], [number of users] )
api.createUserEnrollment(prodID, 1)

```
