import React from 'react'
import { render } from 'react-dom'
import { createHistory, useBasename } from 'history'
import { Router, Route, Link, IndexRoute } from 'react-router'
import history from './History'

var App = require('./App.jsx');
var Index = require('./index/App.jsx');
var About = require('./about/App.jsx');
var Model = require('./model/App.jsx');
var Record = require('./record/App.jsx');

window.shuffle = function (array) {
  if (!Array.isArray(array)) return [];
  var currentIndex = array.length, temporaryValue, randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
};

render((
  <Router history={history}>
    <Route path="/" component={App}>
      <IndexRoute component={Index} rootClassName="p-index"/>
      <Route path="about" component={About} rootClassName="p-about" {...{
        mode: 'about',
        title: 'About',
        overview: "See all the companies available in the database",
        theme: '#FF5722'
      }}/>
      <Route path=":model" query={{range: 0,offset: 0}} component={Model} rootClassName="p-model" {...{
        companies: {
          mode: 'companies',
          record: 'company',
          title: 'Companies',
          description: "A video game publisher is a company that publishes video games that they have either developed internally or have had developed by a video game developer; while a video game developer is a software developer that specializes in video game development – the process and related disciplines of creating video games.",
          overview: "See all the companies available in the database",
          theme: '#2196F3'
        }, games: {
          mode: 'games',
          record: 'game',
          title: 'Games',
          description: "Structured playing, usually undertaken for enjoyment and sometimes used as an educational tool. Games are distinct from work, which is usually carried out for remuneration, and from art, which is more often an expression of aesthetic or ideological elements.",
          overview: "See all the games available in the database",
          theme: '#FFC107'
        }, platforms: {
          mode: 'platforms',
          record: 'platform',
          title: 'Platforms',
          description: "A video game console is a device that outputs a video signal or visual image to display a video game. The term \"video game console\" is used to distinguish a console machine primarily designed for consumers to use for playing video games in contrast to arcade machines or home computers. It includes home video game consoles, handheld game consoles, microconsoles and dedicated consoles.",
          overview: "See all the platforms available in the database",
          theme: '#8BC34A'
        }
      }}/>
      <Route path=":model/:id" component={Record} rootClassName="p-record"/>
      <Route path="*" component={About}/>
    </Route>
  </Router>
), document.getElementById('app'));