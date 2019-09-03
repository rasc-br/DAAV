import axios from 'axios';

export const api = {
    data() {
        return {
          apiPath: 'http://127.0.0.1:5000',
          header: {
            'Content-Type': 'multipart/form-data',
          }
        }
    },
    methods:{
        checkToken(jwt){
            if (!jwt || jwt.split('.').length < 3) {
                return false
              }
            const data = JSON.parse(atob(jwt.split('.')[1]));
            const exp = new Date(data.exp * 1000);
            const now = new Date();
            return now < exp;
        },
        async registerUser(userData){
            let result = '';
            axios.post(`${this.apiPath}/register/`, userData, this.header).then((res) => {
                result = res.data;
            }).catch((error) => {
                result = `Register Error: ${error}`;
            });

            return result;
        },
        checkLoginUser(userData){
            return axios.post(`${this.apiPath}/login/`, userData)
        },
        saveUser(){
            return 'User saved';
        }
    }
}