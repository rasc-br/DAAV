<template>
  <card>
    <h5 slot="header" class="title">Edit Profile</h5>
    <div class="row">
      <div class="col-md-3 pr-md-1">
        <base-input label="Username"
                    v-model="model.username"
                    disabled>
        </base-input>
      </div>
      <div class="col-md-5 px-md-1">
        <base-input label="Email address"
                    v-model="model.email"
                    type="email">
        </base-input>
      </div>
    </div>
    <div class="row">
      <div class="col-md-6 pr-md-1">
        <base-input label="First Name"
                  v-model="model.firstname">
        </base-input>
      </div>
      <div class="col-md-6 pl-md-1">
        <base-input label="Last Name"
                  v-model="model.lastname">
        </base-input>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <base-input label="Address"
                  v-model="model.address">
        </base-input>
      </div>
    </div>
    <div class="row">
      <div class="col-md-4 pr-md-1">
        <base-input label="City"
                  v-model="model.city">
        </base-input>
      </div>
      <div class="col-md-4 px-md-1">
        <base-input label="Country"
                  v-model="model.country">
        </base-input>
      </div>
      <div class="col-md-4 pl-md-1">
        <base-input label="Postal Code"
                    v-model="model.postalcode">
        </base-input>
      </div>
    </div>
    <div class="row">
      <div class="col-md-8">
        <base-input>
          <label>About Me</label>
          <textarea rows="4" cols="80"
                    class="form-control"
                    placeholder="Here can be your description"
                    v-model="model.about">
          </textarea>
        </base-input>
      </div>
    </div>
    <base-button slot="footer" type="primary" fill @click="saveProfile">Save</base-button>
  </card>
</template>
<script>
  import { api } from '@/mixins/apiMixin';
  import NotificationTemplate from '@/pages//Notifications/NotificationTemplate';

  export default {
    mixins: [api],    
    props: {
      model: {
        type: Object,
        default: () => {
          return {};
        }
      }
    },
    data(){
      return {
        profileStatus: '',
      }
    },        
  watch: {
    profileStatus: function (val) {
      if (val == 'SUCCESS')
      {
        this.$notify({
          component: NotificationTemplate,
          icon: "tim-icons icon-check-2",
          horizontalAlign: 'center',
          verticalAlign: 'top',
          type: 'success',
          message: `Profile edited successfully!`,
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
          message: `Error editing profile`,
          timeout: 5000
        });
      }
    },
  },      
    methods: {
      async saveProfile(){
        this.profileStatus = '';
        await this.editProfile(this.$userProfileData);
        this.profileStatus = this.tempResult;
      },
    }
  }
</script>
<style>
</style>
