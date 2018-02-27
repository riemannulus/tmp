const path = require('path');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');

module.exports = {
    entry: {
        'matrix': './tmp/assets/matrix.js',
    },
    output: {
        path: path.resolve(__dirname, 'tmp/static'),
        filename: '[name].[chunkhash].js',
    },
    resolve: {
        extensions: ['.js', '.css'],
    },
    module: {
        rules: [
            {
                test: /\.scss$/i,
                use: [
                    'style-loader',
                    'css-loader',
                    'sass-loader',
                ],
            },
            {
                test: /\.(png|svg|jpe?g)$/i,
                use: [{
                    loader: 'file-loader',
                    options: {
                        name: '[name].[ext]',
                    },
                }],
            },
        ]
    },
    plugins: [
        new CleanWebpackPlugin(['./tmp/static']),
        new ManifestRevisionPlugin(path.join('build', 'manifest.json'), {
            rootAssetPath: 'assets',
        }),
    ],
};
