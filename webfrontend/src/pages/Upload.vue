<template>
<div>
  <div class="card">
    <div class="card-header">
      <h5 class="title">Upload APK - Choose a file from your computer to send for analysis</h5>
    </div>
    <div class="card-body">
      <div class="row">
        <div class="col-12">
          <div class="font-icon-detail">
            <div class="col-md-6 pr-md-1" style="text-align: center; display: inline-block;">
              <input type="file" id="chooseFile" ref="chooseFile" style="display:none;" v-on:change="handleFileUpload()"/>
              <base-button type="file" @click="chooseFile" >Upload file</base-button> <br/>
              <h4 v-if="choosenFile">{{choosenFile.name}}</h4>
              <base-button type="primary" @click="goAnalyzeFile" >Analyze!</base-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="card">
    <div class="card-header">
      <h5 class="title">Get from Aptoide - Insert a MD5 to analyze directly from Aptoide</h5>
    </div>
    <div class="card-body">
      <div class="row">
        <div class="col-12">
          <div class="font-icon-detail">
            <div class="col-md-6 pr-md-1" style="text-align: center; display: inline-block;">
               <base-input label="Insert MD5"
                    v-model="choosenMD5">
               </base-input>
              <base-button type="primary" @click="goAnalyzeMD5" >Analyze!</base-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>  
</div>
</template>
<script>
import { api } from '@/mixins/apiMixin';
import NotificationTemplate from './Notifications/NotificationTemplate';

export default {
  mixins: [api],  
  data(){
    return {
      choosenFile: '',
      choosenMD5: '',
      analizeReturn: '',
    }
  },         
  watch: {
    analizeReturn: function (val) {
      if (val.status == 'SUCCESS')
      {
        this.$notify({
          component: NotificationTemplate,
          icon: "tim-icons icon-check-2",
          horizontalAlign: 'center',
          verticalAlign: 'top',
          type: 'success',
          message: val.message,
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
          message: val.message,
          timeout: 5000
        });
      }
    },
  },     
  methods: {
    chooseFile(){
      this.$refs.chooseFile.click();
    },
    handleFileUpload(){
      [this.choosenFile] = this.$refs.chooseFile.files;
    },
    goAnalyzeFile(){
      //none
    },
    async goAnalyzeMD5(){
      this.analizeReturn = '';
      if (this.choosenMD5)
      {
        let regex = new RegExp("^[a-f0-9]{32}$");
        if (regex.test(this.choosenMD5))
        {
          await this.analizeMD5(this.choosenMD5);
          this.analizeReturn = this.tempResult;
        }
        else
        {
        this.$notify({
          component: NotificationTemplate,
          icon: "tim-icons icon-alert-circle-exc",
          horizontalAlign: 'center',
          verticalAlign: 'top',
          type: 'warning',
          message: 'This is not a valid MD5',
          timeout: 5000
        });          
        }
      }
      else
      {
        this.$notify({
          component: NotificationTemplate,
          icon: "tim-icons icon-alert-circle-exc",
          horizontalAlign: 'center',
          verticalAlign: 'top',
          type: 'warning',
          message: 'You must fill a MD5 of an Aptoide APK',
          timeout: 5000
        });
      }
    }      
  }
}
</script>
<style>
</style>
