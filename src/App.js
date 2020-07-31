import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [result, setResult] = useState(0);

  useEffect(() => {
    fetch("/test").then(res => res.json()).then(data => {
      setResult(data.response)
    })
  }, []);
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <p>Note: the below is done with Flask:</p>
        <p>{result}</p>
      </header>
    </div>
  );
}

export default App;
