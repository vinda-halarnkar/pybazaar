const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const BundleTracker = require('webpack-bundle-tracker');
const webpack = require("webpack");
const CopyWebpackPlugin = require("copy-webpack-plugin");
const fs = require("fs");

// Define log file path
const logFilePath = path.resolve("sass-warnings.log")

// Function to append warnings to the log file
function logWarning(message) {
    fs.appendFileSync(logFilePath, `[${new Date().toISOString()}] WARNING:  ${message}\n`, "utf8");
}

function logError(message) {
    fs.appendFileSync(logFilePath, `[${new Date().toISOString()}] ERROR:  ${message}\n`, "utf8");
}

module.exports = {
    entry: {
        main: './frontend/index.js',   // Main entry (includes main.scss)
        product: './frontend/src/styles/product.scss',  // Product-specific CSS
    },
    output: {
        path: path.resolve(__dirname, 'static/bundles'),
        filename: '[name].js'
    },
    plugins: [
        new MiniCssExtractPlugin({filename: '[name].css',}),
        new BundleTracker({path: __dirname, filename: 'webpack-stats.json'}),
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery",
            "window.jQuery": "jquery",
        }),
        new CopyWebpackPlugin({
            patterns: [
                { from: 'frontend/src/img', to: path.resolve(__dirname, 'static/images'), noErrorOnMissing: true },
            ],
        }),
    ],
    resolve: {
        extensions: [".scss", ".css", ".js"],
        modules: ["node_modules"],
    },
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
                    {
                        loader: "css-loader",
                        options: {
                            url: {
                                filter: (url, resourcePath) => {
                                    let condition = !url.includes("static/images");
                                    return condition;
                                }
                            }
                        }
                    },
                    {
                        loader: "sass-loader",
                        options: {
                            api: "modern-compiler",
                            sassOptions: {
                                logger: {
                                    warn: (message, options) => {
                                        if (options.deprecation) {
                                            logWarning(message + "\n" + options.deprecationType.description + "\n" + options.stack);
                                        }
                                    },
                                    error: (message, options) => {
                                        logError(message + "\n" + options.stack);
                                    },
                                },
                            },
                        },
                    },
                ],
            },
            {
                // Process only images from node_modules (ignore theme images)
                test: /\.(png|jpg|jpeg|gif|svg)$/i,
                type: 'asset/resource',
                generator: {
                    filename: '../images/[name][ext]'
                },
                issuer: [/node_modules/],
            },
            // {
            //     // Process only fonts from node_modules (ignore theme fonts)
            //     test: /\.(woff|woff2|eot|ttf|otf)$/,
            //     type: 'asset/resource',
            //     generator: {
            //         filename: '../fonts/[name][ext]',
            //     },
            //     issuer: [/node_modules/],
            // },
        ]
    },
    watchOptions: {
        ignored: /node_modules/, // Ignore unnecessary file changes
        poll: 1000, // Check for file changes every second (helps in Docker)
    },
    stats: {
        errorDetails: true,
    },
}
