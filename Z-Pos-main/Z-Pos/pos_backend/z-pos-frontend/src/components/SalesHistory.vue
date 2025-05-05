<template>
  <div class="sales-history">
    <h2>Sales History</h2>

    <!--Date Filters -->
    <div class="filters">
      <label>
        From:
        <input type="date" v-model="fromDate" />
      </label>
      <label>
        To:
        <input type="date" v-model="toDate" />
      </label>
      <button class="chart-toggle" @click="showChart = !showChart">
        {{ showChart ? 'Hide Chart' : 'View Chart' }}
      </button>
    </div>

    <!--Chart -->
    <div class="chart-container" v-if="showChart">
      <sales-chart :chartData="salesChartData" />
    </div>

    <!--Summary Box -->
    <div class="summary-box">
      <p><strong>Total Sales:</strong> £{{ summary.totalSales.toFixed(2) }}</p>
      <p><strong>Total Transactions:</strong> {{ summary.totalTransactions }}</p>
      <p><strong>Average Sale:</strong> £{{ summary.averageSale.toFixed(2) }}</p>
    </div>

    <!--Sales Table -->
    <div class="sales-table-wrapper" v-if="filteredSales.length">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Date</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sale in filteredSales" :key="sale.id">
            <td>{{ sale.id }}</td>
            <td>{{ new Date(sale.created_at).toLocaleString() }}</td>
            <td>£{{ Number(sale.total).toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-else>No sales match your filter.</p>
  </div>
</template>

<script>
import axios from 'axios';
import SalesChart from '@/components/SalesChart.vue';



export default {
  name: 'SalesHistory',
  components: {
    SalesChart
  },
  data() {
    return {
      sales: [],
      fromDate: '',
      toDate: '',
      showChart: false,
      summary: {
        totalSales: 0,
        totalTransactions: 0,
        averageSale: 0
      }
    };
  },
  computed: {
    filteredSales() {
      return this.sales.filter(sale => {
        const saleDate = new Date(sale.created_at).toISOString().split('T')[0];
        const from = this.fromDate || '0000-01-01';
        const to = this.toDate || '9999-12-31';
        return saleDate >= from && saleDate <= to;
      });
    },
    salesChartData() {
      const dailyTotals = {};
      this.filteredSales.forEach(sale => {
        const date = new Date(sale.created_at).toISOString().split('T')[0];
        if (!dailyTotals[date]) dailyTotals[date] = 0;
        dailyTotals[date] += parseFloat(sale.total);
      });

      const labels = Object.keys(dailyTotals).sort();
      const data = labels.map(date => dailyTotals[date]);

      return {
        labels,
        datasets: [
          {
            label: 'Total Sales',
            backgroundColor: '#3b82f6',
            data
          }
        ]
      };
    }
  },
  watch: {
    filteredSales: {
      handler: 'calculateSummary',
      immediate: true
    }
  },
  methods: {
    calculateSummary() {
      const filtered = this.filteredSales;
      const total = filtered.reduce((sum, sale) => sum + parseFloat(sale.total), 0);
      const count = filtered.length;
      this.summary.totalSales = total;
      this.summary.totalTransactions = count;
      this.summary.averageSale = count ? total / count : 0;
    }
  },
  async mounted() {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/till/sales/', {
        headers: {
          Authorization: `Token ${localStorage.getItem('token')}`
        }
      });
      this.sales = response.data;
    } catch (err) {
      console.error('Failed to fetch sales history:', err);
    }
  }
};
</script>

<style scoped>
.sales-history {
  padding: 20px;
}
.filters {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  align-items: center;
}
.filters label {
  font-weight: bold;
}
.filters input {
  margin-left: 5px;
  padding: 4px;
}
.chart-toggle {
  background-color: #3b82f6;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-left: auto;
}
.chart-container {
  max-width: 800px;
  height: 300px;
  margin: 0 auto 20px auto;
}
.summary-box {
  background-color: #f1f5f9;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
.summary-box p {
  margin: 4px 0;
}
.sales-table-wrapper {
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid #ccc;
  border-radius: 6px;
  margin-bottom: 20px;
}
.sales-table-wrapper table {
  width: 100%;
  border-collapse: collapse;
}
.sales-table-wrapper th,
.sales-table-wrapper td {
  padding: 8px;
  border: 1px solid #ccc;
}

.sales-table-wrapper thead th {
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 1;
}
</style>
