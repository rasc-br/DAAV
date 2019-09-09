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
              <!-- <input type="file" id="chooseFile" ref="chooseFile" v-on:change="handleFileUpload()"/> -->
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

export default {
  mixins: [api],  
  data(){
    return {
      choosenFile: '',
      choosenMD5: '',
    }
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
    goAnalyzeMD5(){
      //none
    }      
  }
}
</script>
<style>
</style>
