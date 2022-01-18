var AWS = require('aws-sdk');
// AWS.config.update({ region: "us-east-1" });

var ddb  = new AWS.DynamoDB({apiVersion: '2012-08-10'});

var RequestClass = function() {
    // run code here, or...
    
}; 

// ...add a method, which we do in this example:
function requestAwsData(){
    return new Promise((resolve, reject) => {
    
        // return "My List";
        const params = {
            ProjectionExpression: "RpiDateTime, RpiUser, RpiDuration, RpiFault, RpiRestarts, RpiSession, RpiSessionStatus",
            TableName: "rpi-aws-log",
        };
        
        ddb.scan(params, function (err, data) {
        if (err) {
            console.log("Error", err);
            reject(err);
        } else {
            console.log("Success", data);
            data.Items.forEach(function (element, index, array) {
                console.log(
                    "printing",
                    element
                );
            });
            //console.log(data.Items[0].RpiSessionStatus.S);
            resolve(data.Items);
            return;
        }
        
        });
    });
}

RequestClass.prototype.getAwsData = async function() {
    
    console.log("making call to request");
    const result = await requestAwsData();
    console.log("data recieved from aws", result);
    return result;
};

// now expose with module.exports:
exports.Request = RequestClass;


