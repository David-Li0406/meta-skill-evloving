---
name: fullstory-privacy-controls-mobile
version: v3
platforms:
  - ios
  - android
  - flutter
  - react-native
sdks:
  - fullstory-swift
  - fullstory-android
  - fullstory-flutter
  - fullstory-react-native
description: Mobile implementation guide for Fullstory's Privacy Controls. Includes API reference and code examples for iOS (Swift/SwiftUI), Android (Kotlin/Jetpack Compose), Flutter (Dart), and React Native.
parent_skill: fullstory-privacy-controls
related_skills:
  - fullstory-privacy-controls
  - fullstory-privacy-strategy
  - fullstory-user-consent
---

# Fullstory Privacy Controls — Mobile Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for privacy modes, compliance guidance, and best practices.
>
> **Web Implementation**: See [SKILL-WEB.md](./SKILL-WEB.md) for JavaScript/CSS.

---

## Quick Reference

| Platform | SDK | Exclude | Mask | Unmask |
|----------|-----|---------|------|--------|
| iOS | `FullStory` | `FS.exclude(_:)` | `FS.mask(_:)` | `FS.unmask(_:)` |
| Android | `FullStory` | `FS.exclude(view)` | `FS.mask(view)` | `FS.unmask(view)` |
| Flutter | `fullstory_flutter` | `FS.exclude(key)` | `FS.mask(key)` | `FS.unmask(key)` |
| React Native | `@fullstory/react-native` | `fsClass="fs-exclude"` | `fsClass="fs-mask"` | `fsClass="fs-unmask"` |

---

## iOS (Swift/SwiftUI)

### API Reference

```swift
import FullStory

// Exclude a view (nothing captured, events ignored)
FS.exclude(view)

// Mask a view (structure captured, text wireframed)
FS.mask(view)

// Unmask a view (everything captured)
FS.unmask(view)

// SwiftUI modifiers
.fsExclude()
.fsMask()
.fsUnmask()
```

### ✅ GOOD Implementation Examples

#### Login Form with Proper Protection

```swift
// GOOD: UIKit login form with appropriate privacy
class LoginViewController: UIViewController {
    
    @IBOutlet weak var emailTextField: UITextField!
    @IBOutlet weak var passwordTextField: UITextField!
    @IBOutlet weak var loginButton: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        configurePrivacy()
    }
    
    private func configurePrivacy() {
        // Mask email (PII but structure useful)
        FS.mask(emailTextField)
        
        // Exclude password (never capture credentials)
        FS.exclude(passwordTextField)
        
        // Unmask login button (visible for funnel analysis)
        FS.unmask(loginButton)
    }
}
```

**Why this is good:**
- ✅ Explicit exclusion for password
- ✅ Email masked (PII protected, interactions tracked)
- ✅ Login button visible for conversion analysis

#### SwiftUI User Profile

```swift
// GOOD: SwiftUI profile with layered privacy
struct UserProfileView: View {
    let user: User
    
    var body: some View {
        VStack(spacing: 16) {
            // Mask PII but allow interaction tracking
            VStack(alignment: .leading) {
                Text(user.name)
                    .font(.title)
                Text(user.email)
                    .font(.subheadline)
            }
            .fsMask()
            
            // Public action buttons - unmask
            HStack {
                Button("Edit Profile") { editProfile() }
                Button("Settings") { openSettings() }
            }
            .fsUnmask()
            
            // Sensitive financial data - exclude entirely
            if let paymentMethod = user.paymentMethod {
                PaymentMethodView(method: paymentMethod)
                    .fsExclude()
            }
        }
    }
}
```

**Why this is good:**
- ✅ Name and email masked (structure visible, text wireframed)
- ✅ Action buttons fully visible for UX analysis
- ✅ Payment info completely excluded

#### Healthcare Form (HIPAA-Compliant)

