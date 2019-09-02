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
        <input type="file" id="chooseFile" style="display: none" @change="onFileChange">
        <img class="avatar" :src="user.avatar" @click="selectNewAvatar">
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
  export default {
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
      }
    },
    methods: {
      selectNewAvatar() {
         document.getElementById("chooseFile").click();
      },
      onFileChange(e){
        let files = e.target.files || e.dataTransfer.files;
        if (!files.length)
         return;
        this.avatarFile = files[0];
        // Upload this.avatarFile to API
        // Change user.avatar to new file uploaded
      },
    }
  }
</script>
<style>
</style>
