---
name: angularfire
description: AngularFire library for integrating Firebase services (Authentication, Firestore, Storage, Functions, Analytics) with Angular applications. Use when building Angular apps with Firebase backend, implementing authentication, real-time database, cloud storage, serverless functions, or Firebase analytics. Covers v20+ with standalone components.
license: MIT
---

# AngularFire Integration Skill

## 🎯 Purpose
This skill provides comprehensive guidance on **AngularFire**, the official Angular library for Firebase, including authentication, Firestore database, Cloud Storage, Cloud Functions, and Firebase Analytics integration.

## 📦 What is AngularFire?

AngularFire is the official Angular library for Firebase:
- **Firebase Authentication**: User authentication and authorization
- **Cloud Firestore**: NoSQL real-time database
- **Realtime Database**: Legacy real-time database
- **Cloud Storage**: File storage and serving
- **Cloud Functions**: Serverless backend functions
- **Analytics**: User analytics and tracking
- **RxJS Integration**: Observable-based APIs
- **Angular Standalone Support**: Full support for standalone components

## 🎨 When to Use This Skill

Use AngularFire guidance when:
- Building Angular applications with Firebase backend
- Implementing user authentication (email, Google, social login)
- Working with Firestore real-time database
- Uploading and managing files in Cloud Storage
- Calling Firebase Cloud Functions from Angular
- Tracking analytics events in Angular apps
- Managing Firebase collections with RxJS observables
- Migrating to standalone components with Firebase

## 🛠️ Installation & Setup

### Install AngularFire

```bash
# Install AngularFire and Firebase SDK
pnpm install @angular/fire firebase

# Or using Angular CLI
ng add @angular/fire
```

### Firebase Configuration

```typescript
// src/environments/environment.ts
export const environment = {
  production: false,
  firebase: {
    apiKey: "YOUR_API_KEY",
    authDomain: "your-app.firebaseapp.com",
    projectId: "your-project-id",
    storageBucket: "your-app.appspot.com",
    messagingSenderId: "123456789",
    appId: "1:123456789:web:abcdef",
    measurementId: "G-XXXXXXXXXX"
  }
};
```

### App Configuration (Standalone)

```typescript
// app.config.ts
import { ApplicationConfig } from '@angular/core';
import { provideFirebaseApp, initializeApp } from '@angular/fire/app';
import { provideAuth, getAuth } from '@angular/fire/auth';
import { provideFirestore, getFirestore } from '@angular/fire/firestore';
import { provideStorage, getStorage } from '@angular/fire/storage';
import { provideFunctions, getFunctions } from '@angular/fire/functions';
import { provideAnalytics, getAnalytics } from '@angular/fire/analytics';
import { environment } from './environments/environment';

export const appConfig: ApplicationConfig = {
  providers: [
    provideFirebaseApp(() => initializeApp(environment.firebase)),
    provideAuth(() => getAuth()),
    provideFirestore(() => getFirestore()),
    provideStorage(() => getStorage()),
    provideFunctions(() => getFunctions()),
    provideAnalytics(() => getAnalytics()),
  ]
};
```

## 📚 Core AngularFire Features

### 1. Authentication

**Auth Service:**
```typescript
import { Auth, signInWithEmailAndPassword, createUserWithEmailAndPassword, 
         signOut, user, User } from '@angular/fire/auth';
import { inject } from '@angular/core';

export class AuthService {
  private auth = inject(Auth);
  
  // Observable of current user
  user$ = user(this.auth);
  
  // Email/Password Sign In
  async signIn(email: string, password: string) {
    try {
      const credential = await signInWithEmailAndPassword(
        this.auth, 
        email, 
        password
      );
      return credential.user;
    } catch (error) {
      console.error('Sign in error:', error);
      throw error;
    }
  }
  
  // Create New User
  async signUp(email: string, password: string) {
    try {
      const credential = await createUserWithEmailAndPassword(
        this.auth,
        email,
        password
      );
      return credential.user;
    } catch (error) {
      console.error('Sign up error:', error);
      throw error;
    }
  }
  
  // Sign Out
  async signOut() {
    await signOut(this.auth);
  }
}
```

**Google Sign-In:**
```typescript
import { GoogleAuthProvider, signInWithPopup } from '@angular/fire/auth';

export class AuthService {
  private auth = inject(Auth);
  
  async signInWithGoogle() {
    const provider = new GoogleAuthProvider();
    try {
      const result = await signInWithPopup(this.auth, provider);
      return result.user;
    } catch (error) {
      console.error('Google sign in error:', error);
      throw error;
    }
  }
}
```

**Auth Guard:**
```typescript
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { Auth, user } from '@angular/fire/auth';
import { map } from 'rxjs/operators';

export const authGuard = () => {
  const auth = inject(Auth);
  const router = inject(Router);
  
  return user(auth).pipe(
    map(user => {
      if (user) {
        return true;
      } else {
        router.navigate(['/login']);
        return false;
      }
    })
  );
};

// Usage in routes
const routes: Routes = [
  {
    path: 'dashboard',
    component: DashboardComponent,
    canActivate: [authGuard]
  }
];
```

