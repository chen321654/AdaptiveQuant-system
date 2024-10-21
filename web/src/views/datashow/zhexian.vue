<template>
    <div id="app">
        <h1>WebSocket Example</h1>
        <div>
            <input v-model="message" placeholder="Enter a message" />
            <button @click="sendMessage">Send</button>
        </div>
        <div>
            <h2>Messages:</h2>
            <ul>
                <li v-for="(msg, index) in messages" :key="index">{{ msg }}</li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            ws: null, // WebSocket 实例
            message: '', // 当前要发送的消息
            messages: [] // 接收到的消息列表
        };
    },
    mounted() {
        this.connectWebSocket();
    },
    methods: {
        // 连接 WebSocket
        connectWebSocket() {
            this.ws = new WebSocket('wss://quote.tradeswitcher.com/quote-stock-b-ws-api?token=bcc2bebbab8719c91212d304fd9146cd-c-app');

            this.ws.onopen = () => {
                console.log('WebSocket connection opened');
            };

            this.ws.onmessage = (event) => {
                console.log('Message from server:', event.data);
                this.messages.push(event.data);
            };

            this.ws.onclose = () => {
                console.log('WebSocket connection closed');
                this.reconnectWebSocket();
            };
        },
        // 重连机制
        reconnectWebSocket() {
            setTimeout(() => {
                console.log('Reconnecting WebSocket...');
                this.connectWebSocket();
            }, 3000); // 3秒后重连
        },
        // 发送消息
        sendMessage() {
            if (this.message.trim() !== '') {
                this.ws.send(this.message);
                this.message = ''; // 清空输入框
            }
        }
    },
    beforeDestroy() {
        // 页面销毁时关闭 WebSocket 连接
        if (this.ws) {
            this.ws.close();
        }
    }
};
</script>

<style scoped>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    text-align: center;
    margin-top: 60px;
}
</style>