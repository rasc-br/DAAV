<template>
  <card type="user">
    <p class="card-text">
    </p>
    <div class="author">
      <div class="block block-one"></div>
      <div class="block block-two"></div>
      <div class="block block-three"></div>
      <div class="block block-four"></div>
      <a href="#">
        <input type="file" id="chooseFile" ref="chooseFile" style="display: none" @change="onFileChange">
        <img class="avatar" :src="$userProfileData.avatar" @click="selectNewAvatar">
        <h5 class="title">{{user.firstname}} {{user.lastname}}</h5>
      </a>
      <p class="description">
        {{user.type}}
      </p>
    </div>
    <p></p>
    <p class="card-description">
      {{user.about}}
    </p>
  </card>
</template>
<script>
import { api } from '@/mixins/apiMixin';
import NotificationTemplate from '@/pages//Notifications/NotificationTemplate';

export default {
  mixins: [api],  
  props: {
    user: {
      type: Object,
      default: () => {
        return {};
      }
    }
  },
  data(){
    return {
      imgEditStatus: '',
    }
  },
  watch: {
    imgEditStatus: function (val) {
      if (val == 'SUCCESS')
      {
        this.$notify({
          component: NotificationTemplate,
          icon: "tim-icons icon-check-2",
          horizontalAlign: 'center',
          verticalAlign: 'top',
          type: 'success',
          message: `Profile avatar changed!`,
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
          message: `Error editing profile image`,
          timeout: 5000
        });
      }
    },
  },  
  methods: {
    selectNewAvatar() {
        document.getElementById("chooseFile").click();
    },
    async onFileChange(e){
      // let self = this;
      let files = e.target.files || e.dataTransfer.files;
      if (!files.length)
        return;
      let avatarFile = files[0];

      const toBase64 = file => new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.readAsDataURL(file);
          reader.onload = () => resolve(reader.result);
          reader.onerror = error => reject(error);
      });

      let fileBase64 = await toBase64(avatarFile);

      // let profileData = {username: this.user.username, img: fileBase64, imgtype: avatarFile.type};
      this.imgEditStatus = '';

      this.$userProfileData.avatar = fileBase64;

      await this.editProfile(this.$userProfileData);
      this.imgEditStatus = this.tempResult;

      // if (this.imgEditStatus == 'SUCCESS')
      // {
      //   self.$userProfileData.avatar = fileBase64;
      // }
    },
  }
}
</script>
<style>
</style>
