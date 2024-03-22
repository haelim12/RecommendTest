const request = require('request');

const client_id = '8fc753e32c4848c48bdd29b24c92ee53';
const client_secret = '414b7bfaf02b47c28d08a8223d801bff';

const authOptions = {
  url: 'https://accounts.spotify.com/api/token',
  headers: {
    'Authorization': 'Basic ' + Buffer.from(client_id + ':' + client_secret).toString('base64')
  },
  form: {
    grant_type: 'client_credentials'
  },
  json: true
};

request.post(authOptions, function(error, response, body) {
  if (!error && response.statusCode === 200) {
    const token = body.access_token;
    console.log('Access Token:', token);
  } else {
    console.error('Error getting access token:', error);
  }
});
