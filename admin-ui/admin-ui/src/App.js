import logo from './logo.svg';
import './App.css';
import 'antd/dist/antd.css';
import DataTable from './components/table';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>Admin Log Manager</p>
      </header>
      <DataTable/>
    </div>
  );
}

export default App;
