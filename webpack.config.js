var webpack = require('webpack');
var ngAnnotatePlugin = require('ng-annotate-webpack-plugin');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var ExtractTextPlugin = require("extract-text-webpack-plugin");
var path = require("path");
var AssetsPlugin = require('assets-webpack-plugin');
var assetsPluginInstance = new AssetsPlugin();
var autoprefixer = require("autoprefixer");

module.exports = {
    context: path.resolve(__dirname, 'app/app'),
    entry: {
        app: './app.js',
        vendor: [
            'angular',
            'angular-ui-router',
            'angular-resource'
        ]
    },
    module: {
        loaders: [
            //https://julienrenaux.fr/2015/03/30/introduction-to-webpack-with-practical-examples/
            {test: /\.css/, loader: ExtractTextPlugin.extract("style-loader", "css-loader")},
            {test: /\.(png|jpg|gif)$/, loader: "file-loader?name=img/[hash:6].[ext]"},
            {test: /\.(eot|otf|woff|woff2|ttf|svg)$/, loader: 'url-loader?limit=30000&name=css/[name].[ext]'}
        ]
    },
    output: {
        path: path.join(__dirname, "app/build"),
        filename: "[name].bundle.js"
    },
    postcss: [
        autoprefixer(),
    ],
    resolve: {
        modulesDirectories: ["web_modules", "node_modules", "bower_components"],
        extensions: ['', '.js', '.jsx']
    },
    plugins: [
        new webpack.HotModuleReplacementPlugin(),
        new webpack.optimize.CommonsChunkPlugin(/* chunkName= */"vendor", /* filename= */"vendor.bundle.js"),
        new ExtractTextPlugin("[name].bundle.css"),
        assetsPluginInstance,
        new ngAnnotatePlugin({add: true, prettyPrint: true}),
        new webpack.ResolverPlugin(
            new webpack.ResolverPlugin.DirectoryDescriptionFilePlugin(".bower.json", ["main"])
        )
    ]
};