```swift
// GOOD: Healthcare form with HIPAA-appropriate privacy
class PatientIntakeViewController: UIViewController {
    
    @IBOutlet weak var medicalHistoryStack: UIStackView!
    @IBOutlet weak var appointmentPrefsStack: UIStackView!
    @IBOutlet weak var navigationStack: UIStackView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        configurePrivacy()
    }
    
    private func configurePrivacy() {
        // PHI must be excluded, not just masked
        FS.exclude(medicalHistoryStack)
        
        // Appointment preferences can be masked
        FS.mask(appointmentPrefsStack)
        
        // Navigation elements unmasked
        FS.unmask(navigationStack)
    }
}

// SwiftUI version
struct PatientIntakeForm: View {
    @State private var medications = ""
    @State private var conditions: Set<String> = []
    @State private var preferredDate = Date()
    
    var body: some View {
        Form {
            // PHI - must be excluded
            Section("Medical History") {
                TextField("Current Medications", text: $medications)
                // Condition checkboxes...
            }
            .fsExclude()
            
            // Non-PHI preferences - can be masked
            Section("Appointment Preferences") {
                DatePicker("Preferred Date", selection: $preferredDate)
            }
            .fsMask()
            
            // Navigation - unmask
            Section {
                Button("Submit") { submit() }
            }
            .fsUnmask()
        }
    }
}
```

**Why this is good:**
- ✅ PHI (medications, conditions) completely excluded
- ✅ HIPAA compliance — no health data leaves device
- ✅ Non-PHI preferences masked for flow analysis
- ✅ Navigation buttons visible for funnel analysis

#### E-commerce Checkout

```swift
// GOOD: SwiftUI checkout with appropriate privacy levels
struct CheckoutView: View {
    let order: Order
    @State private var cardNumber = ""
    @State private var expiry = ""
    @State private var cvv = ""
    
    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                // Order summary - can show product names
                OrderSummaryView(items: order.items, total: order.total)
                    .fsUnmask()
                
                // Shipping address - mask the details
                ShippingAddressView(address: order.shippingAddress)
                    .fsMask()
                
                // Payment - exclude entirely (PCI compliance)
                VStack {
                    Text("Payment Method")
                        .font(.headline)
                    SecureField("Card Number", text: $cardNumber)
                    HStack {
                        TextField("MM/YY", text: $expiry)
                        SecureField("CVV", text: $cvv)
                    }
                }
                .fsExclude()
                
                // Action buttons visible
                Button("Place Order") { placeOrder() }
                    .fsUnmask()
            }
        }
    }
}
```

**Why this is good:**
- ✅ Order details visible for conversion analysis
- ✅ Shipping PII masked but structure shows flow
- ✅ Payment card data completely excluded (PCI compliance)
- ✅ Place Order button visible for funnel analysis

#### Table/Collection View with Cell Privacy

```swift
// GOOD: UICollectionView with privacy-aware cells
class ContactsViewController: UIViewController {
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Configure collection view...
    }
}

class ContactCell: UICollectionViewCell {
    
    @IBOutlet weak var nameLabel: UILabel!
    @IBOutlet weak var emailLabel: UILabel!
    @IBOutlet weak var phoneLabel: UILabel!
    @IBOutlet weak var callButton: UIButton!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        configurePrivacy()
    }
    
    private func configurePrivacy() {
        // Mask PII fields
        FS.mask(nameLabel)
        FS.mask(emailLabel)
        FS.mask(phoneLabel)
        
        // Unmask action button
        FS.unmask(callButton)
    }
    
    func configure(with contact: Contact) {
        nameLabel.text = contact.name
        emailLabel.text = contact.email
        phoneLabel.text = contact.phone
    }
}
```

### ❌ BAD Implementation Examples

