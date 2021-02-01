# Bodleian Scheduler
|PyPi_Version| |PyPi_Status| |Format| |Supported_versions_of_Python| |Language grade: Python| |License|

The Bodleian Scheduler is a service that returns an ics calendar invite via your Oxford University email when you book a library slot through https://spacefinder.bodleian.ox.ac.uk/

### Setup

Go to https://www.oxtickets.co.uk/ where you can follow steps 1 and 2 in order to sign up for the service.

Enter your Oxford University College email as seen below

```bash
john.smith@college.ox.ac.uk
```
## New Bod Booking Bot

The Bod slot booking bot uses selenium to click through the process as fast as your internet will allow you to. The booker can be initialised and run on your computer with python3.

Please enter your details into the **userdata.json** completely and correctly.

### Slot Preference IDs

Enter these IDs into each slot preference.

```bash
BOD UPPER
BOD LOWER
DUKE HUMFREYS
VERE HARMSWORTH
```

If there are any issues please contact
[fraser@sauramedia.com](mailto:fraser@sauramedia.com)