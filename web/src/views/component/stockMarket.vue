<template>
    <div class="stock-market-dashboard">
        <div class="stock-category-nav">
            <ul>
                <li v-for="category in categories" :key="category.value"
                    :class="{ active: activeCategory === category.value }" @click="setActiveCategory(category.value)">
                    {{ category.label }}
                </li>
            </ul>
        </div>
        <StockMarketTable :category="activeCategory" />
    </div>
</template>

<script setup>
import { ref } from 'vue'
import StockMarketTable from '../datashow/stockdata.vue'

const categories = [
    { label: '全部股票', value: 'all' },
    { label: '上证A股', value: 'shanghai' },
    { label: '深证A股', value: 'shenzhen' },
    { label: '京证A股', value: 'beijing' },
    { label: '创业板', value: 'chinext' },
    { label: '科创板', value: 'star' }
]

const activeCategory = ref('all')

const setActiveCategory = (category) => {
    activeCategory.value = category
}
</script>

<style scoped>
.stock-market-dashboard {
    font-family: Arial, sans-serif;
}

.stock-category-nav ul {
    display: flex;
    list-style-type: none;
    padding: 0;
    margin: 0 0 20px 0;
    border-bottom: 1px solid #e0e0e0;
}

.stock-category-nav li {
    padding: 10px 20px;
    cursor: pointer;
    transition: color 0.3s ease;
}

.stock-category-nav li:hover {
    color: #ff4d4f;
}

.stock-category-nav li.active {
    color: #ff4d4f;
    border-bottom: 2px solid #ff4d4f;
}
</style>