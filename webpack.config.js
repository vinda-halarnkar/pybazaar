const path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const BundleTracker = require('webpack-bundle-tracker')

module.exports = {
    entry: './frontend/index.js',
    output: {
        path: path.resolve(__dirname, 'static/bundles'),
        filename: 'main.js'
    },
    plugins: [
        new MiniCssExtractPlugin({filename: 'main.css',}),
        new BundleTracker({path: __dirname, filename: 'webpack-stats.json'}),
    ],
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader'],
            },
            {
                test: /\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    'sass-loader'
                ],
            },
        ]
    }
}
