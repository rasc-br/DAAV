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
                    Object.keys(res.data).forEach((key) => {
                        if (res.data[key] && res.data[key] != 'none')
                        {
                            if (key!='type')
                            {
                                this.$userProfileData[key] = res.data[key];
                            }
                            else
                            {
                                this.$userProfileData[key] = res.data[key]==1 ? 'Simple User' : 'Experienced User';
                                this.$userProfileData[key] = res.data[key]==100 ? 'God' : this.$userProfileData[key];
                            }
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
        analizeMD5(choosenMD5){
            let apk = {'md5':choosenMD5, 'username':this.$userProfileData.username};
            return axios.post(`${this.apiPath}/apkscan`, apk, this.header).then((res) => {
                this.tempResult = {'message':res.data.message,'status':'SUCCESS'};
            }).catch((error) => {
                this.tempResult = {'message':error.response.data.message,'status':'FAIL'};
            });
        },     
        async getResultsList(){
            let info = {'username':this.$userProfileData.username};
            await axios.post(`${this.apiPath}/resultlist`, info, this.header).then((res) => {
                this.tempResult = {'allResults':res.data,'status':'GotResults'};
            }).catch((error) => {
                this.tempResult = {'message':error.response.data.message,'status':'FAIL'};
            });
        },                    
    }
}