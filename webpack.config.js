const path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const BundleTracker = require('webpack-bundle-tracker')

const fs = require("fs")

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
    entry: './frontend/index.js',
    output: {
        path: path.resolve(__dirname, 'static/bundles'),
        filename: 'main.js'
    },
    plugins: [
        new MiniCssExtractPlugin({filename: 'main.css',}),
        new BundleTracker({path: __dirname, filename: 'webpack-stats.json'}),
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
                    "css-loader",
                    {
                        loader: "sass-loader",
                        options: {
                            api: "modern-compiler",
                            sassOptions: {
                                logger: {
                                    warn: (message, options) => {
                                        if (options.deprecation) {
//                                            console.warn(message); // Show in console
                                            logWarning(message + "\n" + options.deprecationType.description + "\n" + options.stack); // Write to file
                                        }
                                    },
                                    error: (message, options) => {
//                                        console.error(message); // Show in console
                                        logError(message + "\n" + options.stack); // Write to file
                                    },
                                },
                            },
                        },
                    },
                ],
            },
            {
                test: /\.(png|jpg|jpeg|gif|svg)$/i,
                type: 'asset/resource',
                generator: {
                    filename: 'images/[name][ext]'
                }
            },
            {
                test: /\.(woff|woff2|eot|ttf|otf)$/,
                type: 'asset/resource',
                generator: {
                  filename: 'fonts/[name][ext]',
                },
            },
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
