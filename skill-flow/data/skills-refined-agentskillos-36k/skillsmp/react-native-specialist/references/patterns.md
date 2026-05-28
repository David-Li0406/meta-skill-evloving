# React Native Specialist

## Patterns


---
  #### **Name**
Expo Managed Workflow
  #### **Description**
Maximum productivity with minimal native code
  #### **When**
Starting new React Native projects
  #### **Example**
    // Initialize with Expo
    npx create-expo-app@latest my-app --template tabs
    
    // Project structure
    my-app/
    ├── app/                    # File-based routing (Expo Router)
    │   ├── (tabs)/
    │   │   ├── index.tsx       # Home tab
    │   │   ├── profile.tsx     # Profile tab
    │   │   └── _layout.tsx     # Tab navigator
    │   ├── [id].tsx            # Dynamic route
    │   └── _layout.tsx         # Root layout
    ├── components/
    │   ├── ui/                 # Reusable UI components
    │   └── features/           # Feature-specific components
    ├── hooks/                  # Custom hooks
    ├── utils/                  # Helpers
    ├── constants/              # Theme, config
    └── app.json                # Expo config
    
    // app/_layout.tsx - Root with providers
    import { Stack } from 'expo-router';
    import { QueryClientProvider } from '@tanstack/react-query';
    import { ThemeProvider } from '@/contexts/theme';
    
    export default function RootLayout() {
      return (
        <QueryClientProvider client={queryClient}>
          <ThemeProvider>
            <Stack screenOptions={{ headerShown: false }} />
          </ThemeProvider>
        </QueryClientProvider>
      );
    }
    

---
  #### **Name**
Performance Optimized Lists
  #### **Description**
Smooth scrolling with large datasets
  #### **When**
Rendering lists with hundreds/thousands of items
  #### **Example**
    import { FlashList } from '@shopify/flash-list';
    import { memo, useCallback } from 'react';
    
    // Memoize row component
    const ListItem = memo(({ item }: { item: Item }) => (
      <View style={styles.item}>
        <Text>{item.title}</Text>
      </View>
    ));
    
    export function OptimizedList({ data }: { data: Item[] }) {
      // Stable callback
      const renderItem = useCallback(
        ({ item }: { item: Item }) => <ListItem item={item} />,
        []
      );
    
      // Stable key extractor
      const keyExtractor = useCallback(
        (item: Item) => item.id,
        []
      );
    
      return (
        <FlashList
          data={data}
          renderItem={renderItem}
          keyExtractor={keyExtractor}
          estimatedItemSize={80}  // Required for FlashList
          // Performance optimizations
          removeClippedSubviews
          initialNumToRender={10}
          maxToRenderPerBatch={10}
          windowSize={5}
        />
      );
    }
    

---
  #### **Name**
Offline-First Data
  #### **Description**
Work without network, sync when available
  #### **When**
Apps that must work offline
  #### **Example**
    import NetInfo from '@react-native-community/netinfo';
    import AsyncStorage from '@react-native-async-storage/async-storage';
    import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
    
    // Persist queries to storage
    import { createAsyncStoragePersister } from '@tanstack/query-async-storage-persister';
    import { persistQueryClient } from '@tanstack/react-query-persist-client';
    
    const asyncStoragePersister = createAsyncStoragePersister({
      storage: AsyncStorage,
    });
    
    persistQueryClient({
      queryClient,
      persister: asyncStoragePersister,
    });
    
    // Hook with offline support
    function useOfflineData<T>(key: string, fetcher: () => Promise<T>) {
      const queryClient = useQueryClient();
    
      return useQuery({
        queryKey: [key],
        queryFn: fetcher,
        staleTime: 1000 * 60 * 5,  // 5 minutes
        gcTime: 1000 * 60 * 60 * 24,  // 24 hours
        networkMode: 'offlineFirst',
        // Use stale data while fetching
        placeholderData: (prev) => prev,
      });
    }
    
    // Optimistic mutations
    function useOptimisticMutation<T, V>(
      key: string,
      mutationFn: (vars: V) => Promise<T>
    ) {
      const queryClient = useQueryClient();
    
      return useMutation({
        mutationFn,
        onMutate: async (newData) => {
          await queryClient.cancelQueries({ queryKey: [key] });
          const previous = queryClient.getQueryData([key]);
          queryClient.setQueryData([key], newData);
          return { previous };
        },
        onError: (err, newData, context) => {
          queryClient.setQueryData([key], context?.previous);
        },
        onSettled: () => {
          queryClient.invalidateQueries({ queryKey: [key] });
        },
      });
    }
    

---
  #### **Name**
Native Module Integration
  #### **Description**
Bridging to native iOS/Android code
  #### **When**
Need platform APIs not available in React Native
  #### **Example**
    // Using Expo Modules API (recommended)
    // modules/my-native-module/index.ts
    import { NativeModulesProxy } from 'expo-modules-core';
    
    const { MyNativeModule } = NativeModulesProxy;
    
    export function getDeviceInfo(): Promise<DeviceInfo> {
      return MyNativeModule.getDeviceInfo();
    }
    
    // modules/my-native-module/ios/MyNativeModule.swift
    import ExpoModulesCore
    
    public class MyNativeModule: Module {
      public func definition() -> ModuleDefinition {
        Name("MyNativeModule")
    
        AsyncFunction("getDeviceInfo") { () -> [String: Any] in
          return [
            "model": UIDevice.current.model,
            "systemVersion": UIDevice.current.systemVersion
          ]
        }
      }
    }
    
    // Usage in React Native
    import { getDeviceInfo } from './modules/my-native-module';
    
    const info = await getDeviceInfo();
    console.log(info.model); // "iPhone"
    

## Anti-Patterns


---
  #### **Name**
Inline Styles Everywhere
  #### **Description**
Creating new style objects on every render
  #### **Why**
Creates new objects every render, triggers re-renders, defeats memo
  #### **Instead**
Use StyleSheet.create() outside component, or styled-components

---
  #### **Name**
Ignoring Platform Differences
  #### **Description**
Same UI for iOS and Android
  #### **Why**
Users expect platform conventions - bottom tabs on iOS, drawer on Android
  #### **Instead**
Use Platform.select() or .ios.tsx/.android.tsx files

---
  #### **Name**
Heavy Bridge Traffic
  #### **Description**
Sending large objects or frequent updates to native
  #### **Why**
Bridge serialization is expensive, causes jank
  #### **Instead**
Batch updates, use Reanimated for animations, consider JSI

---
  #### **Name**
No Offline Handling
  #### **Description**
Assuming constant network connection
  #### **Why**
Mobile networks drop constantly, users get errors
  #### **Instead**
Offline-first with local storage and sync

---
  #### **Name**
Console.log in Production
  #### **Description**
Leaving console.log in production builds
  #### **Why**
Causes performance issues, exposes sensitive data
  #### **Instead**
Use Babel plugin to strip console in production