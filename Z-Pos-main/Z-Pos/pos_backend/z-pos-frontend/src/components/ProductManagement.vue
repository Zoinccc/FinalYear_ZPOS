<template>
  <div class="product-management">
    <h2>Product Management</h2>

    <!-- Add Product Button -->
    <button class="add-button" @click="openAddModal">+ Add Product</button>

    <!-- Filters -->
    <div class="filters">
      <!-- Search Bar -->
      <div class="search-bar">
        <input
          v-model="searchQuery"
          placeholder="Search by barcode, category, or price"
          type="text"
        />
      </div>

      <!-- Stock Filter -->
      <div class="stock-filter">
        <select v-model="stockFilter">
          <option value="">All Stock Levels</option>
          <option value="out">Out of Stock</option>
          <option value="low">Low Stock (&lt; 10)</option>
          <option value="in">In Stock (≥ 10)</option>
        </select>
      </div>
    </div>

    <!-- Product Table -->
    <table class="product-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Price</th>
          <th>Barcode</th>
          <th>Stock</th>
          <th>Category</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in filteredProducts" :key="product.id">
          <td>{{ product.name }}</td>
          <td>£{{ Number(product.price).toFixed(2) }}</td>
          <td>{{ product.barcode }}</td>
          <td>{{ product.stock }}</td>
          <td>{{ getCategoryName(product.category) }}</td>
          <td>
            <button @click="openEditModal(product)">Edit</button>
            <button @click="deleteProduct(product.id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Add Modal -->
    <div v-if="showAddModal" class="modal-overlay">
      <div class="modal">
        <h3>Add Product</h3>
        <form @submit.prevent="addProduct">
          <input v-model="newProduct.name" placeholder="Product Name" required />
          <input v-model.number="newProduct.price" placeholder="Price" type="number" step="0.01" required />
          <input v-model="newProduct.barcode" placeholder="Barcode" type="text" required />
          <input v-model.number="newProduct.stock" placeholder="Stock" type="number" required />
          <select v-model="newProduct.category" required>
            <option disabled value="">Select Category</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
          <div class="modal-buttons">
            <button type="submit">Save</button>
            <button type="button" @click="resetAddForm">Reset</button>
            <button type="button" @click="closeAddModal">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal-overlay">
      <div class="modal">
        <h3>Edit Product</h3>
        <form @submit.prevent="updateProduct">
          <input v-model="editProductData.name" placeholder="Product Name" required />
          <input v-model.number="editProductData.price" placeholder="Price" type="number" step="0.01" required />
          <input v-model="editProductData.barcode" placeholder="Barcode" type="text" required />
          <input v-model.number="editProductData.stock" placeholder="Stock" type="number" required />
          <div class="modal-buttons">
            <button type="submit">Save</button>
            <button type="button" @click="closeEditModal">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ProductManagement',
  data() {
    return {
      products: [],
      categories: [],
      showAddModal: false,
      showEditModal: false,
      searchQuery: '',
      stockFilter: '',
      newProduct: {
        name: '',
        price: '',
        barcode: '',
        stock: '',
        category: '',
      },
      editProductData: {}
    };
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/till/products/', {
          headers: { Authorization: `Token ${localStorage.getItem('token')}` }
        });
        this.products = response.data;
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    },
    async fetchCategories() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/till/categories/', {
          headers: { Authorization: `Token ${localStorage.getItem('token')}` }
        });
        this.categories = response.data;
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },
    async addProduct() {
      try {
        await axios.post('http://127.0.0.1:8000/api/till/products/', this.newProduct, {
          headers: { Authorization: `Token ${localStorage.getItem('token')}` }
        });
        this.fetchProducts();
        this.newProduct = { name: '', price: '', barcode: '', stock: '', category: '' };
        this.closeAddModal();
        }catch (error) {
    console.error('Add error:', error.response?.data || error);
    alert(
      'Failed to add product:\n' +
      JSON.stringify(error.response?.data || {}, null, 2)
    );
}
    },
    openAddModal() {
      this.newProduct = {
        name: '',
        price: '',
        barcode: '',
        stock: '',
        category: ''
      };
      this.showAddModal = true;
    },

    openEditModal(product) {
      const matchedCategory = this.categories.find(c => c.name === product.category);
      const categoryId = matchedCategory ? matchedCategory.id : '';

      this.editProductData = {
        ...product,
        category: categoryId
      };
      this.showEditModal = true;
    },
    async updateProduct() { 
      try {
        await axios.put(`http://127.0.0.1:8000/api/till/products/${this.editProductData.id}/`, this.editProductData, {
          headers: { Authorization: `Token ${localStorage.getItem('token')}` }
        });
        this.fetchProducts();
        this.closeEditModal();
      } catch (error) {
        alert('Failed to update product. Admins only?');
        console.error(error);
      }
    },

    resetAddForm() {
      this.newProduct = {
        name: '',
        price: '',
        barcode: '',
        stock: '',
        category: ''
      };
    },
    getCategoryName(id) {
      const category = this.categories.find(cat => cat.id === id);
      return category ? category.name : 'Unknown';
    },
    closeAddModal() {
      this.showAddModal = false;
    },
    closeEditModal() {
      this.showEditModal = false;
    },

    async deleteProduct(id) {
      if (!confirm('Are you sure you want to delete this product?')) return;
      try {
        const product = this.products.find(p => p.id === id);
        const payload = {
          name: product.name,
          price: product.price,
          barcode: product.barcode,
          stock: product.stock,
          category: product.category,
          is_active: false
        };
        await axios.put(`http://127.0.0.1:8000/api/till/products/${id}/`, payload, {
          headers: { Authorization: `Token ${localStorage.getItem('token')}` }
        });
        this.fetchProducts();
      } catch (error) {
        alert('Failed to hide product. Admins only?');
        console.error(error);
      }
    },
  },

  computed: {
    filteredProducts() {
      const q = this.searchQuery.toLowerCase();
      return this.products.filter(p => {
        const barcode = p.barcode?.toString().toLowerCase() || '';
        const price = p.price?.toString() || '';
        const category = this.getCategoryName(p.category)?.toLowerCase() || '';

        const matchesSearch =
          barcode.includes(q) ||
          price.includes(q) ||
          category.includes(q);

        const matchesStock =
          this.stockFilter === '' ||
          (this.stockFilter === 'out' && p.stock === 0) ||
          (this.stockFilter === 'low' && p.stock > 0 && p.stock < 10) ||
          (this.stockFilter === 'in' && p.stock >= 10);

        return matchesSearch && matchesStock;
      });
    }
},
  mounted() {
    this.fetchProducts();
    this.fetchCategories();
  }
};
</script>

<style scoped>
.product-management {
  padding: 20px;
}
.add-button {
  padding: 10px 16px;
  background-color: #1a1f36;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 20px;
}
.product-table {
  width: 100%;
  border-collapse: collapse;
}
.product-table th,
.product-table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: left;
}
button {
  padding: 6px 10px;
  margin-right: 5px;
  cursor: pointer;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}
.modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}
.modal-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}
.modal input,
.modal select {
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.search-bar {
  margin-bottom: 15px;
}

.search-bar input {
  width: 200%;
  padding: 8px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 14px;
}

.filters {
  display: flex;
  gap: 250px;
  margin-bottom: 15px;
}

.stock-filter select {
  padding: 8px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 14px;
}

</style>
