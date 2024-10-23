<template>
  <div class="stock-market-table">
    <el-table :data="tableData" style="width: 100%" :default-sort="{ prop: 'rank', order: 'ascending' }">
      <el-table-column prop="rank" label="序号" width="60" />
      <el-table-column prop="code" label="代码" width="80" />
      <el-table-column prop="name" label="名称" width="100" />
      <el-table-column prop="price" label="现价" width="80" sortable>
        <template #default="scope">
          <span :style="{ color: scope.row.priceChange >= 0 ? 'red' : 'green' }">{{ scope.row.price }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="changePercent" label="涨跌幅(%)" width="100" sortable>
        <template #default="scope">
          <span :style="{ color: scope.row.changePercent >= 0 ? 'red' : 'green' }">{{ scope.row.changePercent }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="priceChange" label="涨跌" width="80" sortable>
        <template #default="scope">
          <span :style="{ color: scope.row.priceChange >= 0 ? 'red' : 'green' }">{{ scope.row.priceChange }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="changeRate" label="涨速(%)" width="100" sortable />
      <el-table-column prop="turnoverRate" label="换手(%)" width="100" sortable />
      <el-table-column prop="volumeRatio" label="量比" width="80" sortable />
      <el-table-column prop="amplitude" label="振幅(%)" width="100" sortable />
      <el-table-column prop="transactionAmount" label="成交额" width="100" sortable />
      <el-table-column prop="circulatingShares" label="流通股" width="100" sortable />
      <el-table-column prop="marketCap" label="流通市值" width="100" sortable />
      <el-table-column prop="peRatio" label="市盈率" width="80" sortable />
    </el-table>
    <div class="pagination">
      <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :page-sizes="[20, 50, 100]"
        :small="small" :disabled="disabled" :background="background" layout="total, sizes, prev, pager, next, jumper"
        :total="totalItems" @size-change="handleSizeChange" @current-change="handleCurrentChange" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const tableData = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const totalItems = ref(0)
const small = ref(false)
const disabled = ref(false)
const background = ref(true)

const fetchData = async () => {
  try {
    const response = await axios.get('/data/stockdata', {
      params: {
        page: currentPage.value,
        pageSize: pageSize.value
      }
    })

    if (response.data.ref) {
      tableData.value = response.data.data.map(item => ({
        rank: item.rank,
        code: item.code,
        name: item.name,
        price: parseFloat(item.price),
        changePercent: parseFloat(item.changePercent),
        priceChange: parseFloat(item.priceChange),
        changeRate: parseFloat(item.changeRate),
        turnoverRate: parseFloat(item.turnoverRate),
        volumeRatio: parseFloat(item.volumeRatio),
        amplitude: parseFloat(item.amplitude),
        transactionAmount: item.transactionAmount,
        circulatingShares: item.circulatingShares,
        marketCap: item.marketCap,
        peRatio: parseFloat(item.peRatio)
      }))
      totalItems.value = response.data.total || 269 // Use the total from API if available, otherwise default to 269
    } else {
      ElMessage.error('Failed to fetch data: Unexpected response structure')
    }
  } catch (error) {
    console.error('Error fetching data:', error)
    ElMessage.error('Failed to fetch data. Please try again later.')
  }
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchData()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchData()
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.stock-market-table {
  margin: 20px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}
</style>