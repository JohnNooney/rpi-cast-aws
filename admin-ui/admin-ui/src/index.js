import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
//import AWS from 'aws-sdk';
import * as AWS from 'aws-sdk'


//Initialize the Amazon Cognito credentials provider
AWS.config.region = 'us-east-1'; // Region
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
});

AWS.config.credentials.get(function(err) {
	if (err) {
		console.log("Error: "+err);
		return;
	}
	console.log("Cognito Identity Id: " + AWS.config.credentials.identityId);

	// Other service clients will automatically use the Cognito Credentials provider
	// configured in the JavaScript SDK.
	var cognitoSyncClient = new AWS.CognitoSync();
	cognitoSyncClient.listDatasets({
		IdentityId: AWS.config.credentials.identityId,
		IdentityPoolId: AWS.config.credentials.identityPoolId
	}, function(err, data) {
		if ( !err ) {
			console.log(JSON.stringify(data));
		}
	});
});

// AWS.config.loadFromPath('./libs/config.json');


ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
