<template>
    <div class="row">
      <div class="col-12">
        <card :title="title">
          <div class="table-responsive">
            <base-table :data="resultsTable.data"
                        :columns="resultsTable.columns"
                        thead-classes="text-primary">
            </base-table>
          </div>
        </card>
      </div>
    </div>
</template>
<script>
import { BaseTable } from "@/components";

export default {
  components: {
    BaseTable    
  },
  data() {
    return {
      title: 'Detailed Results',
      detailed_results: 'none',
      resultsTable: {
        columns: ["Information","Data"],
        data: []
      },   
    };
  },
  methods: {
    extractData(objectToExtract) {
      for (const [key, value] of Object.entries(objectToExtract)) {
        if (typeof(value)!=='object')
        {
          let item = {
            information: key,
            data: value,
          }
          this.resultsTable.data.push(item);
        }
        else
        {
          this.extractData(value);
        }  
      }
    },
  },
  mounted() {
    this.detailed_results = this.$route.params.detailed_results;

    this.extractData(this.detailed_results);
    // for (const [key, value] of Object.entries(this.detailed_results)) {
    //   if (typeof(value)!=='object')
    //   {
    //     let item = {
    //       information: key,
    //       data: value,
    //     }
    //     this.resultsTable.data.push(item);
    //   }
    //   else
    //   {
        
    //   }  
    // }

  },
};
</script>
<style>
</style>