```swift
// BAD: Entire view excluded (loses all analytics)
override func viewDidLoad() {
    super.viewDidLoad()
    FS.exclude(self.view)  // Everything excluded!
}

// BAD: Relying only on auto-detection
class PaymentViewController: UIViewController {
    @IBOutlet weak var ssnTextField: UITextField!  // Not excluded!
    @IBOutlet weak var accountNumberField: UITextField!  // Not excluded!
    // No explicit privacy configuration
}

// BAD: Using mask for highly sensitive data
FS.mask(ssnTextField)  // Should be excluded!
FS.mask(bankAccountField)  // Should be excluded!

// BAD: Privacy configured after view appears
override func viewDidAppear(_ animated: Bool) {
    super.viewDidAppear(animated)
    // Too late! Content may already be captured
    FS.mask(sensitiveLabel)
}
```

**CORRECTED:**

```swift
// GOOD: Granular privacy, configured early
override func viewDidLoad() {
    super.viewDidLoad()
    
    // Exclude highly sensitive fields
    FS.exclude(ssnTextField)
    FS.exclude(bankAccountField)
    
    // Mask PII
    FS.mask(nameTextField)
    FS.mask(emailTextField)
    
    // Unmask public content
    FS.unmask(submitButton)
}
```

---

## Android (Kotlin/Jetpack Compose)

### API Reference

```kotlin
import com.fullstory.FS

// Exclude a view (nothing captured, events ignored)
FS.exclude(view)

// Mask a view (structure captured, text wireframed)
FS.mask(view)

// Unmask a view (everything captured)
FS.unmask(view)
```

### ✅ GOOD Implementation Examples

#### Login Form with Proper Protection

```kotlin
// GOOD: Login activity with appropriate privacy
class LoginActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityLoginBinding
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLoginBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        configurePrivacy()
    }
    
    private fun configurePrivacy() {
        // Mask email (PII but structure useful)
        FS.mask(binding.emailEditText)
        
        // Exclude password (never capture credentials)
        FS.exclude(binding.passwordEditText)
        
        // Unmask login button (visible for funnel analysis)
        FS.unmask(binding.loginButton)
    }
}
```

**Why this is good:**
- ✅ Explicit exclusion for password
- ✅ Email masked (PII protected, interactions tracked)
- ✅ Login button visible for conversion analysis

#### User Profile with Layered Privacy

```kotlin
// GOOD: User profile fragment with appropriate privacy
class UserProfileFragment : Fragment() {
    
    private var _binding: FragmentUserProfileBinding? = null
    private val binding get() = _binding!!
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        configurePrivacy()
    }
    
    private fun configurePrivacy() {
        // Mask PII but allow click tracking
        FS.mask(binding.profileHeader)  // Contains name, email
        
        // Public action buttons - unmask
        FS.unmask(binding.editProfileButton)
        FS.unmask(binding.settingsButton)
        
        // Sensitive financial data - exclude entirely
        FS.exclude(binding.paymentMethodsSection)
    }
    
    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
```

#### Healthcare Form (HIPAA-Compliant)

```kotlin
// GOOD: Healthcare form with HIPAA-appropriate privacy
class PatientIntakeFragment : Fragment() {
    
    private var _binding: FragmentPatientIntakeBinding? = null
    private val binding get() = _binding!!
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        configurePrivacy()
    }
    
    private fun configurePrivacy() {
        // PHI must be excluded, not just masked
        FS.exclude(binding.medicalHistorySection)
        
        // Appointment preferences can be masked
        FS.mask(binding.appointmentPreferencesSection)
        
        // Navigation elements unmasked
        FS.unmask(binding.previousButton)
        FS.unmask(binding.submitButton)
    }
}
```

#### E-commerce Checkout

```kotlin
// GOOD: Checkout activity with appropriate privacy levels
class CheckoutActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityCheckoutBinding
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityCheckoutBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        configurePrivacy()
    }
    
    private fun configurePrivacy() {
        // Order summary - can show product names
        FS.unmask(binding.orderSummarySection)
        
        // Shipping address - mask the details
        FS.mask(binding.shippingAddressSection)
        
        // Payment - exclude entirely (PCI compliance)
        FS.exclude(binding.paymentSection)
        
        // Action buttons visible
        FS.unmask(binding.placeOrderButton)
        FS.unmask(binding.editCartButton)
    }
}
```