### 2. Cloud Firestore

**Firestore Service:**
```typescript
import { Firestore, collection, collectionData, doc, docData,
         addDoc, setDoc, updateDoc, deleteDoc, query, where } from '@angular/fire/firestore';
import { inject } from '@angular/core';
import { Observable } from 'rxjs';

export interface Task {
  id?: string;
  title: string;
  completed: boolean;
  createdAt: Date;
  userId: string;
}

export class TasksService {
  private firestore = inject(Firestore);
  private tasksCollection = collection(this.firestore, 'tasks');
  
  // Get all tasks as observable
  getTasks(): Observable<Task[]> {
    return collectionData(this.tasksCollection, { idField: 'id' }) as Observable<Task[]>;
  }
  
  // Get tasks by user
  getUserTasks(userId: string): Observable<Task[]> {
    const userTasksQuery = query(
      this.tasksCollection,
      where('userId', '==', userId)
    );
    return collectionData(userTasksQuery, { idField: 'id' }) as Observable<Task[]>;
  }
  
  // Get single task
  getTask(id: string): Observable<Task> {
    const taskDoc = doc(this.firestore, `tasks/${id}`);
    return docData(taskDoc, { idField: 'id' }) as Observable<Task>;
  }
  
  // Add new task
  async addTask(task: Omit<Task, 'id'>) {
    return await addDoc(this.tasksCollection, {
      ...task,
      createdAt: new Date()
    });
  }
  
  // Update task
  async updateTask(id: string, data: Partial<Task>) {
    const taskDoc = doc(this.firestore, `tasks/${id}`);
    await updateDoc(taskDoc, data);
  }
  
  // Delete task
  async deleteTask(id: string) {
    const taskDoc = doc(this.firestore, `tasks/${id}`);
    await deleteDoc(taskDoc);
  }
}
```

**Advanced Queries:**
```typescript
import { query, where, orderBy, limit, startAfter, getDocs } from '@angular/fire/firestore';

export class TasksService {
  // Complex query with filters and ordering
  async getCompletedTasks() {
    const q = query(
      this.tasksCollection,
      where('completed', '==', true),
      where('userId', '==', this.currentUserId),
      orderBy('createdAt', 'desc'),
      limit(20)
    );
    
    const snapshot = await getDocs(q);
    return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() } as Task));
  }
  
  // Pagination
  async getTasksPage(lastVisible: any) {
    const q = query(
      this.tasksCollection,
      orderBy('createdAt', 'desc'),
      startAfter(lastVisible),
      limit(10)
    );
    
    const snapshot = await getDocs(q);
    return {
      tasks: snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() } as Task)),
      lastDoc: snapshot.docs[snapshot.docs.length - 1]
    };
  }
}
```

**Firestore with Signals:**
```typescript
import { toSignal } from '@angular/core/rxjs-interop';

export class TasksComponent {
  private tasksService = inject(TasksService);
  
  // Convert observable to signal
  tasks = toSignal(this.tasksService.getTasks(), { initialValue: [] });
  
  // Computed signal for filtered tasks
  completedTasks = computed(() => 
    this.tasks().filter(task => task.completed)
  );
}
```

### 3. Cloud Storage

**Storage Service:**
```typescript
import { Storage, ref, uploadBytes, uploadBytesResumable, 
         getDownloadURL, deleteObject, listAll } from '@angular/fire/storage';
import { inject } from '@angular/core';

export class StorageService {
  private storage = inject(Storage);
  
  // Upload file
  async uploadFile(file: File, path: string) {
    const storageRef = ref(this.storage, path);
    const snapshot = await uploadBytes(storageRef, file);
    return await getDownloadURL(snapshot.ref);
  }
  
  // Upload with progress tracking
  uploadFileWithProgress(file: File, path: string) {
    const storageRef = ref(this.storage, path);
    const uploadTask = uploadBytesResumable(storageRef, file);
    
    return new Observable<number>(observer => {
      uploadTask.on('state_changed',
        (snapshot) => {
          const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
          observer.next(progress);
        },
        (error) => observer.error(error),
        async () => {
          const downloadURL = await getDownloadURL(uploadTask.snapshot.ref);
          observer.complete();
        }
      );
    });
  }
  
  // Delete file
  async deleteFile(path: string) {
    const storageRef = ref(this.storage, path);
    await deleteObject(storageRef);
  }
  
  // List files in directory
  async listFiles(path: string) {
    const storageRef = ref(this.storage, path);
    const result = await listAll(storageRef);
    
    return Promise.all(
      result.items.map(async (item) => ({
        name: item.name,
        fullPath: item.fullPath,
        url: await getDownloadURL(item)
      }))
    );
  }
}
```

**File Upload Component:**
```typescript
@Component({
  selector: 'app-file-upload',
  template: `
    <input type="file" (change)="onFileSelected($event)">
    
    @if (uploadProgress() !== null) {
      <mat-progress-bar mode="determinate" [value]="uploadProgress()!">
      </mat-progress-bar>
      <p>{{ uploadProgress() }}% uploaded</p>
    }
    
    @if (downloadURL()) {
      <img [src]="downloadURL()" alt="Uploaded image">
    }
  `
})
export class FileUploadComponent {
  private storageService = inject(StorageService);
  uploadProgress = signal<number | null>(null);
  downloadURL = signal<string | null>(null);
  
  async onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    
    if (!file) return;
    
    const path = `uploads/${Date.now()}_${file.name}`;
    
    this.storageService.uploadFileWithProgress(file, path).subscribe({
      next: (progress) => this.uploadProgress.set(progress),
      error: (error) => console.error('Upload error:', error),
      complete: async () => {
        const url = await this.storageService.getFileURL(path);
        this.downloadURL.set(url);
        this.uploadProgress.set(null);
      }
    });
  }
}
```

### 4. Cloud Functions

**Functions Service:**
```typescript
import { Functions, httpsCallable } from '@angular/fire/functions';
import { inject } from '@angular/core';

export class FunctionsService {
  private functions = inject(Functions);
  
  // Call cloud function
  async sendEmail(data: { to: string; subject: string; body: string }) {
    const sendEmailFn = httpsCallable(this.functions, 'sendEmail');
    const result = await sendEmailFn(data);
    return result.data;
  }
  
  // Call with timeout
  async processPayment(paymentData: any) {
    const processPaymentFn = httpsCallable(
      this.functions, 
      'processPayment',
      { timeout: 60000 } // 60 seconds
    );
    
    try {
      const result = await processPaymentFn(paymentData);
      return result.data;
    } catch (error) {
      console.error('Payment processing error:', error);
      throw error;
    }
  }
}
```

### 5. Analytics

**Analytics Service:**
```typescript
import { Analytics, logEvent, setUserId, setUserProperties } from '@angular/fire/analytics';
import { inject } from '@angular/core';

export class AnalyticsService {
  private analytics = inject(Analytics);
  
  // Log custom event
  logPageView(pageName: string) {
    logEvent(this.analytics, 'page_view', {
      page_name: pageName,
      page_location: window.location.href
    });
  }
  
  // Log button click
  logButtonClick(buttonName: string) {
    logEvent(this.analytics, 'button_click', {
      button_name: buttonName
    });
  }
  
  // Set user ID
  setUser(userId: string) {
    setUserId(this.analytics, userId);
  }
  
  // Set user properties
  setUserProperties(properties: Record<string, any>) {
    setUserProperties(this.analytics, properties);
  }
  
  // Track purchase
  trackPurchase(value: number, currency: string, items: any[]) {
    logEvent(this.analytics, 'purchase', {
      value,
      currency,
      items
    });
  }
}
```

## 🎯 Best Practices

### 1. Use Dependency Injection
```typescript
// ✅ Good - Use inject()
export class MyService {
  private firestore = inject(Firestore);
  private auth = inject(Auth);
}

// ❌ Avoid - Don't import Firebase directly
import { getFirestore } from 'firebase/firestore';
```

### 2. Handle Errors Properly
```typescript
async signIn(email: string, password: string) {
  try {
    return await signInWithEmailAndPassword(this.auth, email, password);
  } catch (error: any) {
    if (error.code === 'auth/user-not-found') {
      throw new Error('User not found');
    } else if (error.code === 'auth/wrong-password') {
      throw new Error('Invalid password');
    }
    throw error;
  }
}
```

### 3. Use Signals with AngularFire
```typescript
// ✅ Good - Convert observables to signals
import { toSignal } from '@angular/core/rxjs-interop';

export class Component {
  user = toSignal(user(this.auth));
  tasks = toSignal(this.tasksService.getTasks(), { initialValue: [] });
}
```

### 4. Security Rules
```javascript
// firestore.rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Tasks belong to users
    match /tasks/{taskId} {
      allow read, write: if request.auth != null && 
                           resource.data.userId == request.auth.uid;
    }
  }
}
```

### 5. Offline Persistence
```typescript
// Enable offline persistence
import { enableIndexedDbPersistence } from '@angular/fire/firestore';

provideFirebaseApp(() => {
  const app = initializeApp(environment.firebase);
  const firestore = getFirestore(app);
  enableIndexedDbPersistence(firestore);
  return app;
});
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Firebase not initialized | Check `provideFirebaseApp()` in app.config.ts |
| Auth errors | Verify Firebase config and enable auth methods in console |
| Firestore permission denied | Check security rules and user authentication |
| Storage upload fails | Verify storage rules and file size limits |
| Functions timeout | Increase timeout or optimize function code |
| Analytics not tracking | Check analytics is enabled in Firebase console |

## 📖 References

- [AngularFire Documentation](https://github.com/angular/angularfire)
- [Firebase Documentation](https://firebase.google.com/docs)
- [Firestore Guide](https://firebase.google.com/docs/firestore)
- [Firebase Auth Guide](https://firebase.google.com/docs/auth)
- [Cloud Storage Guide](https://firebase.google.com/docs/storage)

---

## 📂 Recommended Placement

**Project-level skill:**
```
/.github/skills/angularfire/SKILL.md
```

Copilot will load this when working with Firebase in Angular applications.
