---
name: navigation-expo-router
description: Use this skill when implementing navigation in Expo Router applications.
---

# Navigation - Expo Router

This skill provides guidelines and best practices for implementing navigation in Expo Router applications. Follow these steps to ensure a smooth navigation experience.

1. **Set Up Navigation**: Install the necessary packages for Expo Router.
   ```bash
   npm install expo-router
   ```

2. **Create Navigation Structure**: Define your navigation structure in your application.
   ```javascript
   import { Stack } from 'expo-router';

   export default function App() {
     return (
       <Stack>
         <Stack.Screen name="home" component={HomeScreen} />
         <Stack.Screen name="details" component={DetailsScreen} />
       </Stack>
     );
   }
   ```

3. **Navigate Between Screens**: Use the navigation methods to move between screens.
   ```javascript
   import { useRouter } from 'expo-router';

   const HomeScreen = () => {
     const router = useRouter();

     return (
       <Button title="Go to Details" onPress={() => router.push('/details')} />
     );
   };
   ```

4. **Handle Navigation State**: Manage navigation state and parameters as needed.
   ```javascript
   const DetailsScreen = ({ route }) => {
     const { itemId } = route.params;

     return (
       <Text>Item ID: {itemId}</Text>
     );
   };
   ```

5. **Refer to Documentation**: For detailed documentation, refer to the official Expo Router documentation.