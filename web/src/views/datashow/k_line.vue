<template>
    <div class="chart-container">
        <div class="time-options">
            <span v-for="(item, index) in klineData" :key="index" @click="tabTime(item)"
                :class="{ active: item.time === active }">
                {{ item.time }}
            </span>
        </div>
        <div :id="chartId" class="chart-box"></div>
    </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { init, registerStyles } from "klinecharts";
import axios from "axios";

const props = defineProps({
    stockCode: {
        type: String,
        required: true
    }
});

const chartId = computed(() => `chart_${props.stockCode}`);
const active = ref("");
let chart;

const red = '#F92855'
const green = '#2DC08E'
const alphaRed = 'rgba(249, 40, 85, .7)'
const alphaGreen = 'rgba(45, 192, 142, .7)'

registerStyles('red_rise_green_fall', {
    candle: {
        bar: {
            upColor: red,
            downColor: green,
            upBorderColor: red,
            downBorderColor: green,
            upWickColor: red,
            downWickColor: green,
        },
        priceMark: {
            last: {
                upColor: red,
                downColor: green,
            }
        }
    },
    indicator: {
        ohlc: {
            upColor: alphaRed,
            downColor: alphaGreen
        },
        bars: [{
            style: 'fill',
            borderStyle: 'solid',
            borderSize: 1,
            borderDashedValue: [2, 2],
            upColor: alphaRed,
            downColor: alphaGreen,
            noChangeColor: '#888888'
        }],
        circles: [{
            style: 'fill',
            borderStyle: 'solid',
            borderSize: 1,
            borderDashedValue: [2, 2],
            upColor: alphaRed,
            downColor: alphaGreen,
            noChangeColor: '#888888'
        }]
    }
})

const klineData = ref([
    { time: "分时", key: 'area', kline_type: 1, main: '' },
    { time: "日k", key: 'candle_solid', kline_type: 2, main: 'MA' },
    { time: "周k", key: 'candle_solid', kline_type: 3, main: 'MA' },
    { time: "月k", key: 'candle_solid', kline_type: 4, main: 'MA' },
    { time: "五日", key: 'candle_solid', kline_type: 5, main: 'MA' }
]);

// const apiEndpoint = 'http://127.0.0.1:8000/data/k_line';
// const fetchData = async (kline_type) => {
//     try {
//         const response = await axios.get(apiEndpoint, {
//             params: {
//                 code: "857.HK", // You might want to make this dynamic
//                 kline_type: kline_type,
//                 kline_timestamp_end: 0,
//                 query_kline_num: 100,
//                 adjust_type: 0
//             }
//         });

//         if (response.data.ret === 200) {
//             return response.data.data.kline_list.map(item => ({
//                 timestamp: item.timestamp,
//                 open: parseFloat(item.open),
//                 close: parseFloat(item.close),
//                 high: parseFloat(item.high),
//                 low: parseFloat(item.low),
//                 volume: parseFloat(item.volume),
//                 turnover: parseFloat(item.turnover)
//             }));
//         } else {
//             console.error("Unexpected API response structure:", response.data);
//             return [];
//         }
//     } catch (error) {
//         console.error("Error fetching data:", error);
//         return [];
//     }
// };

//模拟数据
function genData(timestamp = new Date().getTime(), length = 800) {
    let basePrice = 5000
    timestamp = Math.floor(timestamp / 1000 / 60) * 60 * 1000 - length * 60 * 1000
    const dataList = []
    for (let i = 0; i < length; i++) {
        const prices = []
        for (let j = 0; j < 4; j++) {
            prices.push(basePrice + Math.random() * 60 - 30)
        }
        prices.sort()
        const open = +(prices[Math.round(Math.random() * 3)].toFixed(2))
        const high = +(prices[3].toFixed(2))
        const low = +(prices[0].toFixed(2))
        const close = +(prices[Math.round(Math.random() * 3)].toFixed(2))
        const volume = Math.round(Math.random() * 100) + 10
        const turnover = (open + high + low + close) / 4 * volume
        dataList.push({ timestamp, open, high, low, close, volume, turnover })

        basePrice = close
        timestamp += 60 * 1000
    }
    return dataList
}

function setType(type) {
    chart.setStyles({
        candle: { type }
    })
}

const tabTime = async (item) => {
    setType(item.key);
    active.value = item.time;
    // const data = await fetchData(item.kline_type);
    // chart.applyNewData(data);
    chart.applyNewData(genData())

    chart.createIndicator(item.main, true, { id: 'candle_pane' })

    chart.removeIndicator(item.main)


};

onMounted(async () => {
    chart = init(chartId.value);
    setType('area');
    chart.setStyles('red_rise_green_fall');
    //const initialData = await fetchData(klineData.value[0].kline_type);
    //chart.applyNewData(initialData);
    chart.applyNewData(genData())
    chart.setMaxOffsetLeftDistance(0);
    chart.setMaxOffsetRightDistance(0);
    active.value = klineData.value[0].time;

});
</script>

<style lang="scss" scoped>
.chart-container {
    width: 100%;
    margin: 0 auto;

    .time-options {
        display: flex;
        justify-content: space-between;
        margin-bottom: 15px;
        background-color: #f5f5f5;
        border-radius: 20px;
        padding: 5px;

        span {
            cursor: pointer;
            padding: 8px 16px;
            font-size: 14px;
            border-radius: 15px;
            transition: all 0.3s ease;

            &:hover {
                background-color: #e0e0e0;
            }

            &.active {
                color: #ffffff;
                background-color: #1a89ee;
            }
        }
    }

    .chart-box {
        width: 100%;
        height: 300px;
    }
}
</style>