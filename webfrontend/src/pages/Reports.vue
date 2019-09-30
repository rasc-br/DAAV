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

export default {
  components: {
    BaseTable
  },
  data() {
    return {
      resultsTable: {
        title: "APKs Scan Results",
        columns: ["ID", "Apk Full Name", "MD5", "Tool", "Created at", "Result"],
        data: [
                {
                  id: 1,
                  md5: "Dakota Rice",
                  'apk full name': "$36.738",
                  country: "Niger",
                  city: "Oud-Turnhout",
                }
        ]
      },
    };
  },
  methods: {

  },
  mounted() {
    
  },
};
</script>
<style>
</style>
