<template>
  <table class="table tablesorter" :class="tableClass">
    <thead :class="theadClasses">
    <tr>
      <slot name="columns">
        <th v-for="column in columns" :key="column">{{column}}</th>
      </slot>
    </tr>
    </thead>
    <tbody :class="tbodyClasses">
    <tr v-for="(item, index) in data" :key="index">
      <slot :row="item">
        <td v-for="(column, index) in columns"
            :key="index">
          <span v-if="hasValue(item, column) && item[column.toLowerCase()] != 'Details'">
             {{itemValue(item, column)}}
          </span>
          <base-button v-else link type="primary">
            <router-link :to="{ name: 'result', params: { detailed_results: item.details } }">{{item[column.toLowerCase()]}}</router-link>
          </base-button>
          <!-- <base-button v-else link type="primary"
            @click="sendTo(item.details)">
            {{item[column.toLowerCase()]}}
          </base-button> -->
        </td>
      </slot>
    </tr>
    </tbody>
  </table>
</template>
<script>
  export default {
    name: 'base-table',
    props: {
      columns: {
        type: Array,
        default: () => [],
        description: "Table columns"
      },
      data: {
        type: Array,
        default: () => [],
        description: "Table data"
      },
      type: {
        type: String, // striped | hover
        default: "",
        description: "Whether table is striped or hover type"
      },
      theadClasses: {
        type: String,
        default: '',
        description: "<thead> css classes"
      },
      tbodyClasses: {
        type: String,
        default: '',
        description: "<tbody> css classes"
      }
    },
    computed: {
      tableClass() {
        return this.type && `table-${this.type}`;
      }
    },
    methods: {
      hasValue(item, column) {
        return item[column.toLowerCase()] !== "undefined";
      },
      itemValue(item, column) {
        return item[column.toLowerCase()];
      },
      // sendTo(details) {
      //   // this.detailed_results = details;
      //   window.location.href = `${window.location.origin}/#/main/result`;
      // },
    }
  };
</script>
<style>
</style>
