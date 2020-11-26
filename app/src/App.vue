<template>
  <b-container><br>
  <h2 align="center">SOCKS5 Proxy list</h2>
  <div class="overflow-auto">
    <b-table
      id="proxy-list"
      :items="items"
      :per-page="perPage"
      :current-page="currentPage"
      striped hover small
      @row-clicked="onRowClicked"
      responsive
    ></b-table>

    <div style="float:left;">
    <b-form-checkbox id="checkbox-1" v-model="status" name="checkbox-1">
      Copy selected to clipboard
    </b-form-checkbox>
    </div>
    
    <div style="float:right;">
    <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      size="sm"
      align="right"
      :per-page="perPage"
      first-number
      last-number
      aria-controls="proxy-list"
    ></b-pagination>
    </div>

  </div>
  </b-container>
</template>

<script>
  export default {
    data() {
      return {
        perPage: 20,
        currentPage: 1,
        items: [],
        status: 'true'
      }
    },
    computed: {
      rows() {
        return this.items.length
      }
    },
    created(){  
		fetch("http://localhost:5000/api/proxies", {
			"method": "GET",
			"headers": {
			}
		})
		.then(response => { 
			if(response.ok){
				return response.json()
			} else{
				console.log(response.status + " " + response.statusText);
			}
		})
		.then(response => {
			this.items = response;
		})
		.catch(err => {
			console.log(err);
		});
    },
    methods: {
    onRowClicked (item) {
      if(this.status){
      //alert("copied to clipboard");
      var dummy = document.createElement("input");
      document.body.appendChild(dummy);
      dummy.setAttribute("id", "dummy");
      document.getElementById("dummy").value=item.ip+":"+item.port;
      dummy.select();
      document.execCommand("copy");
      document.body.removeChild(dummy);  
      }
    }
}
  }
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
 
  h2{font-family: 'Press Start 2P';}
</style>