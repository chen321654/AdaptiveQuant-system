<template>
    <el-container class="layout-container">
        <el-header>
            <div class="header-content">
                <div class="logo-title">
                    <h1>个人中心</h1>
                </div>
                <el-button type="text" @click="logout">退出</el-button>
            </div>
        </el-header>
        <el-container>
            <el-aside width="250px">
                <el-card class="user-info">
                    <el-avatar :size="100" src="/placeholder.svg?height=100&width=100"></el-avatar>
                    <p>mx_**181v6e</p>
                </el-card>
                <el-menu default-active="1" class="sidebar-menu">
                    <el-menu-item index="1">
                        <el-icon>
                            <House />
                        </el-icon>
                        <span>我的主页</span>
                    </el-menu-item>
                    <el-menu-item index="2">
                        <el-icon>
                            <Star />
                        </el-icon>
                        <span>增值服务</span>
                    </el-menu-item>
                    <el-menu-item index="3">
                        <el-icon>
                            <Service />
                        </el-icon>
                        <span>我的服务</span>
                    </el-menu-item>
                    <el-menu-item index="4">
                        <el-icon>
                            <Lock />
                        </el-icon>
                        <span>修改密码</span>
                    </el-menu-item>
                    <el-menu-item index="5">
                        <el-icon>
                            <DataLine />
                        </el-icon>
                        <span>数据中心</span>
                    </el-menu-item>
                    <el-menu-item index="6">
                        <el-icon>
                            <TrendCharts />
                        </el-icon>
                        <span>行情中心</span>
                    </el-menu-item>
                </el-menu>
            </el-aside>
            <el-main>
                <el-row :gutter="20" class="mb-4">
                    <el-col :span="8" v-for="index in indices" :key="index.name">
                        <el-card>
                            <template #header>
                                <div class="card-header">
                                    <span>{{ index.name }}</span>
                                </div>
                            </template>
                            <div class="index-value">{{ index.value.toFixed(2) }}</div>
                            <div :class="['index-change', index.change >= 0 ? 'positive' : 'negative']">
                                {{ index.change > 0 ? '+' : '' }}{{ index.change.toFixed(2) }} ({{
                                    index.changePercent.toFixed(2) }}%)
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
                <el-card>
                    <template #header>
                        <div class="card-header">
                            <span>我的自选股</span>
                            <div>
                                <el-input v-model="searchStock" placeholder="添加自选股" class="w-auto mr-2">
                                    <template #prefix>
                                        <el-icon>
                                            <Search />
                                        </el-icon>
                                    </template>
                                </el-input>
                                <el-button type="primary" @click="fetchData">
                                    <el-icon>
                                        <Refresh />
                                    </el-icon>
                                </el-button>
                            </div>
                        </div>
                    </template>
                    <el-table :data="stocks" style="width: 100%" v-loading="isLoading">
                        <el-table-column prop="name" label="股票" width="180">
                            <template #default="scope">
                                <div>{{ scope.row.name }}</div>
                                <div class="text-gray-500 text-sm">{{ scope.row.code }}</div>
                            </template>
                        </el-table-column>
                        <el-table-column prop="price" label="当前价" width="100"></el-table-column>
                        <el-table-column prop="change" label="涨跌幅" width="120">
                            <template #default="scope">
                                <span :class="scope.row.change >= 0 ? 'text-red-500' : 'text-green-500'">
                                    {{ scope.row.change > 0 ? '+' : '' }}{{ scope.row.change.toFixed(2) }}
                                    ({{ scope.row.changePercent.toFixed(2) }}%)
                                </span>
                            </template>
                        </el-table-column>
                        <el-table-column prop="volume" label="成交量(手)" width="120"></el-table-column>
                        <el-table-column prop="amount" label="成交额"></el-table-column>
                        <el-table-column prop="marketValue" label="市值"></el-table-column>
                        <el-table-column prop="turnoverRate" label="换手率"></el-table-column>
                        <el-table-column prop="peRatio" label="市盈率"></el-table-column>
                        <el-table-column label="操作" width="100">
                            <template #default="scope">
                                <el-button type="danger" @click="removeStock(scope.row.code)" :icon="Delete"
                                    circle></el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-card>
            </el-main>
        </el-container>
    </el-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { House, Star, Service, Lock, DataLine, TrendCharts, Search, Refresh, Delete } from '@element-plus/icons-vue'

const indices = ref([])
const stocks = ref([])
const isLoading = ref(true)
const searchStock = ref('')

const fetchData = async () => {
    isLoading.value = true
    try {
        const [stocksResponse, indicesResponse] = await Promise.all([
            fetch('/api/stocks'),
            fetch('/api/indices')
        ])

        if (!stocksResponse.ok || !indicesResponse.ok) {
            throw new Error('Failed to fetch data')
        }

        const stocksData = await stocksResponse.json()
        const indicesData = await indicesResponse.json()

        stocks.value = stocksData
        indices.value = indicesData
    } catch (error) {
        console.error('Error fetching data:', error)
        ElMessage.error('Failed to load data. Please try again later.')
    } finally {
        isLoading.value = false
    }
}

const removeStock = async (code) => {
    try {
        const response = await fetch(`/api/stocks/${code}`, { method: 'DELETE' })
        if (!response.ok) {
            throw new Error('Failed to remove stock')
        }
        stocks.value = stocks.value.filter(stock => stock.code !== code)
        ElMessage.success('Stock removed successfully')
    } catch (error) {
        console.error('Error removing stock:', error)
        ElMessage.error('Failed to remove stock. Please try again.')
    }
}

const logout = () => {
    // Implement logout logic here
    ElMessage.success('Logged out successfully')
}

onMounted(() => {
    fetchData()
})
</script>

<style scoped>
.layout-container {
    height: 100vh;
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo-title {
    display: flex;
    align-items: center;
}

.logo {
    width: 40px;
    height: 40px;
    margin-right: 10px;
}

.user-info {
    text-align: center;
    margin-bottom: 20px;
}

.sidebar-menu {
    border-right: none;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.index-value {
    font-size: 24px;
    font-weight: bold;
}

.index-change {
    font-size: 14px;
}

.index-change.positive {
    color: #F56C6C;
}

.index-change.negative {
    color: #67C23A;
}

.mb-4 {
    margin-bottom: 16px;
}

.w-auto {
    width: auto;
}

.mr-2 {
    margin-right: 8px;
}

.text-gray-500 {
    color: #909399;
}

.text-sm {
    font-size: 14px;
}

.text-red-500 {
    color: #F56C6C;
}

.text-green-500 {
    color: #67C23A;
}
</style>