'use strict';

module.exports = function (grunt) {

  grunt.initConfig({
    uglify: {
      options: {
        banner: '/*! Grunt Uglify <%= grunt.template.today("yyyy-mm-dd") %> */ ',
        compress: {
          drop_console: false
        }
      },
      dist: {
        files: [{
          expand: true,
          cwd: 'public/dist/asr',
          src: ['**/Bootstrap.js', 'Bootstrap.js'],
          dest: 'public/dist/asr',
          ext: '.min.js'
        }]
      }
    },
    sass: {
      dev: {
        options: {
          style: 'expanded',
          loadPath: ['./node_modules/bootstrap-sass/assets/stylesheets/']
        },
        files: [{
          expand: true,
          cwd: 'sass',
          src: ['*.scss'],
          dest: 'public/dist/css',
          ext: '.css'
        }]
      },
      dist: {
        options: {
          style: 'compressed',
          loadPath: ['./node_modules/bootstrap-sass/assets/stylesheets/']
        },
        files: [{
          expand: true,
          cwd: 'sass',
          src: ['*.scss'],
          dest: 'public/dist/css',
          ext: '.min.css'
        }]
      }
    },
    browserify: {
      dist: {
        options: {
          transform: [require('babelify').configure({
            blacklist: ["regenerator", "useStrict"]
          })],
          browserifyOptions: {
            debug: true, // source mapping
            ignoreMTime: true
          }
        },
        files: [{
          expand: true,
          cwd: 'asr',
          src: ['**/Bootstrap.jsx', 'Bootstrap.jsx'],
          dest: 'public/dist/asr',
          ext: '.js'
        }]
      },
      dev: {
        options: {
          watch: true,
          keepAlive: true,
          transform: [require('babelify').configure({
            blacklist: ["regenerator", "useStrict"]
          })],
          browserifyOptions: {
            debug: true, // source mapping
            ignoreMTime: true
          }
        },
        files: [{
          expand: true,
          cwd: 'asr',
          src: ['**/Bootstrap.jsx', 'Bootstrap.jsx'],
          dest: 'public/dist/asr',
          ext: '.min.js' // NOTE mimic uglifyjs has been run
        }]
      }
    },
    postcss: {
      options: {
        map: false,
        processors: [
          require('autoprefixer-core')({
            browsers: ['> 1%', 'last 15 versions', 'Firefox > 20']
          })
        ]
      },
      dist: {
        src: 'public/dist/css/*.css'
      }
    }
  });

  grunt.loadNpmTasks('grunt-browserify');
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-postcss');

  grunt.registerTask('css', ['sass:dist', 'postcss:dist']);
  grunt.registerTask('build', ['sass:dev', 'sass:dist', 'postcss:dist', 'browserify:dist', 'uglify:dist']);
  grunt.registerTask('auto-build', ['sass:dev', 'sass:dist', 'postcss:dist', 'browserify:dev']);
};