import React, { useState, useEffect } from 'react';
import useMediaQuery from '@material-ui/core/useMediaQuery';
// import logo from './logo.svg';
import './App.css';
import { Router, Switch, Redirect, Route } from "react-router-dom";
import { Provider } from "react-redux";
import { createMuiTheme, ThemeProvider } from "@material-ui/core/styles";
import CssBaseline from '@material-ui/core/CssBaseline';
import AppScreen from './screens/AppScreen/AppScreen';
import store from "./utils/managers/ReduxStoreManager";
import history from "./utils/history";

// css libraries go here 
import 'bootstrap/dist/css/bootstrap.min.css';

import "@fortawesome/fontawesome-free/css/all.min.css";

function App() {
  const [result, setResult] = useState(0);
  useEffect(() => {
    fetch("/api/multiply/10").then(res => res.json()).then(data => {
      setResult(data)
      console.log(data)
      // if you open up the console on the site you will see a Result object with result: 100, this means there was a success
    })
  }, []);

  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');

  const theme = React.useMemo(
    () =>
      createMuiTheme({
        palette: {
          // type: prefersDarkMode ? 'dark' : 'light',
        },
        typography: {
          fontSize: 14,
          fontFamily: [
            "Open Sans",
            "-apple-system",
            "BlinkMacSystemFont",
            '"Segoe UI"',
            "Roboto",
            '"Helvetica Neue"',
            "Arial",
            "sans-serif",
            '"Apple Color Emoji"',
            '"Segoe UI Emoji"',
            '"Segoe UI Symbol"',
          ].join(","),
        },
      }),
    [prefersDarkMode],
  );

  return (
    <div className="App">
      <Provider store={store}>
        <Router history={history}>
          <ThemeProvider theme={theme}>
            <CssBaseline/>
            <Route path="/" component={AppScreen} />
          </ThemeProvider>
        </Router>
      </Provider>
    </div>
  );
}

export default App;
