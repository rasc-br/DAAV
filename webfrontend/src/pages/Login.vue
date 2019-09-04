<template>
  <div class="login centered">
    <div class="login-header">
      <h1>appSentinel</h1>
    </div>
    <div class="login-form">
      <span class="login-text">Username:</span>
      <input type="text" v-model="username" placeholder="Username"/><br>
      <span class="login-text">Password:</span>
      <input type="password" v-model="password" placeholder="Password"/>
      <br><br>
      <input type="button" v-on:click="onSubmit" value="Login" class="login-button"/>
      <br>
      <a class="sign-up" v-on:click="register">Sign Up!</a>
    </div>
  </div>
</template>

<script>
import { api } from '@/mixins/apiMixin';
import NotificationTemplate from './Notifications/NotificationTemplate';

export default {
  mixins: [api],
  data() {
      return {
        username: '',
        password: '',
      }
  },
  watch: {
    status: function (val) {
      if (val == 'SUCCESS')
      {
        this.$notify({
          component: NotificationTemplate,
          icon: "tim-icons icon-check-2",
          horizontalAlign: 'center',
          verticalAlign: 'top',
          type: 'success',
          message: `User ${this.username} registered successfully!`,
          timeout: 5000
        });              
      }
      else if (val!='')
      {
        this.$notify({
          component: NotificationTemplate,
          icon: "tim-icons icon-alert-circle-exc",
          horizontalAlign: 'center',
          verticalAlign: 'top',
          type: 'warning',
          message: `Database error!`,
          timeout: 5000
        });
      }
    },
  },
  methods: {
        onSubmit()
        {
          if (this.username && this.username.length>1 && this.password && this.password.length>1)
          {
            // Promise send for authentication
            sessionStorage.setItem('token', '1234');
            sessionStorage.setItem('username', this.username);
            window.location.href = `${window.location.origin}/#/main/dashboard`;
          }
          else
          {
            alert('You must fill username and password');
          }
        },
        register()
        {
          if (this.username && this.username.length>1 && this.password && this.password.length>1)
          {
            let userData = {username: this.username, password: this.password};
            this.registerUser(userData);
            this.status = '';
          }
          else
          {
             this.$notify({
              component: NotificationTemplate,
              icon: "tim-icons icon-alert-circle-exc",
              horizontalAlign: 'center',
              verticalAlign: 'top',
              type: 'warning',
              message: `You must fill username and password`,
              timeout: 5000
            });
          }
        }
  }
};
</script>

<style>
body {
  margin:0px;
  font-family: 'Ubuntu', sans-serif;
	background-size: 100% 110%;
}
.centered {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
h1, h2, h3, h4, h5, h6, a {
  margin:0; padding:0;
}
.login-text {
  margin:0 px;
  font-size: 20px;
  color: #ffff;
  float: left;
  padding-left: 20px;
}
.login {
  margin:0 auto;
  max-width:800px;
  width: 500px;
}
.login-header {
  color:#fff;
  text-align:center;
  font-size:300%;
}
.login-form {
  border:.5px solid #fff;
  background:#525f7f;
  border-radius:10px;
  box-shadow:0px 0px 10px #000;
}
.login-form h3 {
  text-align:left;
  margin-left:40px;
  color:#fff;
}
.login-form {
  box-sizing:border-box;
  padding-top:15px;
  margin:8% auto;
  text-align:center;
  min-height: 320px;
}
.login input[type="text"],
.login input[type="password"] {
  max-width:400px;
	width: 80%;
  line-height:3em;
  font-family: 'Ubuntu', sans-serif;
  margin:1em 2em;
  border-radius:5px;
  border:2px solid #f2f2f2;
  outline:none;
  padding-left:10px;
}
.login-form input[type="button"] {
  height:30px;
  width:100px;
  background:#fff;
  border:1px solid #f2f2f2;
  border-radius:20px;
  color: slategrey;
  text-transform:uppercase;
  font-family: 'Ubuntu', sans-serif;
  cursor:pointer;
}
.sign-up{
  color:#f2f2f2 !important;
  margin-left:-70%;
  cursor:pointer;
  text-decoration:underline;
  margin-bottom: 10px;
}
.no-access {
  color:#E86850;
  margin:20px 0px 20px -57%;
  text-decoration:underline;
  cursor:pointer;
}
.try-again {
  color:#f2f2f2;
  text-decoration:underline;
  cursor:pointer;
}

/*Media Querie*/
@media only screen and (min-width : 150px) and (max-width : 530px){
  .login-form h3 {
    text-align:center;
    margin:0;
  }
  .sign-up, .no-access {
    margin:10px 0;
  }
  .login-button {
    margin-bottom:10px;
  }
}
</style>
