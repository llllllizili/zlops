<template>
  <div class="dashboard-container">
    <div class="dashboard-text">name: {{ name }}</div>
    <div class="dashboard-text">perms: <span v-for="perm in perms" :key="perm">{{ perm }}<br> </span></div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name',
      'perms',
      'token'
    ])
  },


  data() {
      return {
        websock: null,
      }
    },
    created() {
      this.initWebSocket();
    },
    destroyed() {
      this.websock.close() //离开路由之后断开websocket连接
    },
    methods: {
      initWebSocket(){ //初始化weosocket
        const wsuri = "ws://127.0.0.1:8000/ws/system/";
        this.websock = new WebSocket(wsuri);
        this.websock.onmessage = this.websocketonmessage;
        this.websock.onopen = this.websocketonopen;
        this.websock.onerror = this.websocketonerror;
        this.websock.onclose = this.websocketclose;
      },
      websocketonopen(){ //连接建立之后执行send方法发送数据
        let actions = {"type":"ticket","test":"12345"};
        this.websocketsend(JSON.stringify(actions));
      },
      websocketonerror(){//连接建立失败重连
        this.initWebSocket();
      },
      websocketonmessage(e){ //数据接收
        const redata = JSON.parse(e.data);
      },
      websocketsend(Data){//数据发送
        this.websock.send(Data);
      },
      websocketclose(e){  //关闭
        console.log('断开连接',e);
      },
    },
  }
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
