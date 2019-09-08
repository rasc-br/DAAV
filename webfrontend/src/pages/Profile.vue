<template>
  <div class="row">
    <div class="col-md-8">
      <edit-profile-form :model="profile">
      </edit-profile-form>
    </div>
    <div class="col-md-4">
      <user-card :user="profile"></user-card>
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
    data() {
      return {
        profile: {
          email: 'songoku@universe7.com',
          username: sessionStorage.getItem('username'),
          firstName: 'Son',
          lastName: 'Goku',
          address: 'Grandpa Gohan House',
          city: 'Mount Paozu',
          country: 'Universe 7',
          about: 'Osu, ora Gokuu',
          avatar: 'img/goku.jpg',
          type: 'Simple User'
        },
      }
    },
    methods: {

    },
    mounted() {
      // Get Profile
      // if (result.avatar)
      // {
        // this.profile.avatar = result.avatar;
      // }
      
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