#### RecyclerView with Privacy-Aware Adapter

```kotlin
// GOOD: RecyclerView adapter with privacy configuration
class ContactsAdapter(
    private val contacts: List<Contact>,
    private val onContactClick: (Contact) -> Unit
) : RecyclerView.Adapter<ContactsAdapter.ContactViewHolder>() {
    
    inner class ContactViewHolder(
        private val binding: ItemContactBinding
    ) : RecyclerView.ViewHolder(binding.root) {
        
        init {
            configurePrivacy()
        }
        
        private fun configurePrivacy() {
            // Mask PII fields
            FS.mask(binding.nameText)
            FS.mask(binding.emailText)
            FS.mask(binding.phoneText)
            
            // Unmask action button
            FS.unmask(binding.callButton)
        }
        
        fun bind(contact: Contact) {
            binding.nameText.text = contact.name
            binding.emailText.text = contact.email
            binding.phoneText.text = contact.phone
            binding.callButton.setOnClickListener { onContactClick(contact) }
        }
    }
    
    // ... adapter implementation
}
```

#### Jetpack Compose Integration

```kotlin
// GOOD: Compose with privacy using AndroidView
@Composable
fun PrivacyAwareTextField(
    value: String,
    onValueChange: (String) -> Unit,
    privacyMode: PrivacyMode,
    modifier: Modifier = Modifier
) {
    AndroidView(
        factory = { context ->
            EditText(context).apply {
                when (privacyMode) {
                    PrivacyMode.EXCLUDE -> FS.exclude(this)
                    PrivacyMode.MASK -> FS.mask(this)
                    PrivacyMode.UNMASK -> FS.unmask(this)
                }
            }
        },
        update = { editText ->
            editText.setText(value)
        },
        modifier = modifier
    )
}

enum class PrivacyMode {
    EXCLUDE, MASK, UNMASK
}

// Usage
@Composable
fun CheckoutScreen() {
    Column {
        // Mask email
        PrivacyAwareTextField(
            value = email,
            onValueChange = { email = it },
            privacyMode = PrivacyMode.MASK
        )
        
        // Exclude credit card
        PrivacyAwareTextField(
            value = cardNumber,
            onValueChange = { cardNumber = it },
            privacyMode = PrivacyMode.EXCLUDE
        )
    }
}
```

### ❌ BAD Implementation Examples

```kotlin
// BAD: Entire view excluded (loses all analytics)
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    setContentView(binding.root)
    FS.exclude(binding.root)  // Everything excluded!
}

// BAD: Relying only on auto-detection
class PaymentActivity : AppCompatActivity() {
    // No explicit privacy configuration
    // SSN and account fields not excluded!
}

// BAD: Using mask for highly sensitive data
FS.mask(binding.ssnEditText)  // Should be excluded!
FS.mask(binding.bankAccountEditText)  // Should be excluded!

// BAD: Privacy configured in onResume (too late)
override fun onResume() {
    super.onResume()
    // Too late! Content may already be captured
    FS.mask(binding.sensitiveText)
}
```

---

## Flutter (Dart)

### API Reference

```dart
import 'package:fullstory_flutter/fs.dart';

// Exclude a widget (nothing captured, events ignored)
FS.exclude(GlobalKey key);

// Mask a widget (structure captured, text wireframed)
FS.mask(GlobalKey key);

// Unmask a widget (everything captured)
FS.unmask(GlobalKey key);
```

### ✅ GOOD Implementation Examples

#### Login Form with Proper Protection

