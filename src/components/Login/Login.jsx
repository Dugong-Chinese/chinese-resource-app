import React, { Component } from "react";
import { Modal, Button, Image, Form, Input, Checkbox } from "antd";

class Login extends Component {
  isNavLinkActive = link => {
    // return link === this.props.location.pathname;
    const { location } = this.props;
    return location.pathname.startsWith(link);
  };

  state = {
    loginModal: false
  };

  isModalVisable(loginModal) {
    this.setState({ loginModal });
  }

  onFinish = values => {
    console.log("Success:", values);
  };

  onFinishFailed = errorInfo => {
    console.log("Failed:", errorInfo);
  };

  render() {
    return (
      <>
        <Button type="primary" onClick={() => this.isModalVisable(true)}>
          Login
        </Button>
        <Modal
          title="Welcome Back"
          centered
          visible={this.state.loginModal}
          onOk={() => this.isModalVisable(false)}
          onCancel={() => this.isModalVisable(false)}
        >
          <Image width={200} src="../../logo.svg" />
          <Form name="basic" initialValues={{ remember: true }}>
            <Form.Item
              label="Username"
              name="username"
              rules={[
                { required: true, message: "Please input your username!" }
              ]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              label="Password"
              name="password"
              rules={[
                { required: true, message: "Please input your password!" }
              ]}
            >
              <Input.Password />
            </Form.Item>

            <Form.Item name="remember" valuePropName="checked">
              <Checkbox>Remember me</Checkbox>
            </Form.Item>

            <Form.Item>
              <Button type="primary" htmlType="submit">
                Submit
              </Button>
            </Form.Item>
          </Form>
        </Modal>
      </>
    );
  }
}

export default Login;
