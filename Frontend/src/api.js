import  axios from 'axios';

//Create an axios instance with a base URL
const api = axios.create({
    baseURL: 'http://127.0.0.1:8078',
});

//export the axios instance for use in other files
export default api;