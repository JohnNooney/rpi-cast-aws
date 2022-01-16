import {Table, Space} from 'antd';
const { Column } = Table;

function DataTable() {
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
  