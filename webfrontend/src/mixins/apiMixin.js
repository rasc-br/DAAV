import axios from 'axios';

export const api = {
    data() {
        return {
          apiPath: 'http://127.0.0.1:5000',
          header: {'Content-Type': 'multipart/form-data'},
          status: '',
          token: '',
          tempResult: '',
          loginData: '',
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
            let self = this;
            await axios.post(`${this.apiPath}/register/`, userData, this.header).then((res) => {
                self.status = res.data;
            }).catch((error) => {
                self.status = `Register Error: ${error}`;
            });
        },
        async loginUser(userData){
            let self = this;
            this.loginData='';
            await axios.post(`${this.apiPath}/login/`, userData, this.header).then((res) => {
                if (res.data.token)
                {
                    self.token = res.data.token;
                    // this.$userProfileData = res.data;
                    Object.keys(res.data).forEach((key) => {
                        if (res.data[key] && res.data[key] != 'none')
                        {
                            this.$userProfileData[key] = res.data[key];
                        }
                    });
                }
                else
                {
                    self.token = res.data;
                }
            }).catch((error) => {
               self.token = error;
            });
        },       
        checkLoginUser(userData){
            return axios.post(`${this.apiPath}/login/`, userData)
        },
        async editProfile(profileData){
            await axios.post(`${this.apiPath}/edit_profile/`, profileData, this.header).then((res) => {
                this.tempResult = res.data;
            }).catch((error) => {
                this.tempResult = error;
            });
        },        
        saveUser(){
            return 'User saved';
        }
    }
}