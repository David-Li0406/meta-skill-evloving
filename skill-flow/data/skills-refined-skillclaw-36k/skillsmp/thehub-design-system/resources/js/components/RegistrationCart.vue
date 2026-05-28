<template>
  <div class="registration-cart">
    
    <!-- STEG 1: Välj Event/Serie -->
    <div v-if="step === 1" class="step step-1">
      <h2>Välj event eller serie</h2>
      
      <div class="event-type-selector">
        <button 
          @click="eventType = 'event'" 
          :class="{ active: eventType === 'event' }"
        >
          📅 Enskilt Event
        </button>
        <button 
          @click="eventType = 'series'" 
          :class="{ active: eventType === 'series' }"
        >
          🏆 Serie (Spara 15-20%)
        </button>
      </div>
      
      <!-- Event-lista -->
      <div v-if="eventType === 'event'" class="event-list">
        <div 
          v-for="event in events" 
          :key="event.id" 
          class="event-card"
          @click="selectEvent(event)"
        >
          <h3>{{ event.name }}</h3>
          <p class="date">{{ formatDate(event.date) }}</p>
          <p class="location">📍 {{ event.location }}</p>
          <div v-if="event.early_bird_active" class="badge early-bird">
            Early Bird -{{ event.early_bird_percent }}%
          </div>
        </div>
      </div>
      
      <!-- Serie-lista -->
      <div v-if="eventType === 'series'" class="series-list">
        <div 
          v-for="series in seriesList" 
          :key="series.id" 
          class="series-card"
          @click="selectSeries(series)"
        >
          <h3>{{ series.name }}</h3>
          <p>{{ series.events_count }} event • Spara {{ series.discount_percent }}%</p>
          <div class="badge series">Serie-rabatt</div>
        </div>
      </div>
    </div>
    
    <!-- STEG 2: Lägg till deltagare -->
    <div v-if="step === 2" class="step step-2">
      
      <!-- Header med vald event/serie -->
      <div class="selected-event-header">
        <button @click="step = 1" class="btn-back">← Tillbaka</button>
        <div class="event-info">
          <h3>{{ selectedEvent ? selectedEvent.name : selectedSeries.name }}</h3>
          <span v-if="selectedEvent" class="type-badge">Enskilt event</span>
          <span v-else class="type-badge series">Serie</span>
        </div>
      </div>
      
      <!-- Varukorg med tillagda riders -->
      <div v-if="cartItems.length > 0" class="cart-items">
        <h3>Anmälda deltagare ({{ cartItems.length }})</h3>
        
        <div 
          v-for="(item, index) in cartItems" 
          :key="index" 
          class="cart-item"
        >
          <div class="rider-info">
            <div class="rider-avatar">
              {{ item.rider.firstname.charAt(0) }}{{ item.rider.lastname.charAt(0) }}
            </div>
            <div class="rider-details">
              <strong>{{ item.rider.firstname }} {{ item.rider.lastname }}</strong>
              <span class="class-name">{{ item.class.name }}</span>
              <span v-if="item.rider.license_number" class="license">
                #{{ item.rider.license_number }}
              </span>
            </div>
          </div>
          <div class="item-price">
            <span class="price">{{ formatPrice(item.price) }} kr</span>
            <span v-if="item.early_bird_discount > 0" class="discount">
              Sparat: {{ formatPrice(item.early_bird_discount) }} kr
            </span>
          </div>
          <button @click="removeItem(index)" class="btn-remove">
            🗑️
          </button>
        </div>
      </div>
      
      <!-- Lägg till ny deltagare -->
      <div class="add-rider-section">
        <h3>Lägg till deltagare {{ cartItems.length + 1 }}</h3>
        
        <!-- Välj befintlig eller skapa ny -->
        <div class="rider-selector-tabs">
          <button 
            @click="addMode = 'existing'" 
            :class="{ active: addMode === 'existing' }"
          >
            Välj befintlig rider
          </button>
          <button 
            @click="addMode = 'new'" 
            :class="{ active: addMode === 'new' }"
          >
            + Skapa ny deltagare
          </button>
        </div>
        
        <!-- BEFINTLIG RIDER -->
        <div v-if="addMode === 'existing'" class="existing-rider-selector">
          <div class="search-box">
            <input 
              v-model="riderSearch" 
              type="text" 
              placeholder="Sök efter namn eller licensnummer..."
              @input="searchRiders"
            />
          </div>
          
          <div class="rider-list">
            <div 
              v-for="rider in filteredRiders" 
              :key="rider.id"
              @click="selectRider(rider)"
              :class="{ selected: selectedRiderId === rider.id }"
              class="rider-option"
            >
              <div class="rider-avatar small">
                {{ rider.firstname.charAt(0) }}{{ rider.lastname.charAt(0) }}
              </div>
              <div class="rider-info">
                <strong>{{ rider.firstname }} {{ rider.lastname }}</strong>
                <span class="meta">
                  {{ rider.age }} år • {{ rider.gender === 'male' ? 'Man' : 'Kvinna' }}
                  <span v-if="rider.license_number">#{{ rider.license_number }}</span>
                </span>
              </div>
              <div class="rider-license">
                {{ rider.license_type }}
              </div>
            </div>
          </div>
        </div>
        
        <!-- NY RIDER -->
        <div v-if="addMode === 'new'" class="new-rider-form">
          <div class="form-grid">
            <div class="form-group">
              <label>Förnamn *</label>
              <input v-model="newRider.firstname" type="text" required />
            </div>
            
            <div class="form-group">
              <label>Efternamn *</label>
              <input v-model="newRider.lastname" type="text" required />
            </div>
            
            <div class="form-group">
              <label>E-post *</label>
              <input v-model="newRider.email" type="email" required />
            </div>
            
            <div class="form-group">
              <label>Födelsedatum *</label>
              <input v-model="newRider.birth_date" type="date" required />
            </div>
            
            <div class="form-group">
              <label>Kön *</label>
              <select v-model="newRider.gender" required>
                <option value="">-- Välj --</option>
                <option value="male">Man</option>
                <option value="female">Kvinna</option>
              </select>
            </div>
            
            <div class="form-group">
              <label>Licenstyp *</label>
              <select v-model="newRider.license_type" required>
                <option value="">-- Välj --</option>
                <option value="Svenska Cykelförbundet">Svenska Cykelförbundet</option>
                <option value="UCI">UCI</option>
                <option value="Daglicens">Daglicens</option>
                <option value="Ingen">Ingen</option>
              </select>
            </div>
            
            <div class="form-group">
              <label>Licensnummer</label>
              <input v-model="newRider.license_number" type="text" />
              <small>Om tillämpligt</small>
            </div>
            
            <div class="form-group">
              <label>Klubb</label>
              <select v-model="newRider.club_id">
                <option value="">-- Välj klubb --</option>
                <option v-for="club in clubs" :key="club.id" :value="club.id">
                  {{ club.name }}
                </option>
              </select>
            </div>
          </div>
          
          <button @click="createAndSelectRider" class="btn-primary" :disabled="!isNewRiderValid">
            Skapa och välj rider
          </button>
        </div>
        
        <!-- VÄLJ KLASS -->
        <div v-if="selectedRiderId" class="class-selector">
          <h4>Välj klass för {{ selectedRider.firstname }}</h4>
          
          <div v-if="loadingClasses" class="loading">
            Laddar tillgängliga klasser...
          </div>
          
          <div v-else class="class-list">
            <div 
              v-for="cls in eligibleClasses" 
              :key="cls.id"
              :class="{ 
                'class-option': true,
                'not-eligible': !cls.eligible,
                'selected': selectedClassId === cls.id
              }"
              @click="cls.eligible && (selectedClassId = cls.id)"
            >
              <div class="class-header">
                <input 
                  type="radio" 
                  :value="cls.id" 
                  v-model="selectedClassId"
                  :disabled="!cls.eligible"
                />
                <strong>{{ cls.name }}</strong>
                
                <span v-if="!cls.eligible" class="not-eligible-badge">
                  ❌ {{ cls.reason }}
                </span>
              </div>
              
              <div class="class-pricing">
                <span class="final-price">{{ formatPrice(cls.final_price) }} kr</span>
                <span v-if="cls.discount > 0" class="original-price">
                  {{ formatPrice(cls.original_price) }} kr
                </span>
                <span v-if="cls.discount > 0" class="discount-badge">
                  -{{ formatPrice(cls.discount) }} kr
                </span>
              </div>
              
              <div class="class-requirements">
                <span v-if="cls.min_age">{{ cls.min_age }}-{{ cls.max_age }} år</span>
                <span v-if="cls.license_required">Licens: {{ cls.license_required }}</span>
              </div>
            </div>
          </div>
          
          <button 
            @click="addToCart" 
            class="btn-add-to-cart"
            :disabled="!selectedClassId"
          >
            ✓ Lägg till i anmälan ({{ formatPrice(selectedClassPrice) }} kr)
          </button>
        </div>
      </div>
      
      <!-- SUMMERING -->
      <div v-if="cartItems.length > 0" class="cart-summary">
        <h3>Sammanfattning</h3>
        
        <div class="summary-lines">
          <div class="summary-line">
            <span>{{ cartItems.length }} deltagare</span>
            <span>{{ formatPrice(subtotal) }} kr</span>
          </div>
          
          <div v-if="totalEarlyBirdDiscount > 0" class="summary-line discount">
            <span>Early bird-rabatt</span>
            <span>-{{ formatPrice(totalEarlyBirdDiscount) }} kr</span>
          </div>
          
          <div v-if="seriesDiscount > 0" class="summary-line discount">
            <span>Serie-rabatt ({{ selectedSeries.discount_percent }}%)</span>
            <span>-{{ formatPrice(seriesDiscount) }} kr</span>
          </div>
          
          <div class="summary-line">
            <span>Plattformsavgift</span>
            <span>{{ formatPrice(platformFee) }} kr</span>
          </div>
          
          <div class="summary-line">
            <span>Swish-avgift</span>
            <span>{{ formatPrice(paymentFee) }} kr</span>
          </div>
          
          <div class="summary-total">
            <strong>TOTALT ATT BETALA</strong>
            <strong>{{ formatPrice(totalAmount) }} kr</strong>
          </div>
        </div>
        
        <!-- Sparad betalningsavgift -->
        <div v-if="cartItems.length > 1" class="savings-notice">
          💰 Du sparar <strong>{{ formatPrice((cartItems.length - 1) * 1) }} kr</strong> 
          i Swish-avgifter genom att betala allt på en gång!
        </div>
        
        <button @click="step = 3" class="btn-primary btn-large">
          Fortsätt till betalning →
        </button>
      </div>
    </div>
    
    <!-- STEG 3: Bekräfta och betala -->
    <div v-if="step === 3" class="step step-3">
      <h2>Bekräfta och betala</h2>
      
      <!-- Order-sammanfattning -->
      <div class="order-summary">
        <h3>Din order</h3>
        
        <div class="order-header">
          <span class="order-ref">Order: {{ orderReference }}</span>
          <span class="order-date">{{ new Date().toLocaleDateString('sv-SE') }}</span>
        </div>
        
        <div class="order-items">
          <div v-for="(item, index) in cartItems" :key="index" class="order-item">
            <span class="item-number">{{ index + 1 }}.</span>
            <div class="item-details">
              <strong>{{ item.rider.firstname }} {{ item.rider.lastname }}</strong>
              <span class="event-name">
                {{ selectedEvent ? selectedEvent.name : selectedSeries.name }}
              </span>
              <span class="class-name">{{ item.class.name }}</span>
            </div>
            <span class="item-price">{{ formatPrice(item.price) }} kr</span>
          </div>
        </div>
        
        <div class="order-total-section">
          <div class="total-line">
            <span>Summa:</span>
            <span>{{ formatPrice(subtotal) }} kr</span>
          </div>
          <div v-if="totalDiscount > 0" class="total-line">
            <span>Rabatter:</span>
            <span>-{{ formatPrice(totalDiscount) }} kr</span>
          </div>
          <div class="total-line">
            <span>Avgifter:</span>
            <span>{{ formatPrice(platformFee + paymentFee) }} kr</span>
          </div>
          <div class="total-final">
            <strong>TOTALT:</strong>
            <strong>{{ formatPrice(totalAmount) }} kr</strong>
          </div>
        </div>
      </div>
      
      <!-- Betalare-info -->
      <div class="buyer-info">
        <h3>Betalare</h3>
        <div class="form-group">
          <label>Namn *</label>
          <input v-model="buyer.name" type="text" required />
        </div>
        <div class="form-group">
          <label>E-post *</label>
          <input v-model="buyer.email" type="email" required />
        </div>
        <div class="form-group">
          <label>Telefon *</label>
          <input v-model="buyer.phone" type="tel" required />
        </div>
      </div>
      
      <!-- Betalningsmetod -->
      <div class="payment-methods">
        <button 
          @click="payWithSwish" 
          class="btn-payment swish"
          :disabled="processing"
        >
          <span class="payment-logo">📱</span>
          <span>Betala med Swish</span>
          <span class="payment-amount">{{ formatPrice(totalAmount) }} kr</span>
        </button>
        
        <button 
          @click="payWithStripe" 
          class="btn-payment stripe"
          :disabled="processing"
        >
          <span class="payment-logo">💳</span>
          <span>Betala med kort</span>
          <span class="payment-amount">{{ formatPrice(totalAmount) }} kr</span>
        </button>
      </div>
      
      <div v-if="processing" class="processing-overlay">
        <div class="spinner"></div>
        <p>Skapar order...</p>
      </div>
    </div>
    
  </div>
</template>

<script>
export default {
  name: 'RegistrationCart',
  
  data() {
    return {
      step: 1,
      eventType: 'event',
      addMode: 'existing',
      
      // Selections
      selectedEvent: null,
      selectedSeries: null,
      selectedRiderId: null,
      selectedClassId: null,
      
      // Lists
      events: [],
      seriesList: [],
      riders: [],
      filteredRiders: [],
      eligibleClasses: [],
      clubs: [],
      
      // Cart
      cartItems: [],
      
      // New rider form
      newRider: {
        firstname: '',
        lastname: '',
        email: '',
        birth_date: '',
        gender: '',
        license_type: '',
        license_number: '',
        club_id: null
      },
      
      // Buyer info
      buyer: {
        name: '',
        email: '',
        phone: ''
      },
      
      // State
      riderSearch: '',
      loadingClasses: false,
      processing: false,
      orderReference: this.generateOrderReference()
    }
  },
  
  computed: {
    selectedRider() {
      return this.riders.find(r => r.id === this.selectedRiderId);
    },
    
    selectedClassPrice() {
      const cls = this.eligibleClasses.find(c => c.id === this.selectedClassId);
      return cls ? cls.final_price : 0;
    },
    
    subtotal() {
      return this.cartItems.reduce((sum, item) => sum + item.price, 0);
    },
    
    totalEarlyBirdDiscount() {
      return this.cartItems.reduce((sum, item) => sum + (item.early_bird_discount || 0), 0);
    },
    
    seriesDiscount() {
      if (!this.selectedSeries) return 0;
      return this.cartItems.reduce((sum, item) => sum + (item.series_discount || 0), 0);
    },
    
    totalDiscount() {
      return this.totalEarlyBirdDiscount + this.seriesDiscount;
    },
    
    platformFee() {
      const afterDiscount = this.subtotal - this.totalDiscount;
      return Math.round((afterDiscount * 0.025 + 10) * 100) / 100;
    },
    
    paymentFee() {
      return 1.00; // Swish flat fee
    },
    
    totalAmount() {
      return this.subtotal - this.totalDiscount + this.platformFee + this.paymentFee;
    },
    
    isNewRiderValid() {
      return this.newRider.firstname 
        && this.newRider.lastname 
        && this.newRider.email 
        && this.newRider.birth_date 
        && this.newRider.gender 
        && this.newRider.license_type;
    }
  },
  
  mounted() {
    this.loadEvents();
    this.loadSeries();
    this.loadRiders();
    this.loadClubs();
    
    // Pre-fill buyer if logged in
    if (window.user) {
      this.buyer.name = window.user.name;
      this.buyer.email = window.user.email;
      this.buyer.phone = window.user.phone;
    }
  },
  
  methods: {
    
    // === DATA LOADING ===
    
    async loadEvents() {
      const response = await axios.get('/api/events?status=upcoming');
      this.events = response.data.events;
    },
    
    async loadSeries() {
      const response = await axios.get('/api/series?status=active');
      this.seriesList = response.data.series;
    },
    
    async loadRiders() {
      const response = await axios.get('/api/riders/my-riders');
      this.riders = response.data.riders;
      this.filteredRiders = this.riders;
    },
    
    async loadClubs() {
      const response = await axios.get('/api/clubs');
      this.clubs = response.data.clubs;
    },
    
    // === STEP 1: SELECT EVENT/SERIES ===
    
    selectEvent(event) {
      this.selectedEvent = event;
      this.selectedSeries = null;
      this.step = 2;
    },
    
    selectSeries(series) {
      this.selectedSeries = series;
      this.selectedEvent = null;
      this.step = 2;
    },
    
    // === STEP 2: ADD RIDERS ===
    
    searchRiders() {
      const search = this.riderSearch.toLowerCase();
      this.filteredRiders = this.riders.filter(r => 
        r.firstname.toLowerCase().includes(search) ||
        r.lastname.toLowerCase().includes(search) ||
        (r.license_number && r.license_number.includes(search))
      );
    },
    
    async selectRider(rider) {
      this.selectedRiderId = rider.id;
      this.loadingClasses = true;
      
      try {
        const endpoint = this.selectedEvent 
          ? `/api/events/${this.selectedEvent.id}/classes`
          : `/api/series/${this.selectedSeries.id}/classes`;
        
        const response = await axios.get(endpoint, {
          params: { rider_id: rider.id }
        });
        
        this.eligibleClasses = response.data.classes;
      } catch (error) {
        console.error('Failed to load classes:', error);
      } finally {
        this.loadingClasses = false;
      }
    },
    
    async createAndSelectRider() {
      try {
        const response = await axios.post('/api/riders/create-from-registration', this.newRider);
        
        if (response.data.success) {
          this.riders.push(response.data.rider);
          this.selectedRiderId = response.data.rider.id;
          await this.selectRider(response.data.rider);
          this.addMode = 'existing';
          
          // Reset form
          this.newRider = {
            firstname: '',
            lastname: '',
            email: '',
            birth_date: '',
            gender: '',
            license_type: '',
            license_number: '',
            club_id: null
          };
        }
      } catch (error) {
        alert('Kunde inte skapa rider: ' + error.response.data.message);
      }
    },
    
    addToCart() {
      const cls = this.eligibleClasses.find(c => c.id === this.selectedClassId);
      
      if (!cls) return;
      
      const item = {
        type: this.selectedEvent ? 'event' : 'series',
        rider: this.selectedRider,
        event: this.selectedEvent,
        series: this.selectedSeries,
        class: cls,
        price: cls.final_price,
        early_bird_discount: cls.early_bird_discount || 0,
        series_discount: cls.series_discount || 0,
        rider_id: this.selectedRider.id,
        event_id: this.selectedEvent?.id,
        series_id: this.selectedSeries?.id,
        class_id: cls.id
      };
      
      this.cartItems.push(item);
      
      // Reset selection
      this.selectedRiderId = null;
      this.selectedClassId = null;
      this.eligibleClasses = [];
      this.riderSearch = '';
      this.filteredRiders = this.riders;
    },
    
    removeItem(index) {
      this.cartItems.splice(index, 1);
    },
    
    // === STEP 3: PAYMENT ===
    
    async payWithSwish() {
      await this.submitOrder('swish');
    },
    
    async payWithStripe() {
      await this.submitOrder('stripe');
    },
    
    async submitOrder(paymentMethod) {
      this.processing = true;
      
      try {
        const response = await axios.post('/api/orders/create', {
          buyer: this.buyer,
          items: this.cartItems.map(item => ({
            type: item.type,
            rider_id: item.rider_id,
            event_id: item.event_id,
            series_id: item.series_id,
            class_id: item.class_id
          })),
          payment_method: paymentMethod
        });
        
        if (response.data.success) {
          // Redirect till betalning
          if (paymentMethod === 'swish') {
            window.location.href = response.data.payment.swish_url;
          } else {
            window.location.href = response.data.payment.stripe_url;
          }
        } else {
          alert('Kunde inte skapa order: ' + response.data.error);
        }
        
      } catch (error) {
        console.error('Order creation failed:', error);
        alert('Ett fel uppstod: ' + error.response.data.message);
      } finally {
        this.processing = false;
      }
    },
    
    // === UTILITIES ===
    
    formatPrice(amount) {
      return new Intl.NumberFormat('sv-SE', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }).format(amount);
    },
    
    formatDate(date) {
      return new Date(date).toLocaleDateString('sv-SE', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },
    
    generateOrderReference() {
      const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
      let ref = '';
      for (let i = 0; i < 5; i++) {
        ref += chars.charAt(Math.floor(Math.random() * chars.length));
      }
      const date = new Date();
      ref += String(date.getMonth() + 1).padStart(2, '0');
      ref += String(date.getDate()).padStart(2, '0');
      return ref;
    }
  }
}
</script>

<style scoped>
/* Stilar kommer i separat fil - detta är funktionaliteten */
</style>
