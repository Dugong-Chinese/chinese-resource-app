import React, { Component } from "react";
import { Navbar, Nav, NavDropdown } from 'react-bootstrap';
import { Router, Switch, Redirect, Route } from "react-router-dom";
import Login from '../../components/Login/Login';


import { Config } from '../../utils/Config';

import HomeScreen from '../HomeScreen/HomeScreen';
import ResourceScreen from '../ResourceScreen/ResourceScreen';

class AppScreen extends Component {

  isNavLinkActive = (link) => {
    // return link === this.props.location.pathname;
    const { location } = this.props;
    return location.pathname.startsWith(link);
  }

  render() {
    const { history } = this.props;
    return (
      <>
      <Navbar sticky="top" collapseOnSelect expand="md" bg="danger" variant="dark">
        <Navbar.Brand href="#">{Config.appName}</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="mr-auto">
            <Nav.Link onClick={() => { history.push('/search'); }} active={this.isNavLinkActive('/search')}>Advanced Search</Nav.Link>
          </Nav>
          <Nav>
            <NavDropdown title="Profile" id="profile-actions-nav-dropdown">
              <NavDropdown.Item onClick={this.generate}>
                <i className="fa fa-user pr-2" />
                Profile
              </NavDropdown.Item>
              <NavDropdown.Item onClick={this.deploy}>
                <i className="fa fa-book pr-2" />
                My Vocabulary
              </NavDropdown.Item>
              <NavDropdown.Item onClick={this.killServer}>
                <i className="fa fa-sign-out-alt pr-2" />
                Logout
              </NavDropdown.Item>
            </NavDropdown>
            <Nav.Link onClick={() => { history.push('/search'); }} active={this.isNavLinkActive('/search')}>Contact</Nav.Link>
            {!!true && <Nav.Link onClick={this.logout}>Logout</Nav.Link>}
            <Login></Login>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
      
      {/* navbar ends here, app container begins here */}
      {/* <div style={{flex: 0.95, overflow: 'scroll'}}> */}
        <Switch>
          <Route exact path="/" component={HomeScreen} />
          <Route path="/resource" component={ResourceScreen} />
        </Switch>
      {/* </div> */}
      </>
    )
  }

}

export default AppScreen;