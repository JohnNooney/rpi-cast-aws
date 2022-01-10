import {Table, Space} from 'antd';
const { Column, ColumnGroup } = Table;

function DataTable() {
    return (
        <Table dataSource={dataSource} id="admin-table">
            <Column title="Name" dataIndex="name" key="name" />
            <Column title="Age" dataIndex="age" key="age" />
            <Column title="Address" dataIndex="address" key="address" />
            <Column
                title="Action"
                key="action"
                render={(text, record) => (
                    <Space size="middle">
                    <a>Invite {record.lastName}</a>
                    <a>Delete</a>
                    </Space>
                )}
            />
      </Table>
    );
}

const dataSource = [
    {
      key: '1',
      name: 'Mike',
      age: 32,
      address: '10 Downing Street',
    },
    {
      key: '2',
      name: 'John',
      age: 42,
      address: '10 Downing Street',
    },
  ];
  
export default DataTable;
  