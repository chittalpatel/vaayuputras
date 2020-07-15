# ![Vaayuputras](https://vaayuputras.imfast.io/vp_home.jpg)
# Vaayuputras
<table>
<tr>
<td>
  Vaayuputras is a website built using Django framework and It aims to provide a global solution for Wind Power Prediction for any wind farm on earth.
</td>
</tr>
</table>

## Website Hosted on IBM Cloud Foundry
Here is the working live website :  https://vaayuputras.eu-gb.cf.appdomain.cloud/

## Features

- Wind Power Prediction for any wind farm on earth
- Select wind farm from database
- Select wind farm directly from Google Maps
- Wind Farm Economics Calculator
- Power given to user to Train their own model with their owned wind farm data and use it for prediction.
- RESTful API Support for Wind Power prediction and Wind Farm Economics calculator for both Auth and Non-Auth Users.
- Very Powerful IBM Watson Assistant which can perform Wind Power prediction, Do Wind Farm Economics and Chat with Users about Wind Farm Terminologies.

## Site

### Services
The Site is packed with numerous services with beautiful UI for complete User experience.

![](https://vaayuputras.imfast.io/vp_feat.jpg)

### User Authentication System
![](https://vaayuputras.imfast.io/vp_auth.jpg)

### Dashboard
![](https://vaayuputras.imfast.io/vp_dash.jpg)

### Wind Farm Selection
![](https://vaayuputras.imfast.io/vp_swf.jpg)

### Charts
![](https://vaayuputras.imfast.io/vp_ch1.jpg)
![](https://vaayuputras.imfast.io/vp_ch2.jpg)
![](https://vaayuputras.imfast.io/vp_ch3.jpg)

### Wind Farm Economics Calculator
![](https://vaayuputras.imfast.io/vp_wfec.jpg)


## Libraries, Frameworks and UI Used

- Django
- Tensorflow
- Keras
- Material Kit 2.0 UI
- Rest Framework for Django
- Watson Machine Learning
- Watson Assistant
- IBM Elephant SQL (Postgre SQL) Service (for Database Management)
- IBM Cloud Foundry (for Deployment)
- Google Cloud Maps API
- Javascript libraries like Jquery, Popper, NoUISlider, Stats, Plotly etc.
- Weather APIs from OpenWeatherMaps and Climacell.

### Static and JS Files
Static Files, Images and Javascript Files used in project are Hosted [HERE](https://vaayuputras.imfast.io/) as CDN.

## Dataset
All the Data which was gathered from numerous sources and websites is available [HERE](https://drive.google.com/drive/folders/1AybyjROKdkmerQqCffyRwUzvy7KGVWWA?usp=sharing) on Google Drive.

## Data Analysis and Model Training Notebooks

A Kaggle Notebook which was made by Me for Kaggle Dataset Analysis and also received Silver Medal is Available [HERE](https://www.kaggle.com/chittalpatel/wind-turbine-power-analysis)

Other Notebook which contains All the Data Cleaning, Analysis, Machine Learning Experiment and Deep Learning Modelling using LSTM is available in Repo itself.

## How to Run the Project Locally

- Fork the Repository
- Create a Django Environment for vaayuputras_source_code
- Install dependencies from Pipfile.lock
- Connect your database and migrate app
- Create IBM Cloud Account and Deploy the model located in media folder
- Replace all the credentials and API keys with your own
- You are all set to Go...

## How to Run the Project on Cloud

- Follow above all the instructions
- Create Cloud Foundry Service for Python Django App from IBM Cloud
- Push All the Source Files to Gitlab repository on IBM Cloud
- You have completed deploying.

## Team

Chittal Patel | Dhruvil Dholariya
---|---
email.chittal@gmail.com | dhruvildholariya410@gmail.com


### Bug / Feature Request

If you find a bug (the website couldn't handle the query and / or gave undesired results), kindly open an issue [here](https://github.com/chittalpatel/vaayuputras/issues/new) by including your search query and the expected result.

If you'd like to request a new function, feel free to do so by opening an issue [here](https://github.com/chittalpatel/vaayuputras/issues/new). Please include sample queries and their corresponding results.


### Development
Want to contribute? Great!

To fix a bug or enhance an existing module, follow these steps:

- Fork the repo
- Create a new branch (`git checkout -b improve-feature`)
- Make the appropriate changes in the files
- Add changes to reflect the changes made
- Commit your changes (`git commit -am 'Improve feature'`)
- Push to the branch (`git push origin improve-feature`)
- Create a Pull Request 
