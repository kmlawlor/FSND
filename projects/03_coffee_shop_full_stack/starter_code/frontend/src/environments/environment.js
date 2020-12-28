"use strict";
/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */
exports.__esModule = true;
exports.environment = void 0;
exports.environment = {
    production: false,
    apiServerUrl: 'http://127.0.0.1:5000',
    auth0: {
        url: 'kml.us.auth0.com',
        audience: 'coffeshop',
        clientId: 'Dwois70Gj3eLcQWaJhBH3IY4jla86GhH',
        callbackURL: 'http://127.0.0.1:5000/drinks-detail'
    }
};
