Project created using Django.

This is a public file created by myself for others to view, a Private file is also created for production once complete (3/2024) public created.

################################### Attention ####################################################
To work in local host via vscode, follow three steps in settings file. :-
#1. Unhash the secret key.
#2. hash out whitenoise in MIDDLEWARE.
#3. hash out 

#For production, add the production.py file, the secret key will need to be added in azure for security.

Env file required containing the following to work:-
SECRET_KEY= 

EMAIL_HOST= 
EMAIL_HOST_USER= 
EMAIL_HOST_PASSWORD= 

DJSTRIPE_WEBHOOK_SECRET= 
STRIPE_ENDPOINT_SECRET= 
STRIPE_PUBLISHABLE_KEY= 
STRIPE_SECRET_KEY= 
STRIPE_PRICE_ID_25= " " #for one off 25 payment test environment
STRIPE_PRICE_ID_15= " " #for one off 15 payment test environment
STRIPE_PRICE_ID_30= " " #for one off 30 payment test environment
STRIPE_PRICE_ID_PROD= " " #TMH Product

The app works by the user first entering the site presented with a map (Courtesy of leaflet maps)
A user/recovery operator can then register, which uses django built in forms with additional of catcha inserted for security.

Once registered, an email is sent to the user welcoming them and prompting them to edit their profile.

This is where they enter there details, an option near bottom of form to enter post code, then select button which uses an API postcode.io 
to get the geoLocation of the user.

The top of profile is subscribe button. Where user will be redirected to a page to select one of three options to pay for either 31, 62 or 93 days.
Upon selecting which one, the user is directed to stripe check out page where card details maybe entered.

Once payment has gone through. A webhook is programmed to listen where the id and price selected and if paid is then entered to the users model to update the date.
#   r o a d s i d e _ a p p _ p u b l i c  
 #   r o a d s i d e _ a p p _ p u b l i c  
 