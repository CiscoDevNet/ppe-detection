const {resolve} = require('path');
const fs = require('fs');
const path = require('path');
const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const OpenBrowserPlugin = require('open-browser-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const packagejson = require('../../package.json');
const CreateFileWebpack = require('create-file-webpack');

/*
Config

if deploy on stage or production

 */

const staging_host = "https://static.testing.devnetcloud.com";
const prod_host = "https://static.production.devnetcloud.com";

const envconfig = require('../env/dev.json');
const stageenvconfig = require('../env/stage.json');
const prodenvconfig = require('../env/production.json');

const BASENAME = envconfig.config.BASENAME;

//update app links
let app_path = "/" + BASENAME.replace("/", "-");

// merge config
if (process.env.NODE_ENV) {
    //config will merged
    const _envconfig = process.env.NODE_ENV == "production" ? prodenvconfig : stageenvconfig;
    //append absolute stage/prod static resource link
    app_path = process.env.NODE_ENV == "production" ? prod_host + app_path : staging_host + app_path;
    envconfig.js = Object.assign(envconfig.js, _envconfig.js);
    envconfig.css = Object.assign(envconfig.css, _envconfig.css);
    envconfig.window = Object.assign(envconfig.window, _envconfig.window);
    envconfig.config = Object.assign(envconfig.config, _envconfig.config);

}

// update app js/css link to `absolute` link
Object.keys(envconfig.js).forEach(function (key) {
    if (key.startsWith("*")) {
        envconfig.js[key] = app_path + envconfig.js[key];
    }
});

Object.keys(envconfig.css).forEach(function (key) {
    if (key.startsWith("*")) {
        envconfig.css[key] = app_path + envconfig.css[key];
    }
});


const webconfig = {
    devtool: 'cheap-module-eval-source-map',
    entry: [
        './script/main.jsx',
        './script/scss/main.scss',
    ],
    output: {
        filename: 'app.js',
        path: resolve(__dirname, '../../dist')
    },
    resolve: {
	extensions: [".js", ".jsx"],
        alias: {
            "utils": resolve(__dirname, '../../app/script/utils.jsx'),
            "Pages": resolve(__dirname, '../../app/script/pages'),
            "Parts": resolve(__dirname, '../../app/script/parts'),
            "Utils": resolve(__dirname, '../../app/script/utils'),
            "Components": resolve(__dirname, '../../app/script/components')
        }
    },

    context: resolve(__dirname, '../../app'),

    devServer: {
        hot: true,
        disableHostCheck: true,
        contentBase: resolve(__dirname, '../../build'),
        publicPath: '/' + BASENAME + '/',
        historyApiFallback: {
            disableDotRule: true,
            index: '/' + BASENAME + '/index.html',
            rewrites: [{
                from: /\.hot-update\.json$/,
                to: function (context) {
                    return '/' + path.basename(context.parsedUrl.pathname);
                }
            }, {
                from: /\.hot-update\.js$/,
                to: function (context) {
                    return '/' + path.basename(context.parsedUrl.pathname);
                }
            }]
        },
	proxy: [{
	    context: "/socket.io",
            target: "ws://localhost:7030",
	    ws: true,
	    secure: false
        }, {
            context: ['/v1', '/apidocs'],
            target: "http://localhost:7030",
            secure: false
        }]
    },

    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                loaders: [
                    'babel-loader',
                ],
                exclude: /node_modules/
            },
            {
                test: /\.(scss|css)$/,
                use: ExtractTextPlugin.extract({
                    fallback: 'style-loader',
                    use: [
                        'css-loader',
                        {
                            loader: 'sass-loader',
                            query: {
                                sourceMap: false,
                                data: '@import "./node_modules/dui/assets/scss/dui.share.scss";'
                            }
                        }
                    ],
                    publicPath: '../'
                })
            },
            {
                test: /\.(png|jpg|gif)$/,
                use: [
                    {
                        loader: 'url-loader',
                        options: {
                            limit: 8192, // 8k
                            mimetype: 'image/png',
                            name: 'images/[path][name].[ext]'
                        }
                    }
                ],
            },
            {
                test: /\.eot(\?v=\d+.\d+.\d+)?$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            limit: 8192,
                            name: 'fonts/[name].[ext]'
                        }
                    }
                ],
            },
            {
                test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                use: [
                    {
                        loader: 'url-loader',
                        options: {
                            mimetype: 'application/font-woff',
                            name: 'fonts/[name].[ext]',
                        }
                    }
                ],
            },
            {
                test: /\.[ot]tf(\?v=\d+.\d+.\d+)?$/,
                use: [
                    {
                        loader: 'url-loader',
                        options: {
                            mimetype: 'application/octet-stream',
                            name: 'fonts/[name].[ext]',
                        }
                    }
                ],
            },
            {
                test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
                use: [
                    {
                        loader: 'url-loader',
                        options: {
                            limit: 8192,
                            mimetype: 'image/svg+xml',
                            name: 'images/[path][name].[ext]',
                        }
                    }
                ],
            },
        ]
    },

    plugins: [
        new webpack.DefinePlugin({
            'CONFIG': JSON.stringify(envconfig.config)
        }),
        new HtmlWebpackPlugin({
            inject: false,
            title: packagejson.title,
            name: packagejson.name,
            version: packagejson.version,
            description: packagejson.description,
            keywords: packagejson.keywords,
            commitid: process.env["DRONE_COMMIT"] || (new Date()).getTime(),
            env: process.env.NODE_ENV,
            hash: true,
            css: Object.values(envconfig.css),
            js: Object.values(envconfig.js),
            window: envconfig.window,
            filename: 'index.html',
            template: '../template/index.html'
        }),
        new ExtractTextPlugin({filename: './styles/style.css', disable: false, allChunks: true}),
        new CopyWebpackPlugin([{from: 'vendors', to: 'vendors'}, {from: 'assets', to: 'assets'}]),
        new CreateFileWebpack({
            path: './dist',
            fileName: 'app.config.json',
            content: JSON.stringify(envconfig)
        }),
        new CreateFileWebpack({
            path: './dist',
            fileName: 'app.env.json',
            content: JSON.stringify(process.env)
        }),
        new webpack.optimize.ModuleConcatenationPlugin(),
        new webpack.HotModuleReplacementPlugin()
    ],
};


module.exports = webconfig;
