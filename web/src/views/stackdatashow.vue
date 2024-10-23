<template>
    <div class="stock-data-display">
        <el-card class="stock-info">
            <div class="stock-header">
                <h2>国华网安 (000004)</h2>
                <span class="industry">所属行业：软件开发</span>
            </div>
            <div class="stock-price">
                <span class="current-price">22.88</span>
                <span class="price-change negative">-0.54 (-2.31%)</span>
            </div>
        </el-card>

        <el-card class="chart-container">
            <div ref="priceChart" style="height: 300px;"></div>
            <div ref="volumeChart" style="height: 100px;"></div>
        </el-card>

        <el-row :gutter="20">
            <el-col :span="12">
                <el-card class="order-book">
                    <h3>买卖盘口</h3>
                    <el-table :data="orderBookData" :show-header="false" size="small">
                        <el-table-column prop="type" width="50" />
                        <el-table-column prop="price" width="80" />
                        <el-table-column prop="volume" />
                    </el-table>
                </el-card>
            </el-col>
            <el-col :span="12">
                <el-card class="recent-trades">
                    <h3>最近成交</h3>
                    <el-table :data="recentTradesData" size="small">
                        <el-table-column prop="time" label="时间" width="100" />
                        <el-table-column prop="price" label="成交价" width="80" />
                        <el-table-column prop="volume" label="成交量" />
                        <el-table-column prop="type" label="性质" width="80" />
                    </el-table>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const priceChart = ref(null)
const volumeChart = ref(null)

const orderBookData = ref([
    { type: '卖五', price: '22.93', volume: '98' },
    { type: '卖四', price: '22.92', volume: '53' },
    { type: '卖三', price: '22.91', volume: '17' },
    { type: '卖二', price: '22.90', volume: '374' },
    { type: '卖一', price: '22.89', volume: '250' },
    { type: '买一', price: '22.88', volume: '1989' },
    { type: '买二', price: '22.87', volume: '300' },
    { type: '买三', price: '22.86', volume: '282' },
    { type: '买四', price: '22.85', volume: '1021' },
    { type: '买五', price: '22.84', volume: '92' },
])

const recentTradesData = ref([
    { time: '15:00', price: '22.88', volume: '3080', type: '卖出' },
    { time: '14:57', price: '22.88', volume: '9', type: '卖出' },
    { time: '14:56', price: '22.88', volume: '216', type: '买入' },
    { time: '14:56', price: '22.87', volume: '40', type: '卖出' },
    { time: '14:56', price: '22.88', volume: '190', type: '买入' },
    { time: '14:56', price: '22.87', volume: '122', type: '买入' },
])

onMounted(() => {
    const priceChartInstance = echarts.init(priceChart.value)
    const volumeChartInstance = echarts.init(volumeChart.value)

    // Sample data for the charts
    const times = ['09:30', '10:30', '11:30', '13:00', '14:00', '15:00']
    const prices = [22.63, 24.21, 23.42, 23.42, 22.63, 22.88]
    const volumes = [1000, 2000, 1500, 1800, 2200, 3080]

    priceChartInstance.setOption({
        title: { text: '国华网安历史上榜数据' },
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: times },
        yAxis: { type: 'value' },
        series: [{
            data: prices,
            type: 'line',
            smooth: true
        }]
    })

    volumeChartInstance.setOption({
        xAxis: { type: 'category', data: times, show: false },
        yAxis: { type: 'value' },
        series: [{
            data: volumes,
            type: 'bar'
        }]
    })
})
</script>

<style scoped>
.stock-data-display {
    font-family: Arial, sans-serif;
}

.stock-info {
    margin-bottom: 20px;
}

.stock-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.industry {
    font-size: 14px;
    color: #666;
}

.stock-price {
    margin-top: 10px;
}

.current-price {
    font-size: 24px;
    font-weight: bold;
    margin-right: 10px;
}

.price-change {
    font-size: 18px;
}

.price-change.negative {
    color: green;
}

.price-change.positive {
    color: red;
}

.chart-container {
    margin-bottom: 20px;
}

.order-book,
.recent-trades {
    height: 100%;
}

h3 {
    margin-bottom: 10px;
}
</style>