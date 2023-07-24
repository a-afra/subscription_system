<h1 align="center">Subscription System</h1>

<p align="center">
<img src="readme_assets\1.png" alt="">
</p>
<p align="center">
<img src="readme_assets\2.png" alt="">
</p>
<p align="center">
<img src="readme_assets\3.png" alt="">
</p>

## Description

This is a subscription management system built with Django.

## Requirements

* Python 3.6 or higher
* Django 3.2.8

## Getting started

### Installation

Clone the repository or download the ZIP file:
```bash
git clone https://github.com/a-afra/subscription_system.git
cd subscription_system-master
```

Create a virtual environment and activate it:
```bash
python3 -m venv env
```

Activate the virtual environment:

On Windows:
```bash
env\Scripts\activate
```

On Unix or Linux:
```bash
source env/bin/activate
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

Migrate the database:
```bash
cd src/subscriptionproject/
python manage.py makemigrations
python manage.py migrate
```

Create a superuser:
Recomen: use 'admin' as username and password.
```bash
python manage.py createsuperuser
```

Run the development server:
```bash
python maange.py runserver
```

The application can now be accessed at http://localhost:8000/.

## Usage

**Important Step**
You have to add some plans before using the app.

To access the administration interface, go to http://localhost:8000/admin/ and log in with your superuser credentials.

### Creating New Plans

* Log in as a superuser at http://localhost:8000/admin.
* Under the Subscription Plans section, click Add.

<p align="center">
<img src="readme_assets\4.png" alt="">
</p>

* Fill out the form with following content and create 3 new subscription plans.

| Name |  Price |  Description |
|---|---|---|
|  Basic |  10.0 | 2 VCPU<br>2 GB DDR4<br>30 GB Storage  |
|  Professional |  15.0 |  4 VCPU<br>8 GB DDR4<br>140 GB Storage |
|  Advanced |  20.0 |  6 VCPU<br>16 GB DDR4<br>250 GB Storage |

<p align="center">
<img src="readme_assets\5.png" alt="">
</p>


Once you have set up the project, you can use it to manage subscriptions. There are also features to manage invoices.



### Subscribing to Plans

* Navigate to the Plans page at http://localhost:8000/plans.
* Click the Subscribe button next to the desired plan.

### Invoicing

* Invoices will be automatically created for subscribed users on a periodic basis.

### Account Information

* Navigate to the My Account page at http://localhost:8000/my-account.
* View the subscriptions and invoices.

### Account Statistics

* Navigate to the My Statistics page at http://localhost:8000/my-statistics.
* View the total number of invoices and spending per plan.
