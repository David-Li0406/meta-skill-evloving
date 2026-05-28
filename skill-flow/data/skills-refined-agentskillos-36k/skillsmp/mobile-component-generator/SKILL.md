---
name: mobile-component-generator
description: Generates React Native components following GradientPeak mobile patterns
---

# Mobile Component Generator Skill

## When to Use
- User asks to create a new mobile component
- User wants to add a new screen/modal
- User needs a list component with data fetching
- User asks to generate UI for a feature

## What This Skill Does
1. Analyzes component requirements from user request
2. Determines component type (smart vs presentational)
3. Generates component with proper patterns:
   - NativeWind styling (every Text styled directly)
   - React Native Reusables UI components
   - Proper imports and exports
   - TypeScript types
   - Error boundaries if needed
4. Adds to proper directory structure
5. Generates basic tests if requested

## Component Types Generated

### 1. List Component
FlatList/FlashList with loading, empty, and error states

**Template:**
```tsx
import { FlashList } from '@shopify/flash-list';
import { View, Text } from 'react-native';
import { trpc } from '@/lib/trpc';
import { ActivityCard } from '@/components/activity/ActivityCard';
import { Skeleton } from '@/components/ui/skeleton';

export function ActivityList() {
  const { data, isLoading, error, refetch } = trpc.activities.list.useQuery();

  if (isLoading) {
    return (
      <View className="p-4">
        {Array.from({ length: 5 }).map((_, i) => (
          <Skeleton key={i} className="h-24 mb-4" />
        ))}
      </View>
    );
  }

  if (error) {
    return (
      <View className="p-4 items-center justify-center">
        <Text className="text-destructive mb-4">{error.message}</Text>
        <Button onPress={() => refetch()}>
          <Text className="text-primary-foreground">Retry</Text>
        </Button>
      </View>
    );
  }

  if (!data || data.length === 0) {
    return (
      <View className="p-4 items-center justify-center flex-1">
        <Text className="text-muted-foreground">No activities found</Text>
      </View>
    );
  }

  return (
    <FlashList
      data={data}
      keyExtractor={(item) => item.id}
      estimatedItemSize={120}
      renderItem={({ item }) => (
        <ActivityCard
          activity={item}
          onPress={(id) => {
            activitySelectionStore.getState().select(id);
            router.push('/(internal)/(standard)/activity-detail');
          }}
        />
      )}
    />
  );
}
```

### 2. Card Component
Presentational component with props

**Template:**
```tsx
import { View, Text, TouchableOpacity } from 'react-native';
import { Icon } from '@/components/ui/icon';
import { ChevronRight } from 'lucide-react-native';
import type { Activity } from '@repo/core';

export interface ActivityCardProps {
  activity: Activity;
  onPress?: (id: string) => void;
  showChevron?: boolean;
}

export const ActivityCard = React.memo(({
  activity,
  onPress,
  showChevron = true,
}: ActivityCardProps) => {
  return (
    <TouchableOpacity
      onPress={() => onPress?.(activity.id)}
      className="bg-card p-4 rounded-lg mb-3 border border-border"
      accessibilityRole="button"
      accessibilityLabel={`${activity.name}, ${activity.type} activity`}
    >
      <View className="flex-row items-center justify-between">
        <View className="flex-1">
          <Text className="text-foreground font-semibold text-lg mb-1">
            {activity.name}
          </Text>
          <View className="flex-row gap-4">
            <Text className="text-muted-foreground">
              {(activity.distance / 1000).toFixed(2)} km
            </Text>
            <Text className="text-muted-foreground">
              {formatDuration(activity.duration)}
            </Text>
          </View>
        </View>
        {showChevron && (
          <Icon as={ChevronRight} className="text-muted-foreground" size={20} />
        )}
      </View>
    </TouchableOpacity>
  );
});

ActivityCard.displayName = 'ActivityCard';
```

### 3. Modal Component
With form integration

**Template:**
```tsx
import { Modal } from '@/components/ui/modal';
import { Button } from '@/components/ui/button';
import { View, Text } from 'react-native';
import { useState } from 'react';

export interface CreateActivityModalProps {
  visible: boolean;
  onClose: () => void;
  onSuccess?: () => void;
}

export function CreateActivityModal({
  visible,
  onClose,
  onSuccess,
}: CreateActivityModalProps) {
  const [name, setName] = useState('');

  const handleSubmit = async () => {
    // Submit logic
    onSuccess?.();
    onClose();
  };

  return (
    <Modal visible={visible} onClose={onClose}>
      <View className="bg-background rounded-lg p-6">
        <Text className="text-foreground text-2xl font-bold mb-6">
          Create Activity
        </Text>

        {/* Form fields */}

        <View className="flex-row gap-3 mt-6">
          <Button variant="outline" onPress={onClose} className="flex-1">
            <Text className="text-foreground">Cancel</Text>
          </Button>
          <Button onPress={handleSubmit} className="flex-1">
            <Text className="text-primary-foreground">Create</Text>
          </Button>
        </View>
      </View>
    </Modal>
  );
}
```

### 4. Screen Component
With navigation and data fetching

**Template:**
```tsx
import { View, Text, ScrollView } from 'react-native';
import { Stack } from 'expo-router';
import { trpc } from '@/lib/trpc';
import { useEffect } from 'react';
import { activitySelectionStore } from '@/lib/stores/activitySelectionStore';
import { router } from 'expo-router';

export default function ActivityDetailScreen() {
  const activityId = activitySelectionStore.getState().selected?.id;

  const { data: activity, isLoading } = trpc.activities.getById.useQuery(
    { id: activityId! },
    { enabled: !!activityId }
  );

  useEffect(() => {
    if (!activityId) {
      router.back();
    }

    return () => {
      activitySelectionStore.getState().reset();
    };
  }, [activityId]);

  if (isLoading) {
    return <ActivityDetailSkeleton />;
  }

  if (!activity) {
    return <NotFoundScreen />;
  }

  return (
    <>
      <Stack.Screen
        options={{
          title: activity.name,
        }}
      />
      <ScrollView className="flex-1 bg-background">
        <View className="p-4">
          {/* Activity details */}
        </View>
      </ScrollView>
    </>
  );
}
```

## Styling Patterns

### Every Text Must Be Styled
```tsx
// ❌ WRONG - Text won't have color
<View className="text-foreground">
  <Text>This has no color!</Text>
</View>

// ✅ CORRECT - Direct styling
<View>
  <Text className="text-foreground">This has color!</Text>
</View>
```

### Semantic Colors
```tsx
<View className="bg-background border-border">
  <Text className="text-foreground font-semibold">Title</Text>
  <Text className="text-muted-foreground">Subtitle</Text>
  <Button className="bg-primary">
    <Text className="text-primary-foreground">Action</Text>
  </Button>
</View>
```

### Platform-Specific
```tsx
<View className="ios:pt-12 android:pt-6">
  <Text className="text-foreground">Platform-aware padding</Text>
</View>
```

## Directory Structure

```
components/
├── ui/               # React Native Reusables (Button, Input, etc.)
├── shared/           # Cross-domain shared components
├── activity/         # Activity-specific components
│   ├── ActivityCard.tsx
│   ├── ActivityList.tsx
│   └── __tests__/
├── recording/        # Recording-specific components
└── training-plan/    # Training plan components
```

## Post-Generation

After generating a component:
1. Add to appropriate directory
2. Export from index.ts if needed
3. Update navigation if it's a screen
4. Generate basic tests if requested
5. Verify styling with NativeWind

## Example Invocations

- "Create a card component for displaying route summaries"
- "Generate a list screen for viewing activity plans"
- "Create a modal for editing profile settings"
- "Generate a recording overlay component"

## Critical Patterns

- ✅ Style every `<Text>` component directly
- ✅ Use React Native Reusables from `@/components/ui/`
- ✅ Use `activitySelectionStore` for cross-screen state
- ✅ Add `React.memo` for list items
- ✅ Include accessibility props
- ✅ Use TypeScript strict types
- ✅ Handle loading, error, and empty states
