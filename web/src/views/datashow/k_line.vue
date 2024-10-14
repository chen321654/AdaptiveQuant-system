<template>
    <div ref="chartContainer" style="width: 100%; height: 400px;"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';

const chartContainer = ref(null);
let chart = null;

const props = defineProps({
    data: {
        type: Array,
        required: true
    }
});

const initChart = () => {
    if (chartContainer.value) {
        chart = echarts.init(chartContainer.value);
        const option = {
            title: {
                text: '股票 K 线图'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross'
                }
            },
            xAxis: {
                type: 'category',
                data: props.data.map(item => item.date),
                scale: true,
                boundaryGap: false,
                axisLine: { onZero: false },
                splitLine: { show: false },
                min: 'dataMin',
                max: 'dataMax'
            },
            yAxis: {
                scale: true,
                splitArea: {
                    show: true
                }
            },
            dataZoom: [
                {
                    type: 'inside',
                    start: 50,
                    end: 100
                },
                {
                    show: true,
                    type: 'slider',
                    top: '90%',
                    start: 50,
                    end: 100
                }
            ],
            series: [
                {
                    name: 'K线',
                    type: 'candlestick',
                    data: props.data.map(item => [item.open, item.close, item.low, item.high]),
                    itemStyle: {
                        color: '#ef232a',
                        color0: '#14b143',
                        borderColor: '#ef232a',
                        borderColor0: '#14b143'
                    }
                }
            ]
        };

        chart.setOption(option);
    }
};

onMounted(() => {
    initChart();
    window.addEventListener('resize', chart.resize);
});

onUnmounted(() => {
    if (chart) {
        chart.dispose();
        window.removeEventListener('resize', chart.resize);
    }
});
</script>