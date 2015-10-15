/**
 * @jsx React.DOM
 */

/**
 *  For rendering the app on client side.
 */
var React = require('react');
var App = require('./App.jsx');

if (typeof window !== 'undefined') {

    window.onload = function () {
        React.render(<App />, document.getElementsByTagName('body')[0]);
    };

    window.React = React;
}