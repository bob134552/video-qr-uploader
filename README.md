# QRit App

The app is designed to compliment a completed order on Shopify,
after a completed order the user can upload a video message to the receiver of the order.
After the initial login a QR code is generated for the person receiving the video that prefills the video login page.

The receiver of the video message is able to scan the generated QR code and be brought to a prefilled video login page.
Upon logging in the user is able to view the video and send a message to the uploader.

---

## Database

Heroku Postgres is used for the database.

### Model

#### Videos Model

|Name|Key|Description|Field Type|
|:---|:----:|:----:|---:|
|Order number|order_number|max_length=256, null=False, blank=False|Charfield|
|Video|video|upload_to='videos/', null=True, blank=True|Filefield|
|Email|email|max_length=254, null=False, blank=False|Emailfield|
|Keyword|keyword|max_length=20, null=False, blank=False|Charfield|
|qr_code|Qr code|upload_to='qr_codes/', null=False, blank=False|Imagefield|
|reply|Reply|default=False, null=False, blank=False|Booleanfield|

---

## Technologies Used (Frameworks, Libraries, Languages and Programs used)

- [Django](https://www.djangoproject.com/)
    - To allow for easier creation of the site.
- [jQuery](https://en.wikipedia.org/wiki/JQuery)
    - Allows for easier DOM manipulation.
- [Bootstrap5](https://getbootstrap.com/)
    - To make a responsive mobile first site and allow for a simpler structure.
- [Heroku](https://www.heroku.com/)
    - Used for deploying and managing the project.
    - Postgres database used outside of developement.
- [GitHub](https://github.com/)
    - Used to store the projects code.
- [GitPod](https://www.gitpod.io/)
    - IDE used to build the site.
- [Amazon Web Services](https://aws.amazon.com/)
    - Used to store static and media files through S3
- [Animate on Scroll](https://github.com/michalsnik/aos)
    - For a smoother animation for elements on each page.
- [webRTC](https://webrtc.github.io/samples/)
    - For the video capture tool on upload.

### Features

- Automatic QR generation upon creation of video model.
- Video recording tool to aid user in uploading their message.
- Reply form for receiver to message uploader regarding their video message.
- Video preview so user uploading can view their video.
- Shopify integration to avoid creating uploads without a shopify purchase.

### Problems

- Video recorded using the recording tool do not have duration data.
    - A 30s timer has been added to prevent recording a video longer than 30s.
- Currently not able to query Shopify's order API using order number.
    - Retrieving all orders to iterate through at the moment.

---

## Deployment

The app is deployed on Heroku and is viewable through [here](https://qrit-video-app.herokuapp.com/).
