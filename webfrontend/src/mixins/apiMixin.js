export const api = {
    methods:{
        checkToken(){
            // Call Api to check token
            let token = sessionStorage.getItem('token');
            return token;
        },
        saveUser(){
            return 'User saved';
        }
    }
}