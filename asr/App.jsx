import React from 'react'

const App = React.createClass({
  render() {
    return (
      <div className={"full " + this.props.routes[this.props.routes.length - 1].rootClassName}>
        {this.props.children}
      </div>
    )
  }
});

module.exports = App;