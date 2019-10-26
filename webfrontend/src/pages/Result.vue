<template>
    <div class="row">
      <div class="col-12">
        <card :title="title">
          <div class="table-responsive" v-if="!categorized">
            <base-table :data="resultsTable.data"
                        :columns="resultsTable.columns"
                        thead-classes="text-primary">
            </base-table>
          </div>
          <div v-else>
            <!-- TODO v-for of M1,M2,M3... -->
            <card :title="`OWASP M1 - (Total: ${detailed_results['M1'].length})`">
              <div class="table-responsive">
                <base-table :data="resultsCategorizedTable.dataM1"
                            :columns="resultsCategorizedTable.columns"
                            thead-classes="text-primary">
                </base-table>
              </div>
            </card>
            <card :title="`OWASP M2 - (Total: ${detailed_results['M2'].length})`">
              <div class="table-responsive">
                <base-table :data="resultsCategorizedTable.dataM2"
                            :columns="resultsCategorizedTable.columns"
                            thead-classes="text-primary">
                </base-table>
              </div>
            </card>  
            <card :title="`OWASP M3 - (Total: ${detailed_results['M3'].length})`">
              <div class="table-responsive">
                <base-table :data="resultsCategorizedTable.dataM3"
                            :columns="resultsCategorizedTable.columns"
                            thead-classes="text-primary">
                </base-table>
              </div>
            </card>
            <card :title="`OWASP M4 - (Total: ${detailed_results['M4'].length})`">
              <div class="table-responsive">
                <base-table :data="resultsCategorizedTable.dataM4"
                            :columns="resultsCategorizedTable.columns"
                            thead-classes="text-primary">
                </base-table>
              </div>
            </card>
            <card :title="`OWASP M5 - (Total: ${detailed_results['M5'].length})`">
              <div class="table-responsive">
                <base-table :data="resultsCategorizedTable.dataM5"
                            :columns="resultsCategorizedTable.columns"
                            thead-classes="text-primary">
                </base-table>
              </div>
            </card>
            <card :title="`OWASP M6 - (Total: ${detailed_results['M6'].length})`">
              <div class="table-responsive">
                <base-table :data="resultsCategorizedTable.dataM6"
                            :columns="resultsCategorizedTable.columns"
                            thead-classes="text-primary">
                </base-table>
              </div>
            </card>
            <card :title="`OWASP M7 - (Total: ${detailed_results['M7'].length})`">
              <div class="table-responsive">
                <base-table :data="resultsCategorizedTable.dataM7"
                            :columns="resultsCategorizedTable.columns"
                            thead-classes="text-primary">
                </base-table>
              </div>
            </card>
            <card :title="`OWASP M8 - (Total: ${detailed_results['M8'].length})`">
              <div class="table-responsive">
                <base-table :data="resultsCategorizedTable.dataM8"
                            :columns="resultsCategorizedTable.columns"
                            thead-classes="text-primary">
                </base-table>
              </div>
            </card>
            <card :title="`OWASP M9 - (Total: ${detailed_results['M9'].length})`">
              <div class="table-responsive">
                <base-table :data="resultsCategorizedTable.dataM9"
                            :columns="resultsCategorizedTable.columns"
                            thead-classes="text-primary">
                </base-table>
              </div>
            </card>
            <card :title="`OWASP M10 - (Total: ${detailed_results['M10'].length})`">
              <div class="table-responsive">
                <base-table :data="resultsCategorizedTable.dataM10"
                            :columns="resultsCategorizedTable.columns"
                            thead-classes="text-primary">
                </base-table>
              </div>
            </card>                                                                                                          
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
      categorized: false,
      title: 'Detailed Results',
      detailed_results: 'none',
      resultsTable: {
        columns: ["Information","Data"],
        data: []
      },  
      resultsCategorizedTable: {
        columns: ["Vulnerability","Detected By","Details","Feedback URL","Feedback Video","Feedback Book"],
        dataM1: [], dataM2: [], dataM3: [], dataM4: [], dataM5: [], dataM6: [], dataM7: [], dataM8: [], dataM9: [], dataM10: [],
      },       
    };
  },
  methods: {
    extractData(objectToExtract) {
      if (!objectToExtract['M1'])
      {
        this.categorized=false;
        // Not Categorized - Results from a plugin
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
      }
      else
      {
        this.categorized=true;
        // Categorized Results 
        // TODO: Convert into one FOR since is the same structure
        for (const [key, value] of Object.entries(objectToExtract['M1'])) {
            let item = {
              vulnerability: value.name,
              'detected by': value.detectedby,
              details: value.details,
              'feedback url': value.feedback[0] && value.feedback[0]["url"] && value.feedback[0]["url"][0] ? value.feedback[0]["url"][0] : '',
              'feedback video': value.feedback[1] && value.feedback[1]["video"] && value.feedback[1]["video"][0] ? value.feedback[1]["video"][0] : '',
              'feedback book': value.feedback[2] && value.feedback[2]["book"] && value.feedback[2]["book"][0] ? value.feedback[2]["book"][0] : '',
            }
            this.resultsCategorizedTable.dataM1.push(item);
        }
        for (const [key, value] of Object.entries(objectToExtract['M2'])) {
            let item = {
              vulnerability: value.name,
              'detected by': value.detectedby,
              details: value.details,
              'feedback url': value.feedback[0] && value.feedback[0]["url"] && value.feedback[0]["url"][0] ? value.feedback[0]["url"][0] : '',
              'feedback video': value.feedback[1] && value.feedback[1]["video"] && value.feedback[1]["video"][0] ? value.feedback[1]["video"][0] : '',
              'feedback book': value.feedback[2] && value.feedback[2]["book"] && value.feedback[2]["book"][0] ? value.feedback[2]["book"][0] : '',
            }
            this.resultsCategorizedTable.dataM2.push(item);
        }
        for (const [key, value] of Object.entries(objectToExtract['M3'])) {
            let item = {
              vulnerability: value.name,
              'detected by': value.detectedby,
              details: value.details,
              'feedback url': value.feedback[0] && value.feedback[0]["url"] && value.feedback[0]["url"][0] ? value.feedback[0]["url"][0] : '',
              'feedback video': value.feedback[1] && value.feedback[1]["video"] && value.feedback[1]["video"][0] ? value.feedback[1]["video"][0] : '',
              'feedback book': value.feedback[2] && value.feedback[2]["book"] && value.feedback[2]["book"][0] ? value.feedback[2]["book"][0] : '',
            }
            this.resultsCategorizedTable.dataM3.push(item);
        }
        for (const [key, value] of Object.entries(objectToExtract['M4'])) {
            let item = {
              vulnerability: value.name,
              'detected by': value.detectedby,
              details: value.details,
              'feedback url': value.feedback[0] && value.feedback[0]["url"] && value.feedback[0]["url"][0] ? value.feedback[0]["url"][0] : '',
              'feedback video': value.feedback[1] && value.feedback[1]["video"] && value.feedback[1]["video"][0] ? value.feedback[1]["video"][0] : '',
              'feedback book': value.feedback[2] && value.feedback[2]["book"] && value.feedback[2]["book"][0] ? value.feedback[2]["book"][0] : '',
            }
            this.resultsCategorizedTable.dataM4.push(item);
        }
        for (const [key, value] of Object.entries(objectToExtract['M5'])) {
            let item = {
              vulnerability: value.name,
              'detected by': value.detectedby,
              details: value.details,
              'feedback url': value.feedback[0] && value.feedback[0]["url"] && value.feedback[0]["url"][0] ? value.feedback[0]["url"][0] : '',
              'feedback video': value.feedback[1] && value.feedback[1]["video"] && value.feedback[1]["video"][0] ? value.feedback[1]["video"][0] : '',
              'feedback book': value.feedback[2] && value.feedback[2]["book"] && value.feedback[2]["book"][0] ? value.feedback[2]["book"][0] : '',
            }
            this.resultsCategorizedTable.dataM5.push(item);
        }
        for (const [key, value] of Object.entries(objectToExtract['M6'])) {
            let item = {
              vulnerability: value.name,
              'detected by': value.detectedby,
              details: value.details,
              'feedback url': value.feedback[0] && value.feedback[0]["url"] && value.feedback[0]["url"][0] ? value.feedback[0]["url"][0] : '',
              'feedback video': value.feedback[1] && value.feedback[1]["video"] && value.feedback[1]["video"][0] ? value.feedback[1]["video"][0] : '',
              'feedback book': value.feedback[2] && value.feedback[2]["book"] && value.feedback[2]["book"][0] ? value.feedback[2]["book"][0] : '',
            }
            this.resultsCategorizedTable.dataM6.push(item);
        }
        for (const [key, value] of Object.entries(objectToExtract['M7'])) {
            let item = {
              vulnerability: value.name,
              'detected by': value.detectedby,
              details: value.details,
              'feedback url': value.feedback[0] && value.feedback[0]["url"] && value.feedback[0]["url"][0] ? value.feedback[0]["url"][0] : '',
              'feedback video': value.feedback[1] && value.feedback[1]["video"] && value.feedback[1]["video"][0] ? value.feedback[1]["video"][0] : '',
              'feedback book': value.feedback[2] && value.feedback[2]["book"] && value.feedback[2]["book"][0] ? value.feedback[2]["book"][0] : '',
            }
            this.resultsCategorizedTable.dataM7.push(item);
        }
        for (const [key, value] of Object.entries(objectToExtract['M8'])) {
            let item = {
              vulnerability: value.name,
              'detected by': value.detectedby,
              details: value.details,
              'feedback url': value.feedback[0] && value.feedback[0]["url"] && value.feedback[0]["url"][0] ? value.feedback[0]["url"][0] : '',
              'feedback video': value.feedback[1] && value.feedback[1]["video"] && value.feedback[1]["video"][0] ? value.feedback[1]["video"][0] : '',
              'feedback book': value.feedback[2] && value.feedback[2]["book"] && value.feedback[2]["book"][0] ? value.feedback[2]["book"][0] : '',
            }
            this.resultsCategorizedTable.dataM8.push(item);
        }
        for (const [key, value] of Object.entries(objectToExtract['M9'])) {
            let item = {
              vulnerability: value.name,
              'detected by': value.detectedby,
              details: value.details,
              'feedback url': value.feedback[0] && value.feedback[0]["url"] && value.feedback[0]["url"][0] ? value.feedback[0]["url"][0] : '',
              'feedback video': value.feedback[1] && value.feedback[1]["video"] && value.feedback[1]["video"][0] ? value.feedback[1]["video"][0] : '',
              'feedback book': value.feedback[2] && value.feedback[2]["book"] && value.feedback[2]["book"][0] ? value.feedback[2]["book"][0] : '',
            }
            this.resultsCategorizedTable.dataM9.push(item);
        }
        for (const [key, value] of Object.entries(objectToExtract['M10'])) {
            let item = {
              vulnerability: value.name,
              'detected by': value.detectedby,
              details: value.details,
              'feedback url': value.feedback[0] && value.feedback[0]["url"] && value.feedback[0]["url"][0] ? value.feedback[0]["url"][0] : '',
              'feedback video': value.feedback[1] && value.feedback[1]["video"] && value.feedback[1]["video"][0] ? value.feedback[1]["video"][0] : '',
              'feedback book': value.feedback[2] && value.feedback[2]["book"] && value.feedback[2]["book"][0] ? value.feedback[2]["book"][0] : '',
            }
            this.resultsCategorizedTable.dataM10.push(item);
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