```dart
// GOOD: Login form with appropriate privacy
class LoginScreen extends StatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailKey = GlobalKey();
  final _passwordKey = GlobalKey();
  final _loginButtonKey = GlobalKey();
  
  String _email = '';
  String _password = '';

  @override
  void initState() {
    super.initState();
    // Configure privacy after first frame
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _configurePrivacy();
    });
  }

  void _configurePrivacy() {
    // Mask email (PII but structure useful)
    FS.mask(_emailKey);
    
    // Exclude password (never capture credentials)
    FS.exclude(_passwordKey);
    
    // Unmask login button (visible for funnel analysis)
    FS.unmask(_loginButtonKey);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              key: _emailKey,
              decoration: const InputDecoration(labelText: 'Email'),
              onChanged: (value) => _email = value,
            ),
            TextField(
              key: _passwordKey,
              decoration: const InputDecoration(labelText: 'Password'),
              obscureText: true,
              onChanged: (value) => _password = value,
            ),
            ElevatedButton(
              key: _loginButtonKey,
              onPressed: _login,
              child: const Text('Login'),
            ),
          ],
        ),
      ),
    );
  }

  void _login() {
    // Login logic
  }
}
```

#### User Profile with Layered Privacy

```dart
// GOOD: User profile with appropriate privacy levels
class UserProfileScreen extends StatefulWidget {
  final User user;
  
  const UserProfileScreen({required this.user, Key? key}) : super(key: key);

  @override
  State<UserProfileScreen> createState() => _UserProfileScreenState();
}

class _UserProfileScreenState extends State<UserProfileScreen> {
  final _profileHeaderKey = GlobalKey();
  final _actionsKey = GlobalKey();
  final _paymentKey = GlobalKey();

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _configurePrivacy();
    });
  }

  void _configurePrivacy() {
    // Mask PII but allow click tracking
    FS.mask(_profileHeaderKey);
    
    // Public action buttons - unmask
    FS.unmask(_actionsKey);
    
    // Sensitive financial data - exclude entirely
    FS.exclude(_paymentKey);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          // Profile header with PII
          Container(
            key: _profileHeaderKey,
            child: Column(
              children: [
                CircleAvatar(backgroundImage: NetworkImage(widget.user.avatarUrl)),
                Text(widget.user.name, style: Theme.of(context).textTheme.titleLarge),
                Text(widget.user.email),
              ],
            ),
          ),
          
          // Action buttons
          Row(
            key: _actionsKey,
            children: [
              ElevatedButton(onPressed: () {}, child: const Text('Edit Profile')),
              ElevatedButton(onPressed: () {}, child: const Text('Settings')),
            ],
          ),
          
          // Payment methods
          Container(
            key: _paymentKey,
            child: Column(
              children: [
                const Text('Saved Payment Methods'),
                Text('**** **** **** ${widget.user.cardLast4}'),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
```

#### E-commerce Checkout

```dart
// GOOD: Checkout with appropriate privacy levels
class CheckoutScreen extends StatefulWidget {
  final Order order;
  
  const CheckoutScreen({required this.order, Key? key}) : super(key: key);

  @override
  State<CheckoutScreen> createState() => _CheckoutScreenState();
}

class _CheckoutScreenState extends State<CheckoutScreen> {
  final _orderSummaryKey = GlobalKey();
  final _shippingKey = GlobalKey();
  final _paymentKey = GlobalKey();
  final _actionsKey = GlobalKey();

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _configurePrivacy();
    });
  }

  void _configurePrivacy() {
    // Order summary - can show product names
    FS.unmask(_orderSummaryKey);
    
    // Shipping address - mask the details
    FS.mask(_shippingKey);
    
    // Payment - exclude entirely (PCI compliance)
    FS.exclude(_paymentKey);
    
    // Action buttons visible
    FS.unmask(_actionsKey);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Order summary
            Container(
              key: _orderSummaryKey,
              child: OrderSummaryWidget(order: widget.order),
            ),
            
            // Shipping address
            Container(
              key: _shippingKey,
              child: ShippingAddressWidget(address: widget.order.shippingAddress),
            ),
            
            // Payment section
            Container(
              key: _paymentKey,
              child: const PaymentFormWidget(),
            ),
            
            // Actions
            Row(
              key: _actionsKey,
              children: [
                TextButton(onPressed: () {}, child: const Text('Edit Cart')),
                ElevatedButton(onPressed: () {}, child: const Text('Place Order')),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
```

### ❌ BAD Implementation Examples

```dart
// BAD: No privacy configuration at all
class PaymentScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        TextField(decoration: InputDecoration(labelText: 'SSN')),
        TextField(decoration: InputDecoration(labelText: 'Card Number')),
        // No privacy controls! Sensitive data captured!
      ],
    );
  }
}

// BAD: Privacy configured without keys
void _configurePrivacy() {
  // Can't configure privacy without GlobalKey references!
}

// BAD: Using mask for highly sensitive data
FS.mask(_ssnKey);  // Should be excluded!
FS.mask(_bankAccountKey);  // Should be excluded!
```

---

## React Native

### API Reference

```javascript
import FullStory, { FSPage } from '@fullstory/react-native';

// Use fsClass prop on components
<View fsClass="fs-exclude">...</View>
<View fsClass="fs-mask">...</View>
<View fsClass="fs-unmask">...</View>

// Or use the FSPage component for screens
<FSPage fsClass="fs-mask">
  <YourScreenContent />
</FSPage>
```

### ✅ GOOD Implementation Examples

#### Login Form with Proper Protection

```jsx
// GOOD: Login form with appropriate privacy
import React, { useState } from 'react';
import { View, TextInput, TouchableOpacity, Text, StyleSheet } from 'react-native';

function LoginScreen({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  return (
    <View style={styles.container}>
      {/* Mask email (PII but structure useful) */}
      <View fsClass="fs-mask">
        <TextInput
          style={styles.input}
          placeholder="Email"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
        />
      </View>

      {/* Exclude password (never capture credentials) */}
      <View fsClass="fs-exclude">
        <TextInput
          style={styles.input}
          placeholder="Password"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />
      </View>

      {/* Unmask login button (visible for funnel analysis) */}
      <View fsClass="fs-unmask">
        <TouchableOpacity style={styles.button} onPress={() => onLogin(email, password)}>
          <Text style={styles.buttonText}>Login</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16 },
  input: { borderWidth: 1, borderColor: '#ccc', padding: 12, marginBottom: 12, borderRadius: 4 },
  button: { backgroundColor: '#007bff', padding: 16, borderRadius: 4 },
  buttonText: { color: '#fff', textAlign: 'center', fontWeight: '600' },
});

export default LoginScreen;
```

#### User Profile with Layered Privacy

```jsx
// GOOD: User profile with appropriate privacy levels
import React from 'react';
import { View, Text, Image, TouchableOpacity, StyleSheet } from 'react-native';

function UserProfileScreen({ user, onEditProfile, onSettings }) {
  return (
    <View style={styles.container}>
      {/* Mask PII but allow click tracking */}
      <View fsClass="fs-mask" style={styles.profileHeader}>
        <Image source={{ uri: user.avatarUrl }} style={styles.avatar} />
        <Text style={styles.name}>{user.name}</Text>
        <Text style={styles.email}>{user.email}</Text>
      </View>

      {/* Public action buttons - unmask */}
      <View fsClass="fs-unmask" style={styles.actions}>
        <TouchableOpacity style={styles.actionButton} onPress={onEditProfile}>
          <Text>Edit Profile</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.actionButton} onPress={onSettings}>
          <Text>Settings</Text>
        </TouchableOpacity>
      </View>

      {/* Sensitive financial data - exclude entirely */}
      {user.paymentMethod && (
        <View fsClass="fs-exclude" style={styles.paymentSection}>
          <Text style={styles.sectionTitle}>Saved Payment Methods</Text>
          <Text>**** **** **** {user.paymentMethod.last4}</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  profileHeader: { alignItems: 'center', marginBottom: 20 },
  avatar: { width: 80, height: 80, borderRadius: 40 },
  name: { fontSize: 20, fontWeight: '600', marginTop: 8 },
  email: { fontSize: 14, color: '#666' },
  actions: { flexDirection: 'row', justifyContent: 'space-around', marginBottom: 20 },
  actionButton: { padding: 12, backgroundColor: '#f0f0f0', borderRadius: 4 },
  paymentSection: { padding: 16, backgroundColor: '#f9f9f9', borderRadius: 8 },
  sectionTitle: { fontSize: 16, fontWeight: '600', marginBottom: 8 },
});

export default UserProfileScreen;
```

#### Healthcare Form (HIPAA-Compliant)

```jsx
// GOOD: Healthcare form with HIPAA-appropriate privacy
import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';

function PatientIntakeForm({ onSubmit }) {
  const [medications, setMedications] = useState('');
  const [preferredDate, setPreferredDate] = useState('');

  return (
    <ScrollView style={styles.container}>
      {/* PHI must be excluded, not just masked */}
      <View fsClass="fs-exclude" style={styles.section}>
        <Text style={styles.sectionTitle}>Medical History</Text>
        <TextInput
          style={styles.textArea}
          placeholder="Current medications"
          value={medications}
          onChangeText={setMedications}
          multiline
        />
        {/* Condition checkboxes would go here */}
      </View>

      {/* Appointment preferences can be masked */}
      <View fsClass="fs-mask" style={styles.section}>
        <Text style={styles.sectionTitle}>Appointment Preferences</Text>
        <TextInput
          style={styles.input}
          placeholder="Preferred date"
          value={preferredDate}
          onChangeText={setPreferredDate}
        />
      </View>

      {/* Navigation elements unmasked */}
      <View fsClass="fs-unmask" style={styles.actions}>
        <TouchableOpacity style={styles.button}>
          <Text style={styles.buttonText}>Previous</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.button, styles.primaryButton]} onPress={onSubmit}>
          <Text style={[styles.buttonText, styles.primaryButtonText]}>Submit</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  section: { marginBottom: 20 },
  sectionTitle: { fontSize: 18, fontWeight: '600', marginBottom: 12 },
  input: { borderWidth: 1, borderColor: '#ccc', padding: 12, borderRadius: 4 },
  textArea: { borderWidth: 1, borderColor: '#ccc', padding: 12, borderRadius: 4, minHeight: 100 },
  actions: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 20 },
  button: { padding: 16, backgroundColor: '#f0f0f0', borderRadius: 4, flex: 1, marginHorizontal: 4 },
  primaryButton: { backgroundColor: '#007bff' },
  buttonText: { textAlign: 'center' },
  primaryButtonText: { color: '#fff', fontWeight: '600' },
});

export default PatientIntakeForm;
```

#### E-commerce Checkout

