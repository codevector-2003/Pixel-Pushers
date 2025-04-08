import  axios from 'axios';

//Create an axios instance with a base URL
const api = axios.create({
    baseURL: 'http://52.140.41.112:80',
});

//export the axios instance for use in other files
export default api;