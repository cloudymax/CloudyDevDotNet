#  🔥 Firebase: <em>The Fire-Basics</em> 🔥

> Firebase is <emp>a collection of GCP services re-packaged and slightly tuned for game development.</emp> The services offered through firebase are available as individual components of the GCP product offering, and are billed separately.<br />


- [Read the Docs](https://firebase.google.com/) <br />
- [Download the Firebase CLI](https://firebase.google.com/docs/cli) <br />

<br />

## Components 

1. [Firebase Authentication](https://firebase.google.com/docs/auth)

    Firebase Authentication provides <emp>backend services, easy-to-use SDKs, and ready-made UI libraries to authenticate users to your app.</emp> It supports authentication using passwords, phone numbers, popular federated identity providers like Google, Facebook and Twitter, and more. Firebase Authentication integrates tightly with other Firebase services, and it leverages industry standards like OAuth 2.0 and OpenID Connect, so it can be easily integrated with your custom backend. </p>

2. [Cloud Functions](https://firebase.google.com/docs/functions)

    Cloud Functions for Firebase is a serverless framework that lets you automatically run backend code in response to events triggered by Firebase features and HTTPS requests. Your JavaScript or TypeScript code is stored in Google's cloud and runs in a managed environment.

    !!! Warning 

        Javascript and typescript only 

- [Cloud Firestore](https://firebase.google.com/docs/firestore):

    Firebase's newest database for mobile app development. It builds on the successes of the Realtime Database with a new, more intuitive data model. Cloud Firestore also features richer, faster queries and scales further than the Realtime Database.

    !!! Warning 
        
        Not persistant by default. <br />
        
        1M conncurrent connections 10k r/w per sec <br />  </p>

- [Realtime Database](https://firebase.google.com/docs/database):

    Firebase's original database. It's an efficient, low-latency solution for mobile apps that require synced states across clients in realtime.

    !!! Warning 
        
        ❗ hard limit 200k connections and 1k writes/sec. <br /> </p>

- [Cloud Storage](https://firebase.google.com/docs/storage)

    Standard Blob Storage, store images, audio, video, or other user-generated content. On the server, you can use Google Cloud Storage APIs to access the same files. </p>

- [Hosting](https://firebase.google.com/docs/hosting)

     
    - Using the [Firebase CLI](https://firebase.google.com/docs/cli), you deploy files from local directories on your computer to our Hosting servers. <br />
    
    - Beyond serving static content, you can use [Cloud Functions](https://firebase.google.com/docs/functions) for Firebase or [Cloud Run](https://cloud.google.com/run/) to serve dynamic content and host microservices onyour sites. <br />
    
    - All content is served over an SSL connection from the closest edge server on our global CDN. You can also view and test your changes before going live. <br />
    Using the Firebase Local Emulator Suite, you can emulate your app and backend resources at a locally hosted URL. <br />
    
    - You can also share your changes at a temporary preview URL and set up a GitHub integration for easy iterations during development. <br /> </p>


- [ML Kit](https://firebase.google.com/products/ml)

    - Firebase Machine Learning is a mobile SDK that brings Google's machine learning expertise to Android and iOS apps. <br />

        **Pre-trained models:** <br />
            - Text recognition <br />
            - Image labelin g<br />
            - Object detection and tracking <br />
            - Face detection and contour tracing <br />
            - Barcode scanning <br />
            - Language identification <br />
            - Translation <br />
            - Smart Reply <br />

## **Services**

- [Crashlytics](https://firebase.google.com/docs/crashlytics)

    Firebase Crashlytics is a lightweight, realtime crash reporter that helps you track, prioritize, and fix stability issues that erode your app quality. <br />
    Crashlytics saves you troubleshooting time by intelligently grouping crashes and highlighting the circumstances that lead up to them. <br />
    Find out if a particular crash is impacting a lot of users. Get alerts when an issue suddenly increases in severity.<br />
    Figure out which lines of code are causing crashes. <br /> </p>

- [Performance Monitoring](https://firebase.google.com/docs/perf-mon)

    Performance Monitoring SDK to collect performance data from your app, then review and analyze that data in the Firebase console. <br />
    Performance Monitoring helps you to understand in real time where the performance of your app can be improved so that you can use that information to fix performance issues.


- [Robo](https://firebase.google.com/docs/test-lab/android/robo-ux-test)

    Robo test is a testing tool that is integrated with Firebase Test Lab.  <br />
    Robo test analyzes the structure of your app's UI and then explores it methodically, automatically simulating user activities. <br /> 

- [Test Lab](https://firebase.google.com/docs/test-lab)

    Firebase Test Lab is a cloud-based app testing infrastructure that lets you test your app on a range of devices and configurations, so you can get a better idea of how it'll perform in the hands of live users. <br />

- [App Distribution](https://firebase.google.com/products-release)

    Firebase App Distribution makes distributing your apps to trusted testers painless. <br />
    By getting your apps onto testers' devices quickly, you can get feedback early and often. <br />
    And if you use Crashlytics in your apps, you’ll automatically get stability metrics for all your builds, so you know when you’re ready to ship. <br />

- [Performance Monitoring](https://firebase.google.com/products/performance)

    use the Performance Monitoring SDK to collect performance data from your app, then review and analyze that data in the Firebase console. <br />
    Performance Monitoring helps you to understand in real time where the performance of your app can be improved so that you can use that information to fix performance issues. <br />



## **Ads**

- [Analyitics](https://firebase.google.com/docs/analytics)

    At the heart of Firebase is Google Analytics, a free and unlimited analytics solution. <br />
    Analytics integrates across Firebase features and provides you with unlimited reporting for up to 500 distinct events that you can define using the Firebase SDK <br />

    **integration with:**

    - [BigQuery](https://cloud.google.com/bigquery/docs)
      <p> Link your Firebase app to BigQuery where you can perform custom analysis on your entire Analytics dataset and import other data sources. <br /></p>

    - [Crashlytics](https://firebase.google.com/docs/crashlytics)
      <p> Analytics logs events for each crash so you can get a sense of the rate of crashes for different versions or regions, <br />
      allowing you to gain insight into which users are impacted. <br />
      You can also create audiences for users who have experienced multiple crashes and respond with notification messages directed at that audience. <br /></p>

    - [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging)
      Analytics automatically logs events that correspond to notification messages sent via the Notifications composer and supports reporting on the impact of each campaign. <br />

    - [Remote Config](https://firebase.google.com/docs/remote-config)
      Use Analytics audience definitions to change the behavior and appearance of your app for different audiences without distributing multiple versions of your app. <br />
      🤔 Intersting synergy to dynamically performance tune <br />

    - [Tag Manager](https://developers.google.com/tag-manager)
      Integrating Google Tag Manager alongside Google Analytics enables you to manage your Analytics implementation remotely from a web interface after your app has been distributed <br />


- [Predictions](https://firebase.google.com/docs/predictions)

    Firebase Predictions applies machine learning to your analytics data to create dynamic user segments based on your users' predicted behavior. <br />
    These predictions are automatically available for use with Firebase Remote Config, the Notifications composer, Firebase In-App Messaging, and A/B Testing. <br />
    You can also export your app's Predictions data to BigQuery for further analysis or to push to third party tools.

- [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging)

    Firebase Cloud Messaging (FCM) is a cross-platform messaging solution that lets you reliably send messages at no cost. Generic Pub/Sub <br />

- [Remote Config](https://firebase.google.com/docs/remote-config)
 
    Remote Config includes a client library that handles important tasks like fetching parameter values and caching them,  <br />
    while still giving you control over when new values are activated so that they affect your app's user experience.  <br />
    This lets you safeguard your app experience by controlling the timing of any changes. <br />
 🤔 Intersting functionality for pre-loading patches and day-1 content etc <br />