```jsx
// GOOD: Checkout with appropriate privacy levels
import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';

function CheckoutScreen({ order, onPlaceOrder }) {
  const [cardNumber, setCardNumber] = useState('');
  const [expiry, setExpiry] = useState('');
  const [cvv, setCvv] = useState('');

  return (
    <ScrollView style={styles.container}>
      {/* Order summary - can show product names */}
      <View fsClass="fs-unmask" style={styles.section}>
        <Text style={styles.sectionTitle}>Your Order</Text>
        {order.items.map(item => (
          <View key={item.id} style={styles.orderItem}>
            <Text>{item.name}</Text>
            <Text>${item.price.toFixed(2)}</Text>
          </View>
        ))}
        <Text style={styles.total}>Total: ${order.total.toFixed(2)}</Text>
      </View>

      {/* Shipping address - mask the details */}
      <View fsClass="fs-mask" style={styles.section}>
        <Text style={styles.sectionTitle}>Shipping To</Text>
        <Text>{order.shippingAddress.name}</Text>
        <Text>{order.shippingAddress.street}</Text>
        <Text>{order.shippingAddress.city}, {order.shippingAddress.state}</Text>
      </View>

      {/* Payment - exclude entirely (PCI compliance) */}
      <View fsClass="fs-exclude" style={styles.section}>
        <Text style={styles.sectionTitle}>Payment</Text>
        <TextInput
          style={styles.input}
          placeholder="Card Number"
          value={cardNumber}
          onChangeText={setCardNumber}
          keyboardType="numeric"
        />
        <View style={styles.row}>
          <TextInput
            style={[styles.input, styles.halfInput]}
            placeholder="MM/YY"
            value={expiry}
            onChangeText={setExpiry}
          />
          <TextInput
            style={[styles.input, styles.halfInput]}
            placeholder="CVV"
            value={cvv}
            onChangeText={setCvv}
            keyboardType="numeric"
            secureTextEntry
          />
        </View>
      </View>

      {/* Action buttons visible */}
      <View fsClass="fs-unmask" style={styles.actions}>
        <TouchableOpacity style={[styles.button, styles.primaryButton]} onPress={onPlaceOrder}>
          <Text style={styles.primaryButtonText}>Place Order</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  section: { marginBottom: 20, padding: 16, backgroundColor: '#f9f9f9', borderRadius: 8 },
  sectionTitle: { fontSize: 18, fontWeight: '600', marginBottom: 12 },
  orderItem: { flexDirection: 'row', justifyContent: 'space-between', paddingVertical: 8 },
  total: { fontSize: 18, fontWeight: '600', marginTop: 12, paddingTop: 12, borderTopWidth: 1, borderTopColor: '#ddd' },
  input: { borderWidth: 1, borderColor: '#ccc', padding: 12, borderRadius: 4, marginBottom: 12 },
  row: { flexDirection: 'row', justifyContent: 'space-between' },
  halfInput: { width: '48%' },
  actions: { marginTop: 20 },
  button: { padding: 16, borderRadius: 4 },
  primaryButton: { backgroundColor: '#28a745' },
  primaryButtonText: { color: '#fff', textAlign: 'center', fontSize: 18, fontWeight: '600' },
});

export default CheckoutScreen;
```

### ❌ BAD Implementation Examples

```jsx
// BAD: No privacy controls on sensitive data
function PaymentScreen() {
  return (
    <View>
      <TextInput placeholder="SSN" />  {/* Not excluded! */}
      <TextInput placeholder="Card Number" />  {/* Not excluded! */}
    </View>
  );
}

// BAD: Using mask for highly sensitive data
<View fsClass="fs-mask">
  <TextInput placeholder="SSN" />  {/* Should be fs-exclude! */}
  <TextInput placeholder="Bank Account" />  {/* Should be fs-exclude! */}
</View>

// BAD: Entire screen excluded (loses all analytics)
<FSPage fsClass="fs-exclude">
  <CheckoutContent />  {/* Everything excluded! */}
</FSPage>
```

---

## Common Patterns (All Platforms)

### Privacy Configuration Timing

| Platform | When to Configure |
|----------|-------------------|
| iOS (Swift) | `viewDidLoad()` |
| iOS (SwiftUI) | `.onAppear` or use modifiers |
| Android | `onCreate()` / `onViewCreated()` |
| Flutter | `initState()` with `addPostFrameCallback` |
| React Native | Component mount (via props) |

### Data Classification Guide

| Data Type | Recommended Mode | Reason |
|-----------|------------------|--------|
| Passwords / credentials | **Exclude** | Security |
| Credit card numbers | **Exclude** | PCI compliance |
| CVV / security codes | **Exclude** | PCI compliance |
| SSN / Tax IDs | **Exclude** | Regulatory |
| Bank account numbers | **Exclude** | Financial data |
| Medical conditions | **Exclude** | HIPAA |
| User names | Mask | PII but structure useful |
| Email addresses | Mask | PII but interaction useful |
| Phone numbers | Mask | PII but structure useful |
| Addresses | Mask | PII but form flow useful |
| Product names | Unmask | Business data |
| Prices | Unmask | Analytics value |
| Navigation buttons | Unmask | UX analysis |

---

## Reference Links

- **iOS**: https://developer.fullstory.com/mobile/ios/privacy/
- **Android**: https://developer.fullstory.com/mobile/android/privacy/
- **Flutter**: https://developer.fullstory.com/mobile/flutter/privacy/
- **React Native**: https://developer.fullstory.com/mobile/react-native/privacy/
