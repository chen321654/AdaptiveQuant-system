<template>
    <el-row :gutter="20">
        <el-col :span="12">
            <el-card class="index-card">
                <template #header>
                    <div class="card-header">
                        <span>上证指数</span>
                    </div>
                </template>
                <k_line :stock-code="shStockCode"></k_line>
            </el-card>
        </el-col>
        <el-col :span="12">
            <el-card class="index-card">
                <template #header>
                    <div class="card-header">
                        <span>深证指数</span>
                    </div>
                </template>
                <k_line :stock-code="szStockCode"></k_line>
            </el-card>
        </el-col>
    </el-row>

    <el-row :gutter="20">
        <el-col :span="12">
            <el-card class="index-card">
                <template #header>
                    <div class="card-header">
                        <span>北证50</span>
                    </div>
                </template>
                <k_line :stock-code="bzStockCode"></k_line>
            </el-card>
        </el-col>
        <el-col :span="12">
            <el-card class="index-card">
                <template #header>
                    <div class="card-header">
                        <span>创业板指</span>
                    </div>
                </template>
                <k_line :stock-code="kcStockCode"></k_line>
            </el-card>
        </el-col>
    </el-row>
</template>

<script setup>
import { ref } from 'vue'
import k_line from '../datashow/k_line.vue'
const shStockCode = ref("000001.SH")
const szStockCode = ref("399001.SZ")
const bzStockCode = ref("000021.SH")
const kcStockCode = ref("399021.SZ")
</script>

<style scoped>
.stock-indices-dashboard {
    padding: 20px;
}

.index-card {
    height: 100%;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>