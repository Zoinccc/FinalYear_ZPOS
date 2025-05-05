

<template>
  
  <div class="sales-container">
    <!-- Left: Cart & Totals -->
    <div class="cart-section">
      <h2>Cart</h2>
      <div class="cart-divider"></div>
      <div class="cart-content">
        <div class="cart-info-box">
          <div class="cart-scroll">
          <!-- Product Table -->
          <table class="cart-table">
            <thead>
              <tr>
                <th>Product</th>
                <th>Qty</th>
                <th>Price</th>
                <th>Total</th>
                <th>Remove</th>
              </tr>
            </thead>
            <tbody v-if="cart.length">
              <tr v-for="(item, index) in cart" :key="index">
                <td>{{ item.name }}</td>
                <td>
                  <input
                    type="number"
                    v-model.number="item.quantity"
                    min="1"
                    @change="updateTotals"
                  />
                </td>
                <td>£{{ Number(item.price).toFixed(2) }}</td>
                <td>£{{ (Number(item.price) * item.quantity).toFixed(2) }}</td>
                <td>
                  <button @click="removeItem(index)" style="color: red; font-weight: bold;">
                    ❌ Remove
                  </button>
                </td>
              </tr>
            </tbody>
            <tbody v-else>
              <tr>
                <td colspan="5" style="text-align: center; color: #888;">No items in cart</td>
              </tr>
          </tbody>
        </table>

          <!-- Totals Always Visible -->
          <div style="margin-top: 20px;">
            <p><strong>Subtotal:</strong> £{{ subtotal.toFixed(2) }}</p>
            <p><strong>VAT (20%):</strong> £{{ vat.toFixed(2) }}</p>
            <p class="total-box">TOTAL: £{{ total.toFixed(2) }}</p>
          </div>
        </div>
       </div>
      </div>

      <!-- Barcode Input  -->
      <div class="barcode-input">
        <input v-model="searchInput" @keyup.enter="addProduct" placeholder="Enter barcode or product name" />
        <button @click="addProduct">Add to Cart</button>
      </div>
    </div>

    <!-- Right: Action Buttons -->
    <div class="action-buttons">
      <button class="action-button" @click="addBagLevy">
        <img src="@/assets/plastic-bag.png" alt="Bag Icon" class="button-icon" />
        Bag Levy 10p
      </button>
      <button class="action-button" @click="applyDiscount">
        <img src="@/assets/10-percent.png" alt="10% Icon" class="button-icon" />
        Apply 10% Discount
      </button>
      <button class="action-button" @click="viewReceipts">
        <img src="@/assets/receipt.png" alt="Receipt Icon" class="button-icon" />
        View Receipts
      </button>
      <button class="action-button" @click="priceOverride">
        <img src="@/assets/swap.png" alt="Price Override Icon" class="button-icon" />
        Price Override
      </button>
      <button class="action-button" @click="repeatLastItem">
        <img src="@/assets/repeat.png" alt="Repeat Icon" class="button-icon" />
        Repeat Last Item
      </button>
      <button class="action-button" @click="voidLastItem">
        <img src="@/assets/void.png" alt="Void Icon" class="button-icon" />
        Void Basket
      </button>
    </div>

    <!-- Complete Sale button  -->
    <div class="bottom-right">
      <button @click="openPaymentModal" class="complete-sale">Complete Sale</button>
    </div>

    <!-- Payment Modal -->
    <div class="modal-overlay" v-if="showPaymentModal">
      <div class="modal">
        <h3>Choose Payment Method</h3>

        <!-- Payment Method Selection -->
        <label>
          <input type="radio" value="card" v-model="paymentMethod" />
          Card
        </label>
        <label>
          <input type="radio" value="cash" v-model="paymentMethod" />
          Cash
        </label>

        <!-- Cash Options -->
        <div v-if="paymentMethod === 'cash'" class="cash-section">
          <p><strong>Amount Given:</strong></p>
          <div class="cash-buttons">
            <button @click="cashGiven = 5">£5</button>
            <button @click="cashGiven = 10">£10</button>
            <button @click="cashGiven = 20">£20</button>
            <button @click="cashGiven = 50">£50</button>
          </div>
          <input
            type="number"
            v-model.number="cashGiven"
            min="0"
            placeholder="Enter custom amount"
          />
          <p v-if="cashGiven >= total">Change Due: £{{ (cashGiven - total).toFixed(2) }}</p>
          <p v-else>Amount Owed: £{{ (total - cashGiven).toFixed(2) }}</p>
        </div>

        <div class="modal-buttons">
          <button @click="finalizePayment">Confirm</button>
          <button @click="cancelPayment">Cancel</button>
        </div>
      </div>
    </div>

    <!-- View Receipts Modal -->
    <div class="modal-overlay" v-if="showReceiptsModal">
      <div class="modal" style="max-height: 90vh; overflow-y: auto;">
        <h3>Today's Receipts</h3>

        <!-- Sale List -->
        <ul v-if="!selectedReceipt">
          <li v-for="sale in todaySales" :key="sale.id" style="margin-bottom: 10px;">
            <button @click="selectReceipt(sale)">Receipt #{{ sale.id }} - £{{ Number(sale.total).toFixed(2) }} - {{ new Date(sale.created_at).toLocaleString() }}</button>
          </li>
        </ul>

      <!-- Single Receipt View -->
      <div v-else>
        <button @click="selectedReceipt = null" style="margin-bottom: 10px;">← Back to List</button>
        <h3>Receipt #{{ selectedReceipt.id }}</h3>
        <p><strong>Date:</strong> {{ new Date(selectedReceipt.created_at).toLocaleString() }}</p>

        <table border="1" style="width: 100%; margin-top: 10px;">
          <thead>
            <tr>
              <th>Item</th>
              <th>Qty</th>
              <th>Price</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, i) in selectedReceipt.items" :key="i">
              <td>{{ item.name || 'Unknown' }}</td>
              <td>{{ item.quantity }}</td>
              <td>£{{ Number(item.price).toFixed(2) }}</td>
              <td>£{{ (item.quantity * item.price).toFixed(2) }}</td>
            </tr>
          </tbody>
        </table>

  <p style="margin-top: 10px;"><strong>Total:</strong> £{{ Number(selectedReceipt.total).toFixed(2) }}</p>
</div>

    <div class="modal-buttons">
      <button @click="showReceiptsModal = false">Close</button>
    </div>
  </div>
</div>


  </div>

</template>

<script>
import axios from 'axios';
import { setCartState } from '../router/index.js';

export default {
  name: 'SalesScreen',
  data() {
    return {
      cart: [],
      searchInput: '',
      subtotal: 0,
      vat: 0,
      total: 0,
      products: [],
      showPaymentModal: false,
      paymentMethod: 'card',
      cashGiven: 0,
      showReceiptsModal: false,
      todaySales: [],
      selectedReceipt: null,
    };
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/till/products/', {
          headers: { Authorization: `Token ${localStorage.getItem('token')}` },
        });
        this.products = response.data;
      } catch (err) {
        console.error('Failed to fetch products', err);
      }
    },
    addProduct() {
      const input = this.searchInput.trim().toLowerCase();
      const product = this.products.find(
        (p) => p.name.toLowerCase() === input || p.barcode === input
      );
      if (product) {
        const existing = this.cart.find((item) => item.id === product.id);
        if (existing) {
          existing.quantity += 1;
        } else {
          this.cart.push({ ...product, quantity: 1 });
        }
        this.updateTotals();
        this.searchInput = '';
      } else {
        alert('Product not found!');
      }
    },
    addBagLevy() {
      this.cart.push({ name: 'Bag Levy', price: 0.10, quantity: 1 });
      this.updateTotals();
    },
    addMiscCharge() {
      this.cart.push({ name: 'Misc Charge', price: 1.00, quantity: 1 });
      this.updateTotals();
    },
    applyDiscount() {
      this.total = this.total * 0.9;
      alert('10% Discount Applied!');
    },
    priceOverride() {
      if (this.cart.length === 0) {
        alert("Cart is empty.");
        return;
      }

      const itemNames = this.cart.map((item, index) => `${index + 1}. ${item.name}`).join('\n');
      const choice = prompt(`Enter item number to override price:\n${itemNames}`);

      const index = parseInt(choice) - 1;
      if (isNaN(index) || index < 0 || index >= this.cart.length) {
        alert("Invalid selection.");
        return;
      }

      const newPrice = parseFloat(prompt(`Enter new price for ${this.cart[index].name}:`));
      if (isNaN(newPrice) || newPrice <= 0) {
        alert("Invalid price.");
        return;
      }

      this.cart[index].price = newPrice;
      this.updateTotals();
      alert(`Price for ${this.cart[index].name} set to £${newPrice.toFixed(2)}.`);
    },
    repeatLastItem() {
      if (this.cart.length) {
        const lastItem = this.cart[this.cart.length - 1];
        this.cart.push({ ...lastItem });
        this.updateTotals();
      }
    },
    voidLastItem() {
      if (this.cart.length) {
        if (confirm('Are you sure you want to void the entire basket?')) {
          this.cart = [];
          this.subtotal = 0;
          this.vat = 0;
          this.total = 0;
        }
      }
    },
    printReceipt() {
      alert('(Mock) hardware limitations');
    },
    async viewReceipts() {
      const today = new Date().toISOString().split('T')[0];
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/till/sales/', {
          headers: {
            Authorization: `Token ${localStorage.getItem('token')}`
          }
        });
        this.todaySales = response.data.filter(sale => {
          return sale.created_at.startsWith(today);
        });
        this.selectedReceipt = null;
        this.showReceiptsModal = true;
      } catch (err) {
        alert('Failed to fetch sales.');
        console.error(err);
      }
    },
    selectReceipt(sale) {
      this.selectedReceipt = sale;
    },
    updateTotals() {
      this.subtotal = this.cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
      this.vat = this.subtotal * 0.2;
      this.total = this.subtotal + this.vat;
    },
    removeItem(index) {
      this.cart.splice(index, 1);
      this.updateTotals();
    },
    openPaymentModal() {
      if (this.cart.length === 0) {
        alert('Cart is empty.');
        return;
      }
      this.paymentMethod = 'card';
      this.cashGiven = 0;
      this.showPaymentModal = true;
    },
    cancelPayment() {
      this.showPaymentModal = false;
    },
    finalizePayment() {
      if (this.paymentMethod === 'cash' && this.cashGiven < this.total) {
        alert('Insufficient cash amount.');
        return;
      }
      this.showPaymentModal = false;
      this.completeSale();
    },
    async completeSale() {
      if (this.cart.length === 0) {
        alert('Cart is empty. Cannot complete sale.');
        return;
      }
      const payload = {
        items: this.cart
          .filter(item => item.id)
          .map(item => ({
            product_id: item.id,
            quantity: item.quantity
          })),
        total: Number(this.total.toFixed(2))
      };
      console.log("Submitting sale payload:", payload);
      try {
        await axios.post('http://127.0.0.1:8000/api/till/sales/', payload, {
          headers: {
            Authorization: `Token ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          }
        });
        alert(`Sale Completed! Total: £${this.total.toFixed(2)}`);
        this.cart = [];
        this.subtotal = 0;
        this.vat = 0;
        this.total = 0;
      } catch (error) {
        const data = error.response?.data;
        let message = 'An error occurred while completing the sale.';
        if (typeof data === 'string') {
          message = data;
        } else if (data?.non_field_errors?.length) {
          message = data.non_field_errors[0];
        } else if (data?.detail) {
          message = data.detail;
        }
        alert(`Failed to complete sale: ${message}`);
        console.error('Failed to complete sale:', error);
      }
    }
  },


  beforeRouteLeave(to, from, next) {
    if (this.cart.length > 0) {
      const confirmLeave = confirm("Cart is not empty. Are you sure you want to leave?");
      if (confirmLeave) {
        next();
      } else {
        next(false);
      }
    } else {
      next();
    }
  },

  mounted() {
    this.fetchProducts();

    this.$watch(
      () => this.cart.length,
      (newLength) => {
        setCartState(newLength > 0);
      }
    );
  }
};
</script>

<style scoped>
.sales-container {
  display: flex;
  min-height: 90vh; 
  gap: 20px;
  padding: 20px;
  background-color: #f5f7f9;
}

.cart-section {
  flex: 3;
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between; 
  min-height: 600px; 
}


.cart-table {
  width: 100%;
  margin-bottom: 15px;
  border-collapse: collapse;
}

.cart-table th,
.cart-table td {
  padding: 10px;
  text-align: center;
  border: 1px solid #ddd;
}


.cart-content {
  flex-grow: 1;
}

.barcode-input {
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.custom-items {
  flex: 0.5;
  display: flex;
  flex-direction: column;
}

.action-button {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 15px;
  padding: 10px 14px;
  background-color: white;
  border: 2px solid #1a1f36;; 
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  width: 100%;
  min-height: 48px;
  text-align: left;
  transition: all 0.2s ease;
  margin-bottom: 10px;
}

.action-button:hover .button-icon {
  filter: brightness(0) invert(1); 
}

.button-icon {
  width: 20px;
  height: 30px;
  object-fit: contain;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button:hover {
  background-color: #333;
}

.total-box {
  font-size: 24px;
  font-weight: bold;
  margin: 10px 0;
}

.bottom-right {
  position: fixed;
  bottom: 40px;
  right: 40px;
  z-index: 1000;
  display: flex;
  justify-content: flex-end;
}

.complete-sale {
  padding: 14px 30px;
  font-size: 16px;
  font-weight: 600;
  background-color: #28a745;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: background-color 0.2s ease;
}

.complete-sale:hover {
  background-color: #218838;
}

.cart-info-box {
  width: 95%;
  background-color: #eef2f5;
  padding: 10px 15px;
  margin: 10px auto 20px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  color: #333;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.cart-divider {
  height: 1px;
  background-color: #ccc;
  margin: 8px 0 16px 0;
  width: 100%;
}

.cart-scroll {
  max-height: 600px;
  overflow-y: auto;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
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

.modal h3 {
  margin-bottom: 10px;
}

.modal label {
  display: block;
  margin: 10px 0;
}

.cash-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.cash-buttons button {
  padding: 6px 12px;
  background-color: #e5e7eb;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
}

.modal input[type='number'] {
  width: 100%;
  padding: 6px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.modal-buttons button {
  padding: 8px 16px;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
}

</style>
