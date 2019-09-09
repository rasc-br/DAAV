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
        <img class="avatar" :src="avatar" @click="selectNewAvatar">
        <h5 class="title">{{user.firstName}} {{user.lastName}}</h5>
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
      avatarFile: '',
      imgEditStatus: '',
      avatar: this.user.avatar,
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
      let self = this;
      let files = e.target.files || e.dataTransfer.files;
      if (!files.length)
        return;
      this.avatarFile = files[0];

      let profileData = {username: this.user.username, img: this.avatarFile};
      this.imgEditStatus = '';

      await this.editProfile(profileData);
      this.imgEditStatus = this.tempResult;

      if (this.imgEditStatus == 'SUCCESS')
      {
        let reader  = new FileReader();
        reader.onloadend = function () {
         self.avatar = reader.result;
        }
        reader.readAsDataURL(this.avatarFile);
      }
    },
  }
}
</script>
<style>
</style>
