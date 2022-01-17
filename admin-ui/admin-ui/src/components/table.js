import {Table, Space} from 'antd';

// Create service client module using ES6 syntax.
import {ScanCommand } from "@aws-sdk/client-dynamodb";
import { ddbClient } from '../libs/ddbClient';

const { Column } = Table;




// Set the parameters.
export const params = {
// Specify which items in the results are returned.
// FilterExpression: "Subtitle = :topic AND Season = :s AND Episode = :e",
// // Define the expression attribute value, which are substitutes for the values you want to compare.
// ExpressionAttributeValues: {
//     ":topic": { S: "SubTitle2" },
//     ":s": { N: "1" },
//     ":e": { N: "2" },
// },
// Set the projection expression, which the the attributes that you want.
ProjectionExpression: "log-hash, log-sort, session, status, duration, fault, restarts",
TableName: "dbb-test",
};

export const run = async () => {
    try {
        const data = await ddbClient.send(new ScanCommand(params));
        
        data.Items.forEach(function (element, index, array) {
            console.log(element);
        });
        console.log("All data: ", data);
        return data;
    } catch (err) {
        console.log("Error", err);
    }
}


function DataTable() {
    var data =  run();
    console.log("All data in test: ", data);

    return (
        <Table dataSource={json_data} id="admin-table">
            <Column title="Timestamp" dataIndex="log-hash" key="log-hash" />
            <Column title="User" dataIndex="log-sort" key="log-sort"/>
            <Column title="Session" dataIndex="session" key="session" />
            <Column title="Status" dataIndex="status" key="status" />
            <Column title="Duration" dataIndex="duration" key="duration" />
            <Column title="Fault" dataIndex="fault" key="fault" />
            <Column title="Restart" dataIndex="restarts" key="restarts" />
            <Column
                title="Action"
                key="action"
                render={(text, record) => (
                    <Space size="middle">
                    <a>Update</a>
                    <a>Delete</a>
                    </Space>
                )}
            />
      </Table>
    );
}

const json_data = [{
  "log-hash":"2022-01-13 13:38:45.662000+00:00",
  "log-sort":"tester",
  "session": 1,
  "status": "active",
  "duration": "6:38:45",
  "fault": "none",
  "restarts": 0
  },
  {
  "log-hash":"2022-02-13 13:38:45.662000+00:00",
  "log-sort":"tester2",
  "session": 2,
  "status": "finished",
  "duration": "2:38:45",
  "fault": "none",
  "restarts": 0
  }
]
  


// const dataSource = [
//     {
//       sort: json_data["log-sort"],
//       session: json_data["log-sort"],
//       status: json_data["status"],
//       duration: json_data["duration"],
//       fault: json_data["fault"],
//       restarts: json_data["restarts"]
//     },
//     {
//       key: '2',
//       name: 'John',
//       age: 42,
//       address: '10 Downing Street',
//     },
//   ];
  
export default DataTable;
  