//use "webpack --config webpack.production.config.js -p" for production mode
const webpack = require('webpack');
const WebpackStripLoader = require('strip-loader');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const devConfig = require('./common.js');
const stripLoader = {
    test: [/\.js?$/, /\.es6$/],
    include: /src/,
    loader: WebpackStripLoader.loader('console.log', 'console.error', 'debugger')
};

devConfig.module.rules.push(stripLoader);


devConfig.devtool = "source-map";

// remove open browser plugin
devConfig.plugins.pop();

devConfig.plugins.push(new webpack.optimize.OccurrenceOrderPlugin());


devConfig.plugins.push(new webpack.LoaderOptionsPlugin({
    minimize: true,
    debug: false
}));

devConfig.plugins.push(new UglifyJsPlugin({
    parallel: 4
}));

devConfig.plugins.push(new webpack.DefinePlugin({'process.env.NODE_ENV': '"production"'}));


module.exports = devConfig;
