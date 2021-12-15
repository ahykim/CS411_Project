import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";
import './App.css';
import Login from './pages/login';
import NavigationBar from './components/NavigationBar';
import Search from './pages/search';
import Home from './pages/index';

function App() {
  return (
    <html>
      <head>
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css"/>
      </head>
      <body>
      <NavigationBar/>
        <Router>
          <Routes>
            <Route exact path='/' component={Home} />
            <Route path='/movie_search' component={Search} />
            <Route path='/login' component={Login} />
          </Routes>
        </Router>
      </body>
    </html>
  );
}

export default App;
