<template>
  <div class="row">
    <div class="col-md-8">
      <edit-profile-form :model="$userProfileData">
      </edit-profile-form>
    </div>
    <div class="col-md-4">
      <user-card :user="$userProfileData"></user-card>
    </div>
  </div>
</template>
<script>
  import EditProfileForm from './Profile/EditProfileForm';
  import UserCard from './Profile/UserCard';
  import { api } from '@/mixins/apiMixin';

  export default {
   mixins: [api],
    components: {
      EditProfileForm,
      UserCard
    },
    methods: {
      getLoginData()
      {

      }
    },
    mounted() {
      this.getLoginData();
      
    },
    beforeMount() {
      if (!this.checkToken(sessionStorage.getItem('token')))
      {
        window.location.href = `${window.location.origin}/#/`;
      }
    },
    activated() {
      if (!this.checkToken(sessionStorage.getItem('token')))
      {
        window.location.href = `${window.location.origin}/#/`;
      }
    }    
  }
</script>
<style>
</style>
