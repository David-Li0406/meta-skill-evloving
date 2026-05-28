# React Native Specialist - Sharp Edges

## Inline Style Objects

### **Id**
inline-style-objects
### **Summary**
Inline styles create new objects every render
### **Severity**
high
### **Situation**
Styling components
### **Why**
  <View style={{ flex: 1, padding: 10 }} /> creates a new object every
  render. This defeats memo() and causes unnecessary re-renders. In lists
  with hundreds of items, this causes visible jank.
  
### **Solution**
  1. Use StyleSheet.create() outside component:
     const styles = StyleSheet.create({
       container: { flex: 1, padding: 10 }
     });
  
     // In component
     <View style={styles.container} />
  
  2. For dynamic styles, memoize:
     const dynamicStyle = useMemo(
       () => ({ backgroundColor: isActive ? 'blue' : 'gray' }),
       [isActive]
     );
  
  3. Use style arrays for composition:
     <View style={[styles.base, isActive && styles.active]} />
  
### **Symptoms**
  - Slow scrolling in lists
  - UI jank during animations
  - High JS thread usage in profiler
### **Detection Pattern**
style=\{\{|style=\{[^}]+\}

## Bridge Bottleneck

### **Id**
bridge-bottleneck
### **Summary**
Heavy bridge traffic causes performance issues
### **Severity**
critical
### **Situation**
Animations, frequent updates, large data
### **Why**
  React Native's bridge serializes all data between JS and native.
  Sending 60 updates/second for animations means 60 serialization
  cycles/second. Large objects (images, long lists) block the bridge.
  Result: dropped frames, unresponsive UI.
  
### **Solution**
  1. Use Reanimated for animations (runs on UI thread):
     import Animated, {
       useAnimatedStyle,
       withSpring
     } from 'react-native-reanimated';
  
     const animatedStyle = useAnimatedStyle(() => ({
       transform: [{ translateX: withSpring(offset.value) }],
     }));
  
  2. Batch state updates:
     // BAD - 3 bridge crossings
     setA(1); setB(2); setC(3);
  
     // GOOD - 1 bridge crossing
     setState({ a: 1, b: 2, c: 3 });
  
  3. Use FlashList for large lists (minimizes bridge traffic)
  
  4. For image-heavy apps, use FastImage with caching
  
### **Symptoms**
  - Animations drop frames
  - UI freezes during data updates
  - "Slow bridge" warnings in profiler
### **Detection Pattern**
Animated\.timing|setInterval.*setState

## Memory Leak Listeners

### **Id**
memory-leak-listeners
### **Summary**
Event listeners not cleaned up cause memory leaks
### **Severity**
high
### **Situation**
Adding listeners in components
### **Why**
  Keyboard.addListener, DeviceEventEmitter, navigation listeners -
  all must be removed. If you add in useEffect without cleanup,
  listeners accumulate. Eventually app crashes or becomes unresponsive.
  
### **Solution**
  1. Always return cleanup from useEffect:
     useEffect(() => {
       const subscription = Keyboard.addListener('keyboardDidShow', onShow);
       return () => subscription.remove();  // Cleanup!
     }, []);
  
  2. Use hook versions when available:
     import { useKeyboard } from '@react-native-community/hooks';
     const { keyboardShown } = useKeyboard();
  
  3. For navigation:
     useEffect(() => {
       const unsubscribe = navigation.addListener('focus', onFocus);
       return unsubscribe;  // Returns cleanup function
     }, [navigation]);
  
  4. For AppState:
     useEffect(() => {
       const sub = AppState.addEventListener('change', handleChange);
       return () => sub.remove();
     }, []);
  
### **Symptoms**
  - Memory grows over time
  - Multiple handler calls for single event
  - App becomes sluggish after navigation
### **Detection Pattern**
addListener|addEventListener(?!.*remove)

## Async Storage Misuse

### **Id**
async-storage-misuse
### **Summary**
AsyncStorage is slow and has size limits
### **Severity**
medium
### **Situation**
Storing data locally
### **Why**
  AsyncStorage is key-value, serializes to JSON, and has a 6MB limit
  on Android. Storing large objects or frequent reads/writes causes
  performance issues. It's for preferences, not databases.
  
### **Solution**
  1. For large data, use proper storage:
     // MMKV - fast, encrypted
     import { MMKV } from 'react-native-mmkv';
     const storage = new MMKV();
     storage.set('user', JSON.stringify(user));
  
  2. For complex queries, use SQLite:
     import * as SQLite from 'expo-sqlite';
  
  3. For AsyncStorage, keep entries small:
     // BAD - storing full app state
     AsyncStorage.setItem('state', JSON.stringify(hugeState));
  
     // GOOD - store minimal data
     AsyncStorage.setItem('userId', userId);
     AsyncStorage.setItem('theme', theme);
  
  4. Batch operations:
     AsyncStorage.multiSet([
       ['key1', 'value1'],
       ['key2', 'value2'],
     ]);
  
### **Symptoms**
  - Slow app startup
  - "6MB limit exceeded" errors on Android
  - UI freezes on storage operations
### **Detection Pattern**
AsyncStorage\.setItem.*JSON\.stringify.*large

## Hermes Not Enabled

### **Id**
hermes-not-enabled
### **Summary**
Hermes engine disabled, using JSC with worse performance
### **Severity**
medium
### **Situation**
Production builds
### **Why**
  Hermes is Meta's JS engine optimized for React Native. It has faster
  startup (bytecode precompilation), lower memory usage, and better
  performance. Many older tutorials don't enable it.
  
### **Solution**
  1. Enable in app.json (Expo):
     {
       "expo": {
         "jsEngine": "hermes"
       }
     }
  
  2. Verify it's enabled:
     const isHermes = () => !!global.HermesInternal;
     console.log('Using Hermes:', isHermes());
  
  3. For bare React Native, enable in gradle/Podfile
  
  4. Note Hermes limitations:
     - Some older libraries may not be compatible
     - Debugging requires Hermes debugger
  
### **Symptoms**
  - Slow cold start
  - High memory usage
  - JSC-specific performance issues
### **Detection Pattern**
jsEngine.*jsc|HermesInternal.*undefined

## Expo Dev Client Missing

### **Id**
expo-dev-client-missing
### **Summary**
Using Expo Go with custom native code fails
### **Severity**
high
### **Situation**
Adding native modules to Expo project
### **Why**
  Expo Go contains a fixed set of native modules. If you add a library
  with native code, it won't work in Expo Go. You need a development
  build with expo-dev-client.
  
### **Solution**
  1. Install expo-dev-client:
     npx expo install expo-dev-client
  
  2. Create development build:
     npx expo prebuild
     npx expo run:ios  # or run:android
  
  3. Or use EAS Build:
     eas build --profile development --platform ios
  
  4. Structure for native modules:
     modules/
     └── my-module/
         ├── index.ts
         ├── ios/
         │   └── MyModule.swift
         └── android/
             └── MyModule.kt
  
  5. Add to app.json:
     {
       "expo": {
         "plugins": ["./modules/my-module"]
       }
     }
  
### **Symptoms**
  - "Native module not found" errors
  - Library works in simulator but not Expo Go
  - Need features not in Expo Go
### **Detection Pattern**
requireNativeComponent|NativeModules\.

## Platform Specific Bugs

### **Id**
platform-specific-bugs
### **Summary**
Code works on iOS but breaks on Android (or vice versa)
### **Severity**
medium
### **Situation**
Cross-platform development
### **Why**
  iOS and Android have different behaviors: shadows, touch handling,
  text rendering, keyboard, permissions. Testing only on one platform
  means shipping bugs on the other.
  
### **Solution**
  1. Use Platform-specific code:
     import { Platform } from 'react-native';
  
     const styles = StyleSheet.create({
       shadow: Platform.select({
         ios: {
           shadowColor: '#000',
           shadowOffset: { width: 0, height: 2 },
           shadowOpacity: 0.25,
         },
         android: {
           elevation: 4,
         },
       }),
     });
  
  2. Platform-specific files:
     // Button.ios.tsx
     // Button.android.tsx
     // Import as 'Button' - bundler picks correct one
  
  3. Test on both platforms regularly:
     - iOS Simulator + Android Emulator
     - Real devices for accurate testing
  
  4. Common differences to watch:
     - Shadows (iOS: shadow*, Android: elevation)
     - Fonts (different defaults)
     - Touch feedback (iOS: opacity, Android: ripple)
     - StatusBar behavior
  
### **Symptoms**
  - UI looks different on platforms
  - Features work on one platform only
  - Crashes on one platform
### **Detection Pattern**
shadowColor|elevation(?!.*Platform)

## Navigation State Loss

### **Id**
navigation-state-loss
### **Summary**
Navigation state lost on app restart or deep link
### **Severity**
medium
### **Situation**
Complex navigation with deep linking
### **Why**
  By default, navigation state is in memory. App kill = back to home.
  Deep links may not work if screen isn't mounted. State restoration
  and proper deep link handling need explicit implementation.
  
### **Solution**
  1. Persist navigation state:
     import { NavigationContainer } from '@react-navigation/native';
     import AsyncStorage from '@react-native-async-storage/async-storage';
  
     const PERSISTENCE_KEY = 'NAVIGATION_STATE';
  
     function App() {
       const [isReady, setIsReady] = useState(false);
       const [initialState, setInitialState] = useState();
  
       useEffect(() => {
         AsyncStorage.getItem(PERSISTENCE_KEY).then((state) => {
           if (state) setInitialState(JSON.parse(state));
           setIsReady(true);
         });
       }, []);
  
       if (!isReady) return null;
  
       return (
         <NavigationContainer
           initialState={initialState}
           onStateChange={(state) =>
             AsyncStorage.setItem(PERSISTENCE_KEY, JSON.stringify(state))
           }
         >
           {/* ... */}
         </NavigationContainer>
       );
     }
  
  2. Configure deep links properly:
     const linking = {
       prefixes: ['myapp://', 'https://myapp.com'],
       config: {
         screens: {
           Home: '',
           Profile: 'user/:id',
           Settings: 'settings',
         },
       },
     };
  
### **Symptoms**
  - App always starts at home screen
  - Deep links don't navigate correctly
  - Back button behavior unexpected
### **Detection Pattern**
NavigationContainer(?!.*initialState)