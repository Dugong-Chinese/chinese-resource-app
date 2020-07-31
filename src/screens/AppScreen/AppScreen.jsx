import React, { Component } from "react";
import { Navbar, Nav, NavDropdown } from 'react-bootstrap';

import { Config } from '../../utils/Config';

class AppScreen extends Component {

  isNavLinkActive = (link) => {
    // return link === this.props.location.pathname;
    const { location } = this.props;
    return location.pathname.startsWith(link);
  }

  render() {
    const { history } = this.props;
    return (
      <Navbar collapseOnSelect expand="md" bg="danger" variant="dark">
        <Navbar.Brand href="#">{Config.appName}</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="mr-auto">
            <Nav.Link onClick={() => { history.push('/search'); }} active={this.isNavLinkActive('/search')}>Search</Nav.Link>
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
          </Nav>
        </Navbar.Collapse>
      </Navbar>


    )
  }

}

export default AppScreen;