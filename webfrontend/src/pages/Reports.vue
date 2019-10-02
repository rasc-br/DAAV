<template>
    <div class="row">
      <div class="col-12">
        <card :title="resultsTable.title">
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
import { api } from '@/mixins/apiMixin';

export default {
  mixins: [api],  
  components: {
    BaseTable
  },
  data() {
    return {
      resultsTable: {
        title: "APKs Scan Results",
        columns: ["Apk Full Name", "MD5", "Tool", "Created at", "Result"],
        data: []
      },
    };
  },
  methods: {

  },
  mounted() {
    // Send data to Table
    let self = this;
    this.getResultsList().then(()=>{
        if (self.tempResult && self.tempResult.allResults && self.tempResult.allResults.length > 0)
        {
          self.tempResult.allResults.forEach((row, index) => {
          // Consider send Apk Name in object trought database.py
          row.apk_name = row.apk_name.replace('download/','').substring(0,26);
            let item = {
              id: index,
              'apk full name': row.apk_name,
              md5: row.md5,
              tool: row.scantool,
              'created at': row.created_at,
              result:'Details',
              details: row.result_b64
          }
          this.resultsTable.data.push(item)
        });
      }
    })
  },
};
</script>
<style>
</style>
