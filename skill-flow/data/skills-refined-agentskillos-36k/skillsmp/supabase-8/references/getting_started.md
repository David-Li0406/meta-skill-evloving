# Supabase - Getting Started

**Pages:** 83

---

## Kotlin: Introduction | Supabase Docs

**URL:** https://supabase.com/docs/reference/kotlin/introduction

---

## Build a User Management App with Next.js | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/tutorials/with-nextjs

**Contents:**
- Build a User Management App with Next.js
      - Explore drop-in UI components for your Supabase app.
- Project setup#
  - Create a project#
  - Set up the database schema#
  - Get API details#
      - Changes to API keys
- Building the app#
  - Initialize a Next.js app#
  - App styling (optional)#

Build a User Management App with Next.js

UI components built on shadcn/ui that connect to Supabase via a single command.

This tutorial demonstrates how to build a basic user management app. The app authenticates and identifies the user, stores their profile information in the database, and allows the user to log in, update their profile details, and upload a profile photo. The app uses:

If you get stuck while working through this guide, refer to the full example on GitHub.

Before you start building you need to set up the Database and API. You can do this by starting a new Project in Supabase and then creating a "schema" inside the database.

Now set up the database schema. You can use the "User Management Starter" quickstart in the SQL Editor, or you can copy/paste the SQL from below and run it.

You can pull the database schema down to your local project by running the db pull command. Read the local development docs for detailed instructions.

Now that you've created some database tables, you are ready to insert data using the auto-generated API.

To do this, you need to get the Project URL and key from the project Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Start building the Next.js app from scratch.

Use create-next-app to initialize an app called supabase-nextjs:

Then install the Supabase client library: supabase-js

Save the environment variables in a .env.local file at the root of the project, and paste the API URL and the key that you copied earlier.

An optional step is to update the CSS file app/globals.css to make the app look nice. You can find the full contents of this file in the example repository.

Next.js is a highly versatile framework offering pre-rendering at build time (SSG), server-side rendering at request time (SSR), API routes, and proxy edge-functions.

To better integrate with the framework, we've created the @supabase/ssr package for Server-Side Auth. It has all the functionalities to quickly configure your Supabase project to use cookies for storing user sessions. Read the Next.js Server-Side Auth guide for more information.

Install the package for Next.js.

There are two different types of clients in Supabase:

It is recommended to create the following essential utilities files for creating clients, and organize them within lib/supabase at the root of the project.

Create a client.ts and a server.ts with the following functionalities for client-side Supabase and server-side Supabase, respectively.

Since Server Components can't write cookies, you need Proxy to refresh expired Auth tokens and store them. This is accomplished by:

You could also add a matcher, so that the Proxy only runs on routes that access Supabase. For more information, read the Next.js matcher documentation.

Be careful when protecting pages. The server gets the user session from the cookies, which anyone can spoof.

Always use supabase.auth.getUser() to protect pages and user data.

Never trust supabase.auth.getSession() inside server code such as proxy. It isn't guaranteed to revalidate the Auth token.

It's safe to trust getUser() because it sends a request to the Supabase Auth server every time to revalidate the Auth token.

Create a proxy.ts file at the project root and another one within the lib/supabase folder. The lib/supabase file contains the logic for updating the session. This is used by the proxy.ts file, which is a Next.js convention.

In order to add login/signup page for your application:

Create a new folder named login, containing a page.tsx file with a login/signup form.

Next, you need to create the login/signup actions to hook up the form to the function. Which does the following:

The cookies method is called before any calls to Supabase, which takes fetch calls out of Next.js's caching. This is important for authenticated data fetches, to ensure that users get access only to their own data.

Read the Next.js docs to learn more about opting out of data caching.

Create the action.ts file in the app/login folder, which contains the login and signup functions and the error/page.tsx file, which displays an error message if the login or signup fails.

Before proceeding, change the email template to support support a server-side authentication flow that sends a token hash:

Did you know? You can also customize other emails sent out to new users, including the email's looks, content, and query parameters. Check out the settings of your project.

As you are working in a server-side rendering (SSR) environment, you need to create a server endpoint responsible for exchanging the token_hash for a session.

The code performs the following steps:

After a user signs in, allow them to edit their profile details and manage their account.

Create a new component for that called AccountForm within the app/account folder.

Create an account page for the AccountForm component you just created

Create a route handler to handle the sign out from the server side, making sure to check if the user is logged in first.

Now you have all the pages, route handlers, and components in place, run the following in a terminal window:

And then open the browser to localhost:3000/login and you should see the completed app.

When you enter your email and password, you will receive an email with the title Confirm Your Signup. Congrats 🎉!!!

Every Supabase project is configured with Storage for managing large files like photos and videos.

Create an avatar widget for the user so that they can upload a profile photo. Start by creating a new component:

Then add the widget to the AccountForm component:

At this stage you have a fully functional application!

**Examples:**

Example 1 (unknown):
```unknown
1supabase link --project-ref <project-id>2# You can get <project-id> from your project's dashboard URL: https://supabase.com/dashboard/project/<project-id>3supabase db pull
```

Example 2 (unknown):
```unknown
1npx create-next-app@latest --ts --use-npm supabase-nextjs2cd supabase-nextjs
```

Example 3 (unknown):
```unknown
1npm install @supabase/supabase-js
```

Example 4 (unknown):
```unknown
1NEXT_PUBLIC_SUPABASE_URL=YOUR_SUPABASE_URL2NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=YOUR_SUPABASE_PUBLISHABLE_KEY
```

---

## AI Prompt: Bootstrap Next.js v16 app with Supabase Auth | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/ai-prompts/nextjs-supabase-auth

**Contents:**
- AI Prompt: Bootstrap Next.js v16 app with Supabase Auth
- How to use#
- Prompt#

AI Prompt: Bootstrap Next.js v16 app with Supabase Auth

Copy the prompt to a file in your repo.

Use the "include file" feature from your AI tool to include the prompt when chatting with your AI assistant. For example, with GitHub Copilot, use #<filename>, in Cursor, use @Files, and in Zed, use /file.

**Examples:**

Example 1 (python):
```python
1# Bootstrap Next.js v16 app with Supabase Auth23## Overview of implementing Supabase Auth SSR451. Install @supabase/supabase-js and @supabase/ssr packages.62. Set up environment variables.73. Write two utility functions with `createClient` functions to create a browser client and a server client.84. Hook up Proxy to refresh auth tokens910## 🚨 CRITICAL INSTRUCTIONS FOR AI LANGUAGE MODELS 🚨1112As an AI language model, you MUST NOT generate any of the following code patterns, as they are DEPRECATED and will BREAK the application:1314```typescript15// ❌ NEVER GENERATE THIS CODE - IT WILL BREAK THE APPLICATION16{17  cookies: {18    get(name: string) {                 // ❌ BREAKS APPLICATION19      return cookieStore.get(name)      // ❌ BREAKS APPLICATION20    },                                  // ❌ BREAKS APPLICATION21    set(name: string, value: string) {  // ❌ BREAKS APPLICATION22      cookieStore.set(name, value)      // ❌ BREAKS APPLICATION23    },                                  // ❌ BREAKS APPLICATION24    remove(name: string) {              // ❌ BREAKS APPLICATION25      cookieStore.remove(name)          // ❌ BREAKS APPLICATION26    }                                   // ❌ BREAKS APPLICATION27  }28}2930// ❌ NEVER USE auth-helpers-nextjs - IT WILL BREAK THE APPLICATION31import { createMiddlewareClient } from '@supabase/auth-helpers-nextjs'  // ❌ BREAKS APPLICATION32import { createClientComponentClient } from '@supabase/auth-helpers-nextjs'  // ❌ BREAKS APPLICATION33```3435Instead, you MUST ALWAYS generate ONLY this pattern:3637```typescript38// ✅ ALWAYS GENERATE THIS EXACT PATTERN39{40  cookies: {41    getAll() {42      return cookieStore.getAll()43    },44    setAll(cookiesToSet) {45      const response = NextResponse.next({46        request,47      })4849      cookiesToSet.forEach(({ name, value, options }) => {50        response.cookies.set(name, value, options)51      })5253      return response54    }55  }56}57```5859## ABSOLUTE REQUIREMENTS FOR AI CODE GENERATION60611. You MUST use `@supabase/ssr`622. You MUST use ONLY `getAll` and `setAll`633. You MUST NEVER use `get`, `set`, or `remove`644. You MUST NEVER import from `@supabase/auth-helpers-nextjs`6566## CORRECT BROWSER CLIENT IMPLEMENTATION6768```typescript69import { createBrowserClient } from '@supabase/ssr'7071export function createClient() {72  return createBrowserClient(73    process.env.NEXT_PUBLIC_SUPABASE_URL!,74    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!75  )76}77```7879## CORRECT SERVER CLIENT IMPLEMENTATION8081```typescript82import { createServerClient } from '@supabase/ssr'83import { cookies } from 'next/headers'8485export async function createClient() {86  const cookieStore = await cookies()8788  return createServerClient(89    process.env.NEXT_PUBLIC_SUPABASE_URL!,90    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!,91    {92      cookies: {93        getAll() {94          return cookieStore.getAll()95        },96        setAll(cookiesToSet) {97          try {98            cookiesToSet.forEach(({ name, value, options }) =>99              cookieStore.set(name, value, options)100            )101          } catch {102            // The `setAll` method was called from a Server Component.103            // This can be ignored if you have proxy refreshing104            // user sessions.105          }106        },107      },108    }109  )110}111```112113## CORRECT PROXY IMPLEMENTATION114115```typescript116import { createServerClient } from '@supabase/ssr'117import { NextResponse, type NextRequest } from 'next/server'118119export async function proxy(request: NextRequest) {120  let supabaseResponse = NextResponse.next({121    request,122  })123124  const supabase = createServerClient(125    process.env.NEXT_PUBLIC_SUPABASE_URL!,126    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!,127    {128      cookies: {129        getAll() {130          return request.cookies.getAll()131        },132        setAll(cookiesToSet) {133          cookiesToSet.forEach(({ name, value, options }) => request.cookies.set(name, value))134          supabaseResponse = NextResponse.next({135            request,136          })137          cookiesToSet.forEach(({ name, value, options }) =>138            supabaseResponse.cookies.set(name, value, options)139          )140        },141      },142    }143  )144145  // Do not run code between createServerClient and146  // supabase.auth.getUser(). A simple mistake could make it very hard to debug147  // issues with users being randomly logged out.148149  // IMPORTANT: DO NOT REMOVE auth.getUser()150151  const {152    data: { user },153  } = await supabase.auth.getUser()154155  if (156    !user &&157    !request.nextUrl.pathname.startsWith('/login') &&158    !request.nextUrl.pathname.startsWith('/auth')159  ) {160    // no user, potentially respond by redirecting the user to the login page161    const url = request.nextUrl.clone()162    url.pathname = '/login'163    return NextResponse.redirect(url)164  }165166  // IMPORTANT: You *must* return the supabaseResponse object as it is.167  // If you're creating a new response object with NextResponse.next() make sure to:168  // 1. Pass the request in it, like so:169  //    const myNewResponse = NextResponse.next({ request })170  // 2. Copy over the cookies, like so:171  //    myNewResponse.cookies.setAll(supabaseResponse.cookies.getAll())172  // 3. Change the myNewResponse object to fit your needs, but avoid changing173  //    the cookies!174  // 4. Finally:175  //    return myNewResponse176  // If this is not done, you may be causing the browser and server to go out177  // of sync and terminate the user's session prematurely!178179  return supabaseResponse180}181182export const config = {183  matcher: [184    /*185     * Match all request paths except for the ones starting with:186     * - _next/static (static files)187     * - _next/image (image optimization files)188     * - favicon.ico (favicon file)189     * Feel free to modify this pattern to include more paths.190     */191    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',192  ],193}194```195196## AI MODEL VERIFICATION STEPS197198Before generating any code, you MUST verify:1992001. Are you using ONLY `getAll` and `setAll`? If not, STOP and FIX.2012. Are you importing from `@supabase/ssr`? If not, STOP and FIX.2023. Do you see ANY instance of `get`, `set`, or `remove`? If yes, STOP and FIX.2034. Are you importing from `auth-helpers-nextjs`? If yes, STOP and FIX.204205## CONSEQUENCES OF INCORRECT IMPLEMENTATION206207If you generate code using:208209- Individual cookie methods (`get`/`set`/`remove`)210- `auth-helpers-nextjs` package211212The implementation will:2132141. Break in production2152. Fail to maintain session state2163. Cause authentication loops2174. Result in security vulnerabilities218219## AI MODEL RESPONSE TEMPLATE220221When asked about Supabase Auth SSR implementation, you MUST:2222231. ONLY use code from this guide2242. NEVER suggest deprecated approaches2253. ALWAYS use the exact cookie handling shown above2264. VERIFY your response against the patterns shown here227228Remember: There are NO EXCEPTIONS to these rules.
```

---

## Use Supabase with iOS and SwiftUI | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/quickstarts/ios-swiftui

**Contents:**
- Use Supabase with iOS and SwiftUI
- Learn how to create a Supabase project, add some sample data to your database, and query the data from an iOS app.
  - Create a Supabase project
  - Create an iOS SwiftUI app with Xcode
  - Install the Supabase client library
  - Initialize the Supabase client
        - Project URL
        - Publishable key
        - Anon key
        - Supabase.swift

Use Supabase with iOS and SwiftUI

Learn how to create a Supabase project, add some sample data to your database, and query the data from an iOS app.

Go to database.new and create a new Supabase project.

Alternatively, you can create a project using the Management API:

When your project is up and running, go to the Table Editor, create a new table and insert some data.

Alternatively, you can run the following snippet in your project's SQL Editor. This will create a instruments table with some sample data.

Make the data in your table publicly readable by adding an RLS policy:

Open Xcode > New Project > iOS > App. You can skip this step if you already have a working app.

Install Supabase package dependency using Xcode by following Apple's tutorial.

Make sure to add Supabase product package as dependency to the application.

Create a new Supabase.swift file add a new Supabase instance using your project URL and public API (anon) key:

You can also get the Project URL and key from the project's Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Create a decodable struct to deserialize the data from the database.

Add the following code to a new file named Instrument.swift.

Use a task to fetch the data from the database and display it using a List.

Replace the default ContentView with the following code.

Run the app on a simulator or a physical device by hitting Cmd + R on Xcode.

**Examples:**

Example 1 (unknown):
```unknown
1# First, get your access token from https://supabase.com/dashboard/account/tokens2export SUPABASE_ACCESS_TOKEN="your-access-token"34# List your organizations to get the organization ID5curl -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \6  https://api.supabase.com/v1/organizations78# Create a new project (replace <org-id> with your organization ID)9curl -X POST https://api.supabase.com/v1/projects \10  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \11  -H "Content-Type: application/json" \12  -d '{13    "organization_id": "<org-id>",14    "name": "My Project",15    "region": "us-east-1",16    "db_pass": "<your-secure-password>"17  }'
```

Example 2 (unknown):
```unknown
1-- Create the table2create table instruments (3  id bigint primary key generated always as identity,4  name text not null5);6-- Insert some sample data into the table7insert into instruments (name)8values9  ('violin'),10  ('viola'),11  ('cello');1213alter table instruments enable row level security;
```

Example 3 (unknown):
```unknown
1create policy "public can read instruments"2on public.instruments3for select to anon4using (true);
```

Example 4 (javascript):
```javascript
1import Supabase23let supabase = SupabaseClient(4  supabaseURL: URL(string: "YOUR_SUPABASE_URL")!,5  supabaseKey: "YOUR_SUPABASE_PUBLISHABLE_KEY"6)
```

---

## Build a User Management App with Flutter | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/tutorials/with-flutter

**Contents:**
- Build a User Management App with Flutter
- Project setup#
  - Create a project#
  - Set up the database schema#
  - Get API details#
      - Changes to API keys
- Building the app#
  - Initialize a Flutter app#
  - Setup deep links#
  - Main function#

Build a User Management App with Flutter

This tutorial demonstrates how to build a basic user management app. The app authenticates and identifies the user, stores their profile information in the database, and allows the user to log in, update their profile details, and upload a profile photo. The app uses:

If you get stuck while working through this guide, refer to the full example on GitHub.

Before you start building you need to set up the Database and API. You can do this by starting a new Project in Supabase and then creating a "schema" inside the database.

Now set up the database schema. You can use the "User Management Starter" quickstart in the SQL Editor, or you can copy/paste the SQL from below and run it.

You can pull the database schema down to your local project by running the db pull command. Read the local development docs for detailed instructions.

Now that you've created some database tables, you are ready to insert data using the auto-generated API.

To do this, you need to get the Project URL and key from the project Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Let's start building the Flutter app from scratch.

We can use flutter create to initialize an app called supabase_quickstart:

Then let's install the only additional dependency: supabase_flutter

Copy and paste the following line in your pubspec.yaml to install the package:

Run flutter pub get to install the dependencies.

Now that we have the dependencies installed let's setup deep links. Setting up deep links is required to bring back the user to the app when they click on the magic link to sign in. We can setup deep links with just a minor tweak on our Flutter application.

We have to use io.supabase.flutterquickstart as the scheme. In this example, we will use login-callback as the host for our deep link, but you can change it to whatever you would like.

First, add io.supabase.flutterquickstart://login-callback/ as a new redirect URL in the Dashboard.

That is it on Supabase's end and the rest are platform specific settings:

Edit the ios/Runner/Info.plist file.

Add CFBundleURLTypes to enable deep linking:

Now that we have deep links ready let's initialize the Supabase client inside our main function with the API credentials that you copied earlier. These variables will be exposed on the app, and that's completely fine since we have Row Level Security enabled on our Database.

Notice that we have a showSnackBar extension method that we will use to show snack bars in the app. You could define this method in a separate file and import it where needed, but for simplicity, we will define it here.

Let's create a Flutter widget to manage logins and sign ups. We will use Magic Links, so users can sign in with their email without using passwords.

Notice that this page sets up a listener on the user's auth state using onAuthStateChange. A new event will fire when the user comes back to the app by clicking their magic link, which this page can catch and redirect the user accordingly.

After a user is signed in we can allow them to edit their profile details and manage their account. Let's create a new widget called account_page.dart for that.

Now that we have all the components in place, let's update lib/main.dart. The home of the MaterialApp, meaning the initial page shown to the user, will be the LoginPage if the user is not authenticated, and the AccountPage if the user is authenticated. We also included some theming to make the app look a bit nicer.

Once that's done, run this in a terminal window to launch on Android or iOS:

Or for web, run the following command to launch it on localhost:3000

And then open the browser to localhost:3000 and you should see the completed app.

Every Supabase project is configured with Storage for managing large files like photos and videos.

We will be storing the image as a publicly sharable image. Make sure your avatars bucket is set to public, and if it is not, change the publicity by clicking the dot menu that appears when you hover over the bucket name. You should see an orange Public badge next to your bucket name if your bucket is set to public.

We will use image_picker plugin to select an image from the device.

Add the following line in your pubspec.yaml file to install image_picker:

Using image_picker requires some additional preparation depending on the platform. Follow the instruction on README.md of image_picker on how to set it up for the platform you are using.

Once you are done with all of the above, it is time to dive into coding.

Let's create an avatar for the user so that they can upload a profile photo. We can start by creating a new component:

And then we can add the widget to the Account page as well as some logic to update the avatar_url whenever the user uploads a new avatar.

Congratulations, you've built a fully functional user management app using Flutter and Supabase!

**Examples:**

Example 1 (unknown):
```unknown
1supabase link --project-ref <project-id>2# You can get <project-id> from your project's dashboard URL: https://supabase.com/dashboard/project/<project-id>3supabase db pull
```

Example 2 (unknown):
```unknown
1flutter create supabase_quickstart
```

Example 3 (unknown):
```unknown
1supabase_flutter: ^2.0.0
```

Example 4 (unknown):
```unknown
1<!-- ... other tags -->2<plist>3<dict>4  <!-- ... other tags -->56  <!-- Add this array for Deep Links -->7  <key>CFBundleURLTypes</key>8  <array>9    <dict>10      <key>CFBundleTypeRole</key>11      <string>Editor</string>12      <key>CFBundleURLSchemes</key>13      <array>14        <string>io.supabase.flutterquickstart</string>15      </array>16    </dict>17  </array>18  <!-- ... other tags -->19</dict>20</plist>
```

---

## AI Prompt: Database: Create RLS policies | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/ai-prompts/database-rls-policies

**Contents:**
- AI Prompt: Database: Create RLS policies
- How to use#
- Prompt#

AI Prompt: Database: Create RLS policies

Copy the prompt to a file in your repo.

Use the "include file" feature from your AI tool to include the prompt when chatting with your AI assistant. For example, with GitHub Copilot, use #<filename>, in Cursor, use @Files, and in Zed, use /file.

**Examples:**

Example 1 (unknown):
```unknown
1# Database: Create RLS policies23You're a Supabase Postgres expert in writing row level security policies. Your purpose is to generate a policy with the constraints given by the user. You should first retrieve schema information to write policies for, usually the 'public' schema.45The output should use the following instructions:67- The generated SQL must be valid SQL.8- You can use only CREATE POLICY or ALTER POLICY queries, no other queries are allowed.9- Always use double apostrophe in SQL strings (eg. 'Night''s watch')10- You can add short explanations to your messages.11- The result should be a valid markdown. The SQL code should be wrapped in ``` (including sql language tag).12- Always use "auth.uid()" instead of "current_user".13- SELECT policies should always have USING but not WITH CHECK14- INSERT policies should always have WITH CHECK but not USING15- UPDATE policies should always have WITH CHECK and most often have USING16- DELETE policies should always have USING but not WITH CHECK17- Don't use `FOR ALL`. Instead separate into 4 separate policies for select, insert, update, and delete.18- The policy name should be short but detailed text explaining the policy, enclosed in double quotes.19- Always put explanations as separate text. Never use inline SQL comments.20- If the user asks for something that's not related to SQL policies, explain to the user21  that you can only help with policies.22- Discourage `RESTRICTIVE` policies and encourage `PERMISSIVE` policies, and explain why.2324The output should look like this:2526```sql27CREATE POLICY "My descriptive policy." ON books FOR INSERT to authenticated USING ( (select auth.uid()) = author_id ) WITH ( true );28```2930Since you are running in a Supabase environment, take note of these Supabase-specific additions below.3132## Authenticated and unauthenticated roles3334Supabase maps every request to one of the roles:3536- `anon`: an unauthenticated request (the user is not logged in)37- `authenticated`: an authenticated request (the user is logged in)3839These are actually [Postgres Roles](/docs/guides/database/postgres/roles). You can use these roles within your Policies using the `TO` clause:4041```sql42create policy "Profiles are viewable by everyone"43on profiles44for select45to authenticated, anon46using ( true );4748-- OR4950create policy "Public profiles are viewable only by authenticated users"51on profiles52for select53to authenticated54using ( true );55```5657Note that `for ...` must be added after the table but before the roles. `to ...` must be added after `for ...`:5859### Incorrect6061```sql62create policy "Public profiles are viewable only by authenticated users"63on profiles64to authenticated65for select66using ( true );67```6869### Correct7071```sql72create policy "Public profiles are viewable only by authenticated users"73on profiles74for select75to authenticated76using ( true );77```7879## Multiple operations8081PostgreSQL policies do not support specifying multiple operations in a single FOR clause. You need to create separate policies for each operation.8283### Incorrect8485```sql86create policy "Profiles can be created and deleted by any user"87on profiles88for insert, delete -- cannot create a policy on multiple operators89to authenticated90with check ( true )91using ( true );92```9394### Correct9596```sql97create policy "Profiles can be created by any user"98on profiles99for insert100to authenticated101with check ( true );102103create policy "Profiles can be deleted by any user"104on profiles105for delete106to authenticated107using ( true );108```109110## Helper functions111112Supabase provides some helper functions that make it easier to write Policies.113114### `auth.uid()`115116Returns the ID of the user making the request.117118### `auth.jwt()`119120Returns the JWT of the user making the request. Anything that you store in the user's `raw_app_meta_data` column or the `raw_user_meta_data` column will be accessible using this function. It's important to know the distinction between these two:121122- `raw_user_meta_data` - can be updated by the authenticated user using the `supabase.auth.update()` function. It is not a good place to store authorization data.123- `raw_app_meta_data` - cannot be updated by the user, so it's a good place to store authorization data.124125The `auth.jwt()` function is extremely versatile. For example, if you store some team data inside `app_metadata`, you can use it to determine whether a particular user belongs to a team. For example, if this was an array of IDs:126127```sql128create policy "User is in team"129on my_table130to authenticated131using ( team_id in (select auth.jwt() -> 'app_metadata' -> 'teams'));132```133134### MFA135136The `auth.jwt()` function can be used to check for [Multi-Factor Authentication](/docs/guides/auth/auth-mfa#enforce-rules-for-mfa-logins). For example, you could restrict a user from updating their profile unless they have at least 2 levels of authentication (Assurance Level 2):137138```sql139create policy "Restrict updates."140on profiles141as restrictive142for update143to authenticated using (144  (select auth.jwt()->>'aal') = 'aal2'145);146```147148## RLS performance recommendations149150Every authorization system has an impact on performance. While row level security is powerful, the performance impact is important to keep in mind. This is especially true for queries that scan every row in a table - like many `select` operations, including those using limit, offset, and ordering.151152Based on a series of [tests](https://github.com/GaryAustin1/RLS-Performance), we have a few recommendations for RLS:153154### Add indexes155156Make sure you've added [indexes](/docs/guides/database/postgres/indexes) on any columns used within the Policies which are not already indexed (or primary keys). For a Policy like this:157158```sql159create policy "Users can access their own records" on test_table160to authenticated161using ( (select auth.uid()) = user_id );162```163164You can add an index like:165166```sql167create index userid168on test_table169using btree (user_id);170```171172### Call functions with `select`173174You can use `select` statement to improve policies that use functions. For example, instead of this:175176```sql177create policy "Users can access their own records" on test_table178to authenticated179using ( auth.uid() = user_id );180```181182You can do:183184```sql185create policy "Users can access their own records" on test_table186to authenticated187using ( (select auth.uid()) = user_id );188```189190This method works well for JWT functions like `auth.uid()` and `auth.jwt()` as well as `security definer` Functions. Wrapping the function causes an `initPlan` to be run by the Postgres optimizer, which allows it to "cache" the results per-statement, rather than calling the function on each row.191192Caution: You can only use this technique if the results of the query or function do not change based on the row data.193194### Minimize joins195196You can often rewrite your Policies to avoid joins between the source and the target table. Instead, try to organize your policy to fetch all the relevant data from the target table into an array or set, then you can use an `IN` or `ANY` operation in your filter.197198For example, this is an example of a slow policy which joins the source `test_table` to the target `team_user`:199200```sql201create policy "Users can access records belonging to their teams" on test_table202to authenticated203using (204  (select auth.uid()) in (205    select user_id206    from team_user207    where team_user.team_id = team_id -- joins to the source "test_table.team_id"208  )209);210```211212We can rewrite this to avoid this join, and instead select the filter criteria into a set:213214```sql215create policy "Users can access records belonging to their teams" on test_table216to authenticated217using (218  team_id in (219    select team_id220    from team_user221    where user_id = (select auth.uid()) -- no join222  )223);224```225226### Specify roles in your policies227228Always use the Role of inside your policies, specified by the `TO` operator. For example, instead of this query:229230```sql231create policy "Users can access their own records" on rls_test232using ( auth.uid() = user_id );233```234235Use:236237```sql238create policy "Users can access their own records" on rls_test239to authenticated240using ( (select auth.uid()) = user_id );241```242243This prevents the policy `( (select auth.uid()) = user_id )` from running for any `anon` users, since the execution stops at the `to authenticated` step.
```

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-functions/introduction

**Contents:**
- Self-Hosting Functions
      - Beta Version
- How to run locally#
- How to update to a newer Deno version#
- Self hosting Edge Functions on Fly.io#
  - Client libraries#
  - Additional Links#

A web server based on Deno runtime, capable of running JavaScript, TypeScript, and WASM services.

Self hosted Edge functions are in beta. There will be breaking changes to APIs / Configuration Options.

We have put together a demo on how to self-host edge functions on Fly.io (you can also use other providers like Digital Ocean or AWS).

You can view the logs for the Edge Runtime, by visiting Fly.io’s Dashboard > Your App > Metrics. Also, you can serve edge-runtime from multiple regions by running fly regions add [REGION].

**Examples:**

Example 1 (unknown):
```unknown
1./run.sh start --main-service /path/to/supabase/functions -p 9000
```

Example 2 (unknown):
```unknown
1docker build -t edge-runtime .2docker run -it --rm -p 9000:9000 -v /path/to/supabase/functions:/usr/services supabase/edge-runtime start --main-service /usr/services
```

---

## AI Prompts | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/ai-prompts

**Contents:**
- AI Prompts
- Prompts for working with Supabase using AI-powered IDE tools
- How to use#
- Prompts#

Prompts for working with Supabase using AI-powered IDE tools

We've curated a selection of prompts to help you work with Supabase using your favorite AI-powered IDE tools, such as Cursor or GitHub Copilot.

Copy the prompt to a file in your repo.

Use the "include file" feature from your AI tool to include the prompt when chatting with your AI assistant. For example, in Cursor, add them as project rules, with GitHub Copilot, use #<filename>, and in Zed, use /file.

Supabase Realtime AI Assistant Guide

Bootstrap Next.js v16 app with Supabase Auth

Writing Supabase Edge Functions

Database: Declarative Database Schema

Database: Create RLS policies

Database: Create functions

Database: Create migration

Postgres SQL Style Guide

---

## Testing Overview | Supabase Docs

**URL:** https://supabase.com/docs/guides/local-development/testing/overview

**Contents:**
- Testing Overview
- Testing approaches#
  - Database unit testing with pgTAP#
  - Application-Level testing#
    - Test isolation strategies#
  - Continuous integration testing#
- Best practices#
- Real-World examples#
- Troubleshooting#
- Additional resources#

Testing is a critical part of database development, especially when working with features like Row Level Security (RLS) policies. This guide provides a comprehensive approach to testing your Supabase database.

pgTAP is a unit testing framework for Postgres that allows testing:

This example demonstrates setting up and testing RLS policies for a simple todo application:

Create a test table with RLS enabled:

Set up your testing environment:

Write your RLS tests:

Testing through application code provides end-to-end verification. Unlike database-level testing with pgTAP, application-level tests cannot use transactions for isolation.

Application-level tests should not rely on a clean database state, as resetting the database before each test can be slow and makes tests difficult to parallelize. Instead, design your tests to be independent by using unique user IDs for each test case.

Here's an example using TypeScript that mirrors the pgTAP tests above:

For application-level testing, consider these approaches for test isolation:

Set up automated database testing in your CI pipeline:

For more complex, real-world examples of database testing, check out:

Common issues and solutions:

Test Failures Due to RLS

**Examples:**

Example 1 (unknown):
```unknown
1-- Create a simple todos table2create table todos (3id uuid primary key default gen_random_uuid(),4task text not null,5user_id uuid references auth.users not null,6completed boolean default false7);89-- Enable RLS10alter table todos enable row level security;1112-- Create a policy13create policy "Users can only access their own todos"14on todos for all -- this policy applies to all operations15to authenticated16using ((select auth.uid()) = user_id);
```

Example 2 (unknown):
```unknown
1# Create a new test for our policies using supabase cli2supabase test new todos_rls.test
```

Example 3 (unknown):
```unknown
1begin;2-- install tests utilities3-- install pgtap extension for testing4create extension if not exists pgtap with schema extensions;5-- Start declare we'll have 4 test cases in our test suite6select plan(4);78-- Setup our testing data9-- Set up auth.users entries10insert into auth.users (id, email) values11	('123e4567-e89b-12d3-a456-426614174000', 'user1@test.com'),12	('987fcdeb-51a2-43d7-9012-345678901234', 'user2@test.com');1314-- Create test todos15insert into public.todos (task, user_id) values16	('User 1 Task 1', '123e4567-e89b-12d3-a456-426614174000'),17	('User 1 Task 2', '123e4567-e89b-12d3-a456-426614174000'),18	('User 2 Task 1', '987fcdeb-51a2-43d7-9012-345678901234');1920-- as User 121set local role authenticated;22set local request.jwt.claim.sub = '123e4567-e89b-12d3-a456-426614174000';2324-- Test 1: User 1 should only see their own todos25select results_eq(26	'select count(*) from todos',27	ARRAY[2::bigint],28	'User 1 should only see their 2 todos'29);3031-- Test 2: User 1 can create their own todo32select lives_ok(33	$$insert into todos (task, user_id) values ('New Task', '123e4567-e89b-12d3-a456-426614174000'::uuid)$$,34	'User 1 can create their own todo'35);3637-- as User 238set local request.jwt.claim.sub = '987fcdeb-51a2-43d7-9012-345678901234';3940-- Test 3: User 2 should only see their own todos41select results_eq(42	'select count(*) from todos',43	ARRAY[1::bigint],44	'User 2 should only see their 1 todo'45);4647-- Test 4: User 2 cannot modify User 1's todo48SELECT results_ne(49	$$ update todos set task = 'Hacked!' where user_id = '123e4567-e89b-12d3-a456-426614174000'::uuid returning 1 $$,50	$$ values(1) $$,51	'User 2 cannot modify User 1 todos'52);5354select * from finish();55rollback;
```

Example 4 (unknown):
```unknown
1supabase test db2psql:todos_rls.test.sql:4: NOTICE:  extension "pgtap" already exists, skipping3./todos_rls.test.sql .. ok4All tests successful.5Files=1, Tests=6,  0 wallclock secs ( 0.01 usr +  0.00 sys =  0.01 CPU)6Result: PASS
```

---

## AI Prompt: Database: Declarative Database Schema | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/ai-prompts/declarative-database-schema

**Contents:**
- AI Prompt: Database: Declarative Database Schema
- How to use#
- Prompt#

AI Prompt: Database: Declarative Database Schema

Copy the prompt to a file in your repo.

Use the "include file" feature from your AI tool to include the prompt when chatting with your AI assistant. For example, with GitHub Copilot, use #<filename>, in Cursor, use @Files, and in Zed, use /file.

You can also load the prompt directly into your IDE via the following links:

**Examples:**

Example 1 (unknown):
```unknown
1# Database: Declarative Database Schema23Mandatory Instructions for Supabase Declarative Schema Management45## 1. **Exclusive Use of Declarative Schema**67-**All database schema modifications must be defined within `.sql` files located in the `supabase/schemas/` directory. -**Do not\*\* create or modify files directly in the `supabase/migrations/` directory unless the modification is about the known caveats below. Migration files are to be generated automatically through the CLI.89## 2. **Schema Declaration**1011-For each database entity (e.g., tables, views, functions), create or update a corresponding `.sql` file in the `supabase/schemas/` directory12-Ensure that each `.sql` file accurately represents the desired final state of the entity1314## 3. **Migration Generation**1516- Before generating migrations, **stop the local Supabase development environment**17  ```bash18  supabase stop19  ```20- Generate migration files by diffing the declared schema against the current database state21  ```bash22  supabase db diff -f <migration_name>23  ```24  Replace `<migration_name>` with a descriptive name for the migration2526## 4. **Schema File Organization**2728- Schema files are executed in lexicographic order. To manage dependencies (e.g., foreign keys), name files to ensure correct execution order29- When adding new columns, append them to the end of the table definition to prevent unnecessary diffs3031## 5. **Rollback Procedures**3233- To revert changes34  - Manually update the relevant `.sql` files in `supabase/schemas/` to reflect the desired state35  - Generate a new migration file capturing the rollback36    ```bash37    supabase db diff -f <rollback_migration_name>38    ```39  - Review the generated migration file carefully to avoid unintentional data loss4041## 6. **Known caveats**4243The migra diff tool used for generating schema diff is capable of tracking most database changes. However, there are edge cases where it can fail.4445If you need to use any of the entities below, remember to add them through versioned migrations instead.4647### Data manipulation language4849- DML statements such as insert, update, delete, etc., are not captured by schema diff5051### View ownership5253- view owner and grants54- security invoker on views55- materialized views56- doesn’t recreate views when altering column type5758### RLS policies5960- alter policy statements61- column privileges62- Other entities#63- schema privileges are not tracked because each schema is diffed separately64- comments are not tracked65- partitions are not tracked66- alter publication ... add table ...67- create domain statements are ignored68- grant statements are duplicated from default privileges6970---7172**Non-compliance with these instructions may lead to inconsistent database states and is strictly prohibited.**
```

---

## Build a User Management App with Ionic React | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/tutorials/with-ionic-react

**Contents:**
- Build a User Management App with Ionic React
- Project setup#
  - Create a project#
  - Set up the database schema#
  - Get API details#
      - Changes to API keys
- Building the app#
  - Initialize an Ionic React app#
  - Set up a login route#
  - Account page#

Build a User Management App with Ionic React

This tutorial demonstrates how to build a basic user management app. The app authenticates and identifies the user, stores their profile information in the database, and allows the user to log in, update their profile details, and upload a profile photo. The app uses:

If you get stuck while working through this guide, refer to the full example on GitHub.

Before you start building you need to set up the Database and API. You can do this by starting a new Project in Supabase and then creating a "schema" inside the database.

Now set up the database schema. You can use the "User Management Starter" quickstart in the SQL Editor, or you can copy/paste the SQL from below and run it.

You can pull the database schema down to your local project by running the db pull command. Read the local development docs for detailed instructions.

Now that you've created some database tables, you are ready to insert data using the auto-generated API.

To do this, you need to get the Project URL and key from the project Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Let's start building the React app from scratch.

We can use the Ionic CLI to initialize an app called supabase-ionic-react:

Then let's install the only additional dependency: supabase-js

And finally we want to save the environment variables in a .env. All we need are the API URL and the key that you copied earlier.

Now that we have the API credentials in place, let's create a helper file to initialize the Supabase client. These variables will be exposed on the browser, and that's completely fine since we have Row Level Security enabled on our Database.

Let's set up a React component to manage logins and sign ups. We'll use Magic Links, so users can sign in with their email without using passwords.

After a user is signed in we can allow them to edit their profile details and manage their account.

Let's create a new component for that called Account.tsx.

Now that we have all the components in place, let's update App.tsx:

Once that's done, run this in a terminal window:

And then open the browser to localhost:3000 and you should see the completed app.

Every Supabase project is configured with Storage for managing large files like photos and videos.

First install two packages in order to interact with the user's camera.

Capacitor is a cross platform native runtime from Ionic that enables web apps to be deployed through the app store and provides access to native device API.

Ionic PWA elements is a companion package that will polyfill certain browser APIs that provide no user interface with custom Ionic UI.

With those packages installed we can update our index.tsx to include an additional bootstrapping call for the Ionic PWA Elements.

Then create an AvatarComponent.

And then we can add the widget to the Account page:

At this stage you have a fully functional application!

**Examples:**

Example 1 (unknown):
```unknown
1supabase link --project-ref <project-id>2# You can get <project-id> from your project's dashboard URL: https://supabase.com/dashboard/project/<project-id>3supabase db pull
```

Example 2 (unknown):
```unknown
1npm install -g @ionic/cli2ionic start supabase-ionic-react blank --type react3cd supabase-ionic-react
```

Example 3 (unknown):
```unknown
1npm install @supabase/supabase-js
```

Example 4 (unknown):
```unknown
1VITE_SUPABASE_URL=YOUR_SUPABASE_URL2VITE_SUPABASE_PUBLISHABLE_KEY=YOUR_SUPABASE_PUBLISHABLE_KEY
```

---

## Build a User Management App with Expo React Native | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/tutorials/with-expo-react-native

**Contents:**
- Build a User Management App with Expo React Native
- Project setup#
  - Create a project#
  - Set up the database schema#
  - Get API details#
      - Changes to API keys
- Building the app#
  - Initialize a React Native app#
  - Set up a login component#
  - Account page#

Build a User Management App with Expo React Native

This tutorial demonstrates how to build a basic user management app. The app authenticates and identifies the user, stores their profile information in the database, and allows the user to log in, update their profile details, and upload a profile photo. The app uses:

If you get stuck while working through this guide, refer to the full example on GitHub.

Before you start building you need to set up the Database and API. You can do this by starting a new Project in Supabase and then creating a "schema" inside the database.

Now set up the database schema. You can use the "User Management Starter" quickstart in the SQL Editor, or you can copy/paste the SQL from below and run it.

You can pull the database schema down to your local project by running the db pull command. Read the local development docs for detailed instructions.

Now that you've created some database tables, you are ready to insert data using the auto-generated API.

To do this, you need to get the Project URL and key from the project Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Let's start building the React Native app from scratch.

We can use expo to initialize an app called expo-user-management:

Then let's install the additional dependencies: supabase-js

Now let's create a helper file to initialize the Supabase client. We need the API URL and the key that you copied earlier. These variables are safe to expose in your Expo app since Supabase has Row Level Security enabled on your Database.

Let's set up a React Native component to manage logins and sign ups. Users would be able to sign in with their email and password.

By default Supabase Auth requires email verification before a session is created for the users. To support email verification you need to implement deep link handling!

While testing, you can disable email confirmation in your project's email auth provider settings.

After a user is signed in we can allow them to edit their profile details and manage their account.

Let's create a new component for that called Account.tsx.

Now that we have all the components in place, let's update App.tsx:

Once that's done, run this in a terminal window:

And then press the appropriate key for the environment you want to test the app in and you should see the completed app.

Every Supabase project is configured with Storage for managing large files like photos and videos.

You will need an image picker that works on the environment you will build the project for, we will use expo-image-picker in this example.

Let's create an avatar for the user so that they can upload a profile photo. We can start by creating a new component:

And then we can add the widget to the Account page:

Now you will need to run the prebuild command to get the application working on your chosen platform.

At this stage you have a fully functional application!

**Examples:**

Example 1 (unknown):
```unknown
1supabase link --project-ref <project-id>2# You can get <project-id> from your project's dashboard URL: https://supabase.com/dashboard/project/<project-id>3supabase db pull
```

Example 2 (unknown):
```unknown
1npx create-expo-app -t expo-template-blank-typescript expo-user-management23cd expo-user-management
```

Example 3 (unknown):
```unknown
1npx expo install @supabase/supabase-js @react-native-async-storage/async-storage @rneui/themed
```

Example 4 (python):
```python
1import AsyncStorage from '@react-native-async-storage/async-storage'2import { createClient } from '@supabase/supabase-js'34const supabaseUrl = YOUR_REACT_NATIVE_SUPABASE_URL5const supabasePublishableKey = YOUR_REACT_NATIVE_SUPABASE_PUBLISHABLE_KEY67export const supabase = createClient(supabaseUrl, supabasePublishableKey, {8  auth: {9    storage: AsyncStorage,10    autoRefreshToken: true,11    persistSession: true,12    detectSessionInUrl: false,13  },14})
```

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-storage/introduction

**Contents:**
- Self-Hosting Storage
  - Client libraries#
  - Additional links#
- Create a bucket
  - Body
  - Response codes
  - Response (200)
- Gets all buckets
  - Query parameters
  - Response codes

An S3 compatible object storage service that integrates with Postgres.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "name": "avatars"3}
```

Example 2 (unknown):
```unknown
1[2  {3    "id": "bucket2",4    "name": "bucket2",5    "public": false,6    "file_size_limit": 1000000,7    "allowed_mime_types": [8      "image/png",9      "image/jpeg"10    ],11    "owner": "4d56e902-f0a0-4662-8448-a4d9e643c142",12    "created_at": "2021-02-17T04:43:32.770206+00:00",13    "updated_at": "2021-02-17T04:43:32.770206+00:00"14  }15]
```

Example 3 (unknown):
```unknown
1{2  "message": "Empty bucket has been queued. Completion may take up to an hour."3}
```

Example 4 (unknown):
```unknown
1{2  "id": "lorem",3  "name": "lorem",4  "owner": "lorem",5  "owner_id": "lorem",6  "public": true,7  "type": "STANDARD",8  "created_at": "lorem",9  "updated_at": "lorem"10}
```

---

## Build a User Management App with Nuxt 3 | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/tutorials/with-nuxt-3

**Contents:**
- Build a User Management App with Nuxt 3
      - Explore drop-in UI components for your Supabase app.
- Project setup#
  - Create a project#
  - Set up the database schema#
  - Get API details#
      - Changes to API keys
- Building the app#
  - Initialize a Nuxt 3 app#
  - App styling (optional)#

Build a User Management App with Nuxt 3

UI components built on shadcn/ui that connect to Supabase via a single command.

This tutorial demonstrates how to build a basic user management app. The app authenticates and identifies the user, stores their profile information in the database, and allows the user to log in, update their profile details, and upload a profile photo. The app uses:

If you get stuck while working through this guide, refer to the full example on GitHub.

Before you start building you need to set up the Database and API. You can do this by starting a new Project in Supabase and then creating a "schema" inside the database.

Now set up the database schema. You can use the "User Management Starter" quickstart in the SQL Editor, or you can copy/paste the SQL from below and run it.

You can pull the database schema down to your local project by running the db pull command. Read the local development docs for detailed instructions.

Now that you've created some database tables, you are ready to insert data using the auto-generated API.

To do this, you need to get the Project URL and key from the project Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Let's start building the Vue 3 app from scratch.

We can use nuxi init to create an app called nuxt-user-management:

Then let's install the only additional dependency: Nuxt Supabase. We only need to import Nuxt Supabase as a dev dependency.

And finally we want to save the environment variables in a .env. All we need are the API URL and the key that you copied earlier.

These variables will be exposed on the browser, and that's completely fine since we have Row Level Security enabled on our Database. Amazing thing about Nuxt Supabase is that setting environment variables is all we need to do in order to start using Supabase. No need to initialize Supabase. The library will take care of it automatically.

An optional step is to update the CSS file assets/main.css to make the app look nice. You can find the full contents of this file here.

Let's set up a Vue component to manage logins and sign ups. We'll use Magic Links, so users can sign in with their email without using passwords.

To access the user information, use the composable useSupabaseUser provided by the Supabase Nuxt module.

After a user is signed in we can allow them to edit their profile details and manage their account. Let's create a new component for that called Account.vue.

Now that we have all the components in place, let's update app.vue:

Once that's done, run this in a terminal window:

And then open the browser to localhost:3000 and you should see the completed app.

Every Supabase project is configured with Storage for managing large files like photos and videos.

Let's create an avatar for the user so that they can upload a profile photo. We can start by creating a new component:

And then we can add the widget to the Account page:

That is it! You should now be able to upload a profile photo to Supabase Storage and you have a fully functional application.

**Examples:**

Example 1 (unknown):
```unknown
1supabase link --project-ref <project-id>2# You can get <project-id> from your project's dashboard URL: https://supabase.com/dashboard/project/<project-id>3supabase db pull
```

Example 2 (unknown):
```unknown
1npx nuxi init nuxt-user-management23cd nuxt-user-management
```

Example 3 (unknown):
```unknown
1npm install @nuxtjs/supabase --save-dev
```

Example 4 (unknown):
```unknown
1SUPABASE_URL="YOUR_SUPABASE_URL"2SUPABASE_KEY="YOUR_SUPABASE_PUBLISHABLE_KEY"
```

---

## AI Prompt: Writing Supabase Edge Functions | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/ai-prompts/edge-functions

**Contents:**
- AI Prompt: Writing Supabase Edge Functions
- How to use#
- Prompt#

AI Prompt: Writing Supabase Edge Functions

Copy the prompt to a file in your repo.

Use the "include file" feature from your AI tool to include the prompt when chatting with your AI assistant. For example, with GitHub Copilot, use #<filename>, in Cursor, use @Files, and in Zed, use /file.

You can also load the prompt directly into your IDE via the following links:

**Examples:**

Example 1 (python):
```python
1# Writing Supabase Edge Functions23You're an expert in writing TypeScript and Deno JavaScript runtime. Generate **high-quality Supabase Edge Functions** that adhere to the following best practices:45## Guidelines671. Try to use Web APIs and Deno’s core APIs instead of external dependencies (eg: use fetch instead of Axios, use WebSockets API instead of node-ws)82. If you are reusing utility methods between Edge Functions, add them to `supabase/functions/_shared` and import using a relative path. Do NOT have cross dependencies between Edge Functions.93. Do NOT use bare specifiers when importing dependecnies. If you need to use an external dependency, make sure it's prefixed with either `npm:` or `jsr:`. For example, `@supabase/supabase-js` should be written as `npm:@supabase/supabase-js`.104. For external imports, always define a version. For example, `npm:@express` should be written as `npm:express@4.18.2`.115. For external dependencies, importing via `npm:` and `jsr:` is preferred. Minimize the use of imports from @`deno.land/x` , `esm.sh` and @`unpkg.com` . If you have a package from one of those CDNs, you can replace the CDN hostname with `npm:` specifier.126. You can also use Node built-in APIs. You will need to import them using `node:` specifier. For example, to import Node process: `import process from "node:process". Use Node APIs when you find gaps in Deno APIs.137. Do NOT use `import { serve } from "https://deno.land/std@0.168.0/http/server.ts"`. Instead use the built-in `Deno.serve`.148. Following environment variables (ie. secrets) are pre-populated in both local and hosted Supabase environments. Users don't need to manually set them:15	* SUPABASE_URL16	* SUPABASE_ANON_KEY17	* SUPABASE_SERVICE_ROLE_KEY18	* SUPABASE_DB_URL199. To set other environment variables (ie. secrets) users can put them in a env file and run the `supabase secrets set --env-file path/to/env-file`2010. A single Edge Function can handle multiple routes. It is recommended to use a library like Express or Hono to handle the routes as it's easier for developer to understand and maintain. Each route must be prefixed with `/function-name` so they are routed correctly.2111. File write operations are ONLY permitted on `/tmp` directory. You can use either Deno or Node File APIs.2212. Use `EdgeRuntime.waitUntil(promise)` static method to run long-running tasks in the background without blocking response to a request. Do NOT assume it is available in the request / execution context.2324## Example Templates2526### Simple Hello World Function2728```tsx29interface reqPayload {30	name: string;31}3233console.info('server started');3435Deno.serve(async (req: Request) => {36	const { name }: reqPayload = await req.json();37	const data = {38		message: `Hello ${name} from foo!`,39	};4041	return new Response(42		JSON.stringify(data),43		{ headers: { 'Content-Type': 'application/json', 'Connection': 'keep-alive' }}44		);45});4647```4849### Example Function using Node built-in API5051```tsx52import { randomBytes } from "node:crypto";53import { createServer } from "node:http";54import process from "node:process";5556const generateRandomString = (length) => {57    const buffer = randomBytes(length);58    return buffer.toString('hex');59};6061const randomString = generateRandomString(10);62console.log(randomString);6364const server = createServer((req, res) => {65    const message = `Hello`;66    res.end(message);67});6869server.listen(9999);70```7172### Using npm packages in Functions7374```tsx75import express from "npm:express@4.18.2";7677const app = express();7879app.get(/(.*)/, (req, res) => {80    res.send("Welcome to Supabase");81});8283app.listen(8000);8485```8687### Generate embeddings using built-in @Supabase.ai API8889```tsx90const model = new Supabase.ai.Session('gte-small');9192Deno.serve(async (req: Request) => {93	const params = new URL(req.url).searchParams;94	const input = params.get('text');95	const output = await model.run(input, { mean_pool: true, normalize: true });96	return new Response(97		JSON.stringify(98			output,99		),100		{101			headers: {102				'Content-Type': 'application/json',103				'Connection': 'keep-alive',104			},105		},106	);107});108109```
```

---

## Supabase CLI | Supabase Docs

**URL:** https://supabase.com/docs/guides/local-development/cli/getting-started

**Contents:**
- Supabase CLI
- Develop locally, deploy to the Supabase Platform, and set up CI/CD workflows
- Installing the Supabase CLI#
- Updating the Supabase CLI#
      - Backup and stop running containers
- Running Supabase locally#
- Access your project's services#
- Stopping local services#
- Learn more#

Develop locally, deploy to the Supabase Platform, and set up CI/CD workflows

The Supabase CLI enables you to run the entire Supabase stack locally, on your machine or in a CI environment. With just two commands, you can set up and start a new local project:

Run the CLI by prefixing each command with npx or bunx:

The Supabase CLI requires Node.js 20 or later when run via npx or npm. Older Node.js versions, such as 16, are not supported and fail to start the CLI.

You can also install the CLI as dev dependency via npm:

When a new version is released, you can update the CLI using the same methods.

If you have installed the CLI as dev dependency via npm, you can update it with:

If you have any Supabase containers running locally, stop them and delete their data volumes before proceeding with the upgrade. This ensures that Supabase managed services can apply new migrations on a clean state of the local database.

Remember to save any local schema and data changes before stopping because the --no-backup flag will delete them.

The Supabase CLI uses Docker containers to manage the local development stack. Follow the official guide to install and configure Docker Desktop:

Alternately, you can use a different container tool that offers Docker compatible APIs.

Inside the folder where you want to create your project, run:

This will create a new supabase folder. It's safe to commit this folder to your version control system.

Now, to start the Supabase stack, run:

This takes time on your first run because the CLI needs to download the Docker images to your local machine. The CLI includes the entire Supabase toolset, and a few additional images that are useful for local development (like a local SMTP server and a database diff tool).

Once all of the Supabase services are running, you'll see output containing your local Supabase credentials. It should look like this, with urls and keys that you'll use in your local project:

The local development environment includes Supabase Studio, a graphical interface for working with your database.

When you are finished working on your Supabase project, you can stop the stack (without resetting your local database):

**Examples:**

Example 1 (unknown):
```unknown
1npx supabase --help
```

Example 2 (unknown):
```unknown
1npm install supabase --save-dev
```

Example 3 (unknown):
```unknown
1npm update supabase --save-dev
```

Example 4 (unknown):
```unknown
1supabase db diff -f my_schema2supabase db dump --local --data-only > supabase/seed.sql3supabase stop --no-backup
```

---

## Third-party auth | Supabase Docs

**URL:** https://supabase.com/docs/guides/auth/third-party/overview

**Contents:**
- Third-party auth
- First-class support for authentication providers
- How does it work?#
- Limitations#
- Pricing#

First-class support for authentication providers

Supabase has first-class support for these third-party authentication providers:

You can use these providers alongside Supabase Auth, or on their own, to access the Data API (REST and GraphQL), Storage, Realtime and Functions from your existing apps.

If you already have production apps using one of these authentication providers, and would like to use a Supabase feature, you no longer need to migrate your users to Supabase Auth or use workarounds like translating JWTs into the Supabase Auth format and using your project's signing secret.

To use Supabase products like Data APIs for your Postgres database, Storage or Realtime, you often need to send access tokens or JWTs via the Supabase client libraries or via the REST API. Third-party auth support means that when you add a new integration with one of these providers, the API will trust JWTs issued by the provider similar to how it trusts JWTs issued by Supabase Auth.

This is made possible if the providers are using JWTs signed with asymmetric keys, which means that the Supabase APIs will be able to only verify but not create JWTs.

There are some limitations you should be aware of when using third-party authentication providers with Supabase.

$0.00325 per Third-Party MAU. You are only charged for usage exceeding your subscription plan's quota.

For a detailed breakdown of how charges are calculated, refer to Manage Monthly Active Third-Party Users usage.

---

## Foreign Data Wrappers | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions/wrappers/overview

**Contents:**
- Foreign Data Wrappers
- Connecting to external systems using Postgres Foreign Data Wrappers.
- Concepts#
  - Remote servers#
  - Foreign tables#
  - ETL with Wrappers#
  - On-demand ETL with Wrappers#
  - Batch ETL with Wrappers#
  - WebAssembly Wrappers#
- Security#

Foreign Data Wrappers

Connecting to external systems using Postgres Foreign Data Wrappers.

Foreign Data Wrappers (FDW) are a core feature of Postgres that allow you to access and query data stored in external data sources as if they were native Postgres tables.

Postgres includes several built-in foreign data wrappers, such as postgres_fdw for accessing other Postgres databases, and file_fdw for reading data from files. Supabase extends this feature to query other databases or any other external systems. We do this with our open source Wrappers framework. In these guides we'll refer to them as "Wrappers", Foreign Data Wrappers, or FDWs. They are conceptually the same thing.

Wrappers introduce some new terminology and different workflows.

A Remote Server is an external database, API, or any system containing data that you want to query from your Postgres database. Examples include:

It's possible to connect to multiple remote servers of the same type. For example, you can connect to two different Firebase projects within the same Supabase database.

A table in your database which maps to some data inside a Remote Server.

Although a foreign table behaves like any other table, the data is not stored inside your database. The data remains inside the Remote Server.

ETL stands for Extract, Transform, Load. It's an established process for moving data from one system to another. For example, it's common to move data from a production database to a data warehouse.

There are many popular ETL tools, such as Fivetran and Airbyte.

Wrappers provide an alternative to these tools. You can use SQL to move data from one table to another:

This approach provides several benefits:

One disadvantage is that Wrappers are not as feature-rich as ETL tools. They also couple the ETL process to your database.

Supabase extends the ETL concept with real-time data access. Instead of moving gigabytes of data from one system to another before you can query it, you can instead query the data directly from the remote server. This additional option, "Query", extends the ETL process and is called QETL (pronounced "kettle"): Query, Extract, Transform, Load.

This approach has several benefits:

A common use case for Wrappers is to extract data from a production database and load it into a data warehouse. This can be done within your database using pg_cron. For example, you can schedule a job to run every night to extract data from your production database and load it into your data warehouse.

This process can be taxing on your database if you are moving large amounts of data. Often, it's better to use an external tool for batch ETL, such as Fivetran or Airbyte.

WebAssembly (Wasm) is a binary instruction format that enables high-performance execution of code on the web. Wrappers now includes a Wasm runtime, which provides a sandboxed execution environment, to run Wasm foreign data wrappers. Combined Wrappers with Wasm, developing and distributing new FDW becomes much easier and you can even build your own Wasm FDW and use it on Supabase platform.

To learn more about Wasm FDW, visit Wrappers official documentation.

Foreign Data Wrappers do not provide Row Level Security, thus it is not advised to expose them via your API. Wrappers should always be stored in a private schema. For example, if you are connecting to your Stripe account, you should create a stripe schema to store all of your foreign tables inside. This schema should not be added to the “Additional Schemas” setting in the API section.

If you want to expose any of the foreign table columns to your public API, you can create a Database Function with security definer in the public schema, and then you can interact with your foreign table through API. For better access control, the function should have appropriate filters on the foreign table to apply security rules based on your business needs.

As an example, go to SQL Editor and then follow below steps,

Create a Stripe Products foreign table:

Create a security definer function that queries the foreign table and filters on the name prefix parameter:

Restrict the function execution to a specific role only, for example, the authenticated users:

By default, the function created can be executed by any roles like anon, that means the foreign table is public accessible. Always limit the function execution permission to appropriate roles.

Once the preceding steps are finished, the function can be invoked from Supabase client to query the foreign table:

**Examples:**

Example 1 (unknown):
```unknown
1-- Copy data from your production database to your2-- data warehouse for the last 24 hours:34insert into warehouse.analytics5select * from public.analytics6where ts > (now() - interval '1 DAY');
```

Example 2 (unknown):
```unknown
1-- Get all purchases for a user from your data warehouse:2select3  auth.users.id as user_id,4  warehouse.orders.id as order_id5from6  warehouse.orders7join 8  auth.users on auth.users.id = warehouse.orders.user_id9where 10  auth.users.id = '<some_user_id>';
```

Example 3 (unknown):
```unknown
1-- Every day at 3am, copy data from your2-- production database to your data warehouse:3select cron.schedule(4  'nightly-etl',5  '0 3 * * *',6  $$7    insert into warehouse.analytics8    select * from public.analytics9    where ts > (now() - interval '1 DAY');10  $$11);
```

Example 4 (unknown):
```unknown
1create foreign table stripe.stripe_products (2  id text,3  name text,4  active bool,5  default_price text,6  description text,7  created timestamp,8  updated timestamp,9  attrs jsonb10)11  server stripe_fdw_server12  options (13    object 'products',14    rowid_column 'id'15  );
```

---

## Use Supabase Auth with React Native | Supabase Docs

**URL:** https://supabase.com/docs/guides/auth/quickstarts/react-native

**Contents:**
- Use Supabase Auth with React Native
- Learn how to use Supabase Auth with React Native
  - Create a new Supabase project
        - SQL_EDITOR
  - Create a React app
        - Terminal
  - Install the Supabase client library
        - Terminal
  - Set up your login component
        - Project URL

Use Supabase Auth with React Native

Learn how to use Supabase Auth with React Native

Launch a new project in the Supabase Dashboard.

Your new database has a table for storing your users. You can see that this table is currently empty by running some SQL in the SQL Editor.

Create a React app using the create-expo-app command.

Install supabase-js and the required dependencies.

Create a helper file lib/supabase.ts that exports a Supabase client using your Project URL and key.

You can also get the Project URL and key from the project's Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Let's set up a React Native component to manage logins and sign ups.

Add the Auth component to your App.tsx file. If the user is logged in, print the user id to the screen.

Start the app, and follow the instructions in the terminal.

**Examples:**

Example 1 (unknown):
```unknown
1select * from auth.users;
```

Example 2 (unknown):
```unknown
1npx create-expo-app -t expo-template-blank-typescript my-app
```

Example 3 (unknown):
```unknown
1cd my-app && npx expo install @supabase/supabase-js @react-native-async-storage/async-storage @rneui/themed react-native-url-polyfill
```

Example 4 (python):
```python
1import { AppState, Platform } from 'react-native'2import 'react-native-url-polyfill/auto'3import AsyncStorage from '@react-native-async-storage/async-storage'4import { createClient, processLock } from '@supabase/supabase-js'56const supabaseUrl = YOUR_REACT_NATIVE_SUPABASE_URL7const supabaseAnonKey = YOUR_REACT_NATIVE_SUPABASE_PUBLISHABLE_KEY89export const supabase = createClient(supabaseUrl, supabaseAnonKey, {10  auth: {11    ...(Platform.OS !== "web" ? { storage: AsyncStorage } : {}),12    autoRefreshToken: true,13    persistSession: true,14    detectSessionInUrl: false,15    lock: processLock,16  },17})1819// Tells Supabase Auth to continuously refresh the session automatically20// if the app is in the foreground. When this is added, you will continue21// to receive `onAuthStateChange` events with the `TOKEN_REFRESHED` or22// `SIGNED_OUT` event if the user's session is terminated. This should23// only be registered once.24if (Platform.OS !== "web") {25  AppState.addEventListener('change', (state) => {26    if (state === 'active') {27      supabase.auth.startAutoRefresh()28    } else {29      supabase.auth.stopAutoRefresh()30    }31  })32}
```

---

## CLI Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/cli/introduction

**Contents:**
- Supabase CLI
  - Additional links#
- Global flags
  - Flags
- supabase bootstrap
  - Usage
  - Flags
- supabase init
  - Usage
  - Flags

The Supabase CLI provides tools to develop your project locally and deploy to the Supabase Platform. The CLI is still under development, but it contains all the functionality for working with your Supabase projects and the Supabase Platform.

Supabase CLI supports global flags for every command.

create a support ticket for any CLI error

output debug logs to stderr

lookup domain names using the specified resolver

enable experimental features

use the specified docker network instead of a generated one

output format of status variables

use a specific profile for connecting to Supabase API

path to a Supabase project directory

answer yes to all prompts

Password to your remote Postgres database.

Initialize configurations for Supabase local development.

A supabase/config.toml file is created in your current working directory. This configuration is specific to each local project.

You may override the directory path by specifying the SUPABASE_WORKDIR environment variable or --workdir flag.

In addition to config.toml, the supabase directory may also contain other Supabase objects, such as migrations, functions, tests, etc.

Overwrite existing supabase/config.toml.

Use OrioleDB storage engine for Postgres.

Generate IntelliJ IDEA settings for Deno.

Generate VS Code settings for Deno.

Connect the Supabase CLI to your Supabase account by logging in with your personal access token.

Your access token is stored securely in native credentials storage. If native credentials storage is unavailable, it will be written to a plain text file at ~/.supabase/access-token.

If this behavior is not desired, such as in a CI environment, you may skip login by specifying the SUPABASE_ACCESS_TOKEN environment variable in other commands.

The Supabase CLI uses the stored token to access Management APIs for projects, functions, secrets, etc.

Name that will be used to store token in your settings

Do not open browser automatically

Use provided token instead of automatic login flow

Link your local development project to a hosted Supabase project.

PostgREST configurations are fetched from the Supabase platform and validated against your local configuration file.

Optionally, database settings can be validated if you provide a password. Your database password is saved in native credentials storage if available.

If you do not want to be prompted for the database password, such as in a CI environment, you may specify it explicitly via the SUPABASE_DB_PASSWORD environment variable.

Some commands like db dump, db push, and db pull require your project to be linked first.

Password to your remote Postgres database.

Project ref of the Supabase project.

Use direct connection instead of pooler.

Starts the Supabase local development stack.

Requires supabase/config.toml to be created in your current working directory by running supabase init.

All service containers are started by default. You can exclude those not needed by passing in -x flag. To exclude multiple containers, either pass in a comma separated string, such as -x gotrue,imgproxy, or specify -x flag multiple times.

It is recommended to have at least 7GB of RAM to start all services.

Health checks are automatically added to verify the started containers. Use --ignore-health-check flag to ignore these errors.

Names of containers to not start. [gotrue,realtime,storage-api,imgproxy,kong,mailpit,postgrest,postgres-meta,studio,edge-runtime,logflare,vector,supavisor]

Ignore unhealthy services and exit 0

Stops the Supabase local development stack.

Requires supabase/config.toml to be created in your current working directory by running supabase init.

All Docker resources are maintained across restarts. Use --no-backup flag to reset your local development data between restarts.

Use the --all flag to stop all local Supabase projects instances on the machine. Use with caution with --no-backup as it will delete all supabase local projects data.

Stop all local Supabase instances from all projects across the machine.

Deletes all data volumes after stopping.

Local project ID to stop.

Shows status of the Supabase local development stack.

Requires the local development stack to be started by running supabase start or supabase db start.

You can export the connection parameters for initializing supabase-js locally by specifying the -o env flag. Supported parameters include JWT_SECRET, ANON_KEY, and SERVICE_ROLE_KEY.

Override specific variable names.

Executes pgTAP tests against the local database.

Requires the local development stack to be started by running supabase start.

Runs pg_prove in a container with unit test files volume mounted from supabase/tests directory. The test file can be suffixed by either .sql or .pg extension.

Since each test is wrapped in its own transaction, it will be individually rolled back regardless of success or failure.

Tests the database specified by the connection string (must be percent-encoded).

Runs pgTAP tests on the linked project.

Runs pgTAP tests on the local database.

Template framework to generate.

Automatically generates type definitions based on your Postgres database schema.

This command connects to your database (local or remote) and generates typed definitions that match your database tables, views, and stored procedures. By default, it generates TypeScript definitions, but also supports Go and Swift.

Generated types give you type safety and autocompletion when working with your database in code, helping prevent runtime errors and improving developer experience.

The types respect relationships, constraints, and custom types defined in your database schema.

Securely generate a private JWT signing key for use in the CLI or to import in the dashboard.

Supported algorithms: ES256 - ECDSA with P-256 curve and SHA-256 (recommended) RS256 - RSA with SHA-256

Algorithm for signing key generation.

Append new key to existing keys file instead of overwriting.

Generate types from a database url.

Output language of the generated types.

Generate types from the linked project.

Generate types from the local dev database.

Generate types compatible with PostgREST v9 and below.

Generate types from a project ID.

Maximum timeout allowed for the database query.

Comma separated list of schema to include.

Access control for Swift generated types.

Pulls schema changes from a remote database. A new migration file will be created under supabase/migrations directory.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

Optionally, a new row can be inserted into the migration history table to reflect the current state of the remote database.

If no entries exist in the migration history table, pg_dump will be used to capture all contents of the remote schemas you have created. Otherwise, this command will only diff schema changes against the remote database, similar to running db diff --linked.

Pulls from the database specified by the connection string (must be percent-encoded).

Pulls from the linked project.

Pulls from the local database.

Password to your remote Postgres database.

Comma separated list of schema to include.

Pushes all local migrations to a remote database.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

The first time this command is run, a migration history table will be created under supabase_migrations.schema_migrations. After successfully applying a migration, a new row will be inserted into the migration history table with timestamp as its unique id. Subsequent pushes will skip migrations that have already been applied.

If you need to mutate the migration history table, such as deleting existing entries or inserting new entries without actually running the migration, use the migration repair command.

Use the --dry-run flag to view the list of changes before applying.

Pushes to the database specified by the connection string (must be percent-encoded).

Print the migrations that would be applied, but don't actually apply them.

Include all migrations not found on remote history table.

Include custom roles from supabase/roles.sql.

Include seed data from your config.

Pushes to the linked project.

Pushes to the local database.

Password to your remote Postgres database.

Resets the local database to a clean state.

Requires the local development stack to be started by running supabase start.

Recreates the local Postgres container and applies all local migrations found in supabase/migrations directory. If test data is defined in supabase/seed.sql, it will be seeded after the migrations are run. Any other data or schema changes made during local development will be discarded.

When running db reset with --linked or --db-url flag, a SQL script is executed to identify and drop all user created entities in the remote database. Since Postgres roles are cluster level entities, any custom roles created through the dashboard or supabase/roles.sql will not be deleted by remote reset.

Resets the database specified by the connection string (must be percent-encoded).

Reset up to the last n migration versions.

Resets the linked project with local migrations.

Resets the local database with local migrations.

Skip running the seed script after reset.

Reset up to the specified version.

Dumps contents from a remote database.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

Runs pg_dump in a container with additional flags to exclude Supabase managed schemas. The ignored schemas include auth, storage, and those created by extensions.

The default dump does not contain any data or custom roles. To dump those contents explicitly, specify either the --data-only and --role-only flag.

Dumps only data records.

Dumps from the database specified by the connection string (must be percent-encoded).

Prints the pg_dump script that would be executed.

List of schema.tables to exclude from data-only dump.

File path to save the dumped contents.

Keeps commented lines from pg_dump output.

Dumps from the linked project.

Dumps from the local database.

Password to your remote Postgres database.

Dumps only cluster roles.

Comma separated list of schema to include.

Use copy statements in place of inserts.

Diffs schema changes made to the local or remote database.

Requires the local development stack to be running when diffing against the local database. To diff against a remote or self-hosted database, specify the --linked or --db-url flag respectively.

Runs djrobstep/migra in a container to compare schema differences between the target database and a shadow database. The shadow database is created by applying migrations in local supabase/migrations directory in a separate container. Output is written to stdout by default. For convenience, you can also save the schema diff as a new migration file by passing in -f flag.

By default, all schemas in the target database are diffed. Use the --schema public,extensions flag to restrict diffing to a subset of schemas.

While the diff command is able to capture most schema changes, there are cases where it is known to fail. Currently, this could happen if you schema contains:

Diffs against the database specified by the connection string (must be percent-encoded).

Saves schema diff to a new migration file.

Diffs local migration files against the linked project.

Diffs local migration files against the local database.

Comma separated list of schema to include.

Use migra to generate schema diff.

Use pg-schema-diff to generate schema diff.

Use pgAdmin to generate schema diff.

Lints local database for schema errors.

Requires the local development stack to be running when linting against the local database. To lint against a remote or self-hosted database, specify the --linked or --db-url flag respectively.

Runs plpgsql_check extension in the local Postgres container to check for errors in all schemas. The default lint level is warning and can be raised to error via the --level flag.

To lint against specific schemas only, pass in the --schema flag.

The --fail-on flag can be used to control when the command should exit with a non-zero status code. The possible values are:

This flag is particularly useful in CI/CD pipelines where you want to fail the build based on certain lint conditions.

Lints the database specified by the connection string (must be percent-encoded).

Error level to exit with non-zero status.

Lints the linked project for schema errors.

Lints the local database for schema errors.

Comma separated list of schema to include.

Path to a logical backup file.

Creates a new migration file locally.

A supabase/migrations directory will be created if it does not already exists in your current workdir. All schema migration files must be created in this directory following the pattern <timestamp>_<name>.sql.

Outputs from other commands like db diff may be piped to migration new <name> via stdin.

Lists migration history in both local and remote databases.

Requires your local project to be linked to a remote database by running supabase link. For self-hosted databases, you can pass in the connection parameters using --db-url flag.

Note that URL strings must be escaped according to RFC 3986.

Local migrations are stored in supabase/migrations directory while remote migrations are tracked in supabase_migrations.schema_migrations table. Only the timestamps are compared to identify any differences.

In case of discrepancies between the local and remote migration history, you can resolve them using the migration repair command.

Lists migrations of the database specified by the connection string (must be percent-encoded).

Lists migrations applied to the linked project.

Lists migrations applied to the local database.

Password to your remote Postgres database.

Fetches migrations from the database specified by the connection string (must be percent-encoded).

Fetches migration history from the linked project.

Fetches migration history from the local database.

Repairs the remote migration history table.

Requires your local project to be linked to a remote database by running supabase link.

If your local and remote migration history goes out of sync, you can repair the remote history by marking specific migrations as --status applied or --status reverted. Marking as reverted will delete an existing record from the migration history table while marking as applied will insert a new record.

For example, your migration history may look like the table below, with missing entries in either local or remote.

To reset your migration history to a clean state, first delete your local migration file.

Then mark the remote migration 20230103054303 as reverted.

Now you can run db pull again to dump the remote schema as a local migration file.

Repairs migrations of the database specified by the connection string (must be percent-encoded).

Repairs the migration history of the linked project.

Repairs the migration history of the local database.

Password to your remote Postgres database.

Version status to update.

Squashes local schema migrations to a single migration file.

The squashed migration is equivalent to a schema only dump of the local database after applying existing migration files. This is especially useful when you want to remove repeated modifications of the same schema from your migration history.

However, one limitation is that data manipulation statements, such as insert, update, or delete, are omitted from the squashed migration. You will have to add them back manually in a new migration file. This includes cron jobs, storage buckets, and any encrypted secrets in vault.

By default, the latest <timestamp>_<name>.sql file will be updated to contain the squashed migration. You can override the target version using the --version <timestamp> flag.

If your supabase/migrations directory is empty, running supabase squash will do nothing.

Squashes migrations of the database specified by the connection string (must be percent-encoded).

Squashes the migration history of the linked project.

Squashes the migration history of the local database.

Password to your remote Postgres database.

Squash up to the specified version.

Applies migrations to the database specified by the connection string (must be percent-encoded).

Include all migrations not found on remote history table.

Applies pending migrations to the linked project.

Applies pending migrations to the local database.

Seeds the linked project.

Seeds the local database.

This command displays an estimation of table "bloat" - Due to Postgres' MVCC when data is updated or deleted new rows are created and old rows are made invisible and marked as "dead tuples". Usually the autovaccum process will asynchronously clean the dead tuples. Sometimes the autovaccum is unable to work fast enough to reduce or prevent tables from becoming bloated. High bloat can slow down queries, cause excessive IOPS and waste space in your database.

Tables with a high bloat ratio should be investigated to see if there are vacuuming is not quick enough or there are other issues.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command shows you statements that are currently holding locks and blocking, as well as the statement that is being blocked. This can be used in conjunction with inspect db locks to determine which statements need to be terminated in order to resolve lock contention.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command is much like the supabase inspect db outliers command, but ordered by the number of times a statement has been called.

You can use this information to see which queries are called most often, which can potentially be good candidates for optimisation.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command displays queries that have taken out an exclusive lock on a relation. Exclusive locks typically prevent other operations on that relation from taking place, and can be a cause of "hung" queries that are waiting for a lock to be granted.

If you see a query that is hanging for a very long time or causing blocking issues you may consider killing the query by connecting to the database and running SELECT pg_cancel_backend(PID); to cancel the query. If the query still does not stop you can force a hard stop by running SELECT pg_terminate_backend(PID);

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command displays currently running queries, that have been running for longer than 5 minutes, descending by duration. Very long running queries can be a source of multiple issues, such as preventing DDL statements completing or vacuum being unable to update relfrozenxid.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command displays statements, obtained from pg_stat_statements, ordered by the amount of time to execute in aggregate. This includes the statement itself, the total execution time for that statement, the proportion of total execution time for all statements that statement has taken up, the number of times that statement has been called, and the amount of time that statement spent on synchronous I/O (reading/writing from the file system).

Typically, an efficient query will have an appropriate ratio of calls to total execution time, with as little time spent on I/O as possible. Queries that have a high total execution time but low call count should be investigated to improve their performance. Queries that have a high proportion of execution time being spent on synchronous I/O should also be investigated.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command shows information about logical replication slots that are setup on the database. It shows if the slot is active, the state of the WAL sender process ('startup', 'catchup', 'streaming', 'backup', 'stopping') the replication client address and the replication lag in GB.

This command is useful to check that the amount of replication lag is as low as possible, replication lag can occur due to network latency issues, slow disk I/O, long running transactions or lack of ability for the subscriber to consume WAL fast enough.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This command analyzes table I/O patterns to show read/write activity ratios based on block-level operations. It combines data from PostgreSQL's pg_stat_user_tables (for tuple operations) and pg_statio_user_tables (for block I/O) to categorize each table's workload profile.

The command classifies tables into categories:

Note: This command only displays tables that have had both read and write activity. Tables with no I/O operations are not shown. The classification ratio threshold (default: 5:1) determines when a table is considered "heavy" in one direction versus balanced.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

This shows you stats about the vacuum activities for each table. Due to Postgres' MVCC when data is updated or deleted new rows are created and old rows are made invisible and marked as "dead tuples". Usually the autovaccum process will aysnchronously clean the dead tuples.

The command lists when the last vacuum and last auto vacuum took place, the row count on the table as well as the count of dead rows and whether autovacuum is expected to run or not. If the number of dead rows is much higher than the row count, or if an autovacuum is expected but has not been performed for some time, this can indicate that autovacuum is not able to keep up and that your vacuum settings need to be tweaked or that you require more compute or disk IOPS to allow autovaccum to complete.

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Path to save CSV files in

Inspect the database specified by the connection string (must be percent-encoded).

Inspect the linked project.

Inspect the local database.

Create an organization for the logged-in user.

List all organizations the logged-in user belongs.

Provides tools for creating and managing your Supabase projects.

This command group allows you to list all projects in your organizations, create new projects, delete existing projects, and retrieve API keys. These operations help you manage your Supabase infrastructure programmatically without using the dashboard.

Project management via CLI is especially useful for automation scripts and when you need to provision environments in a repeatable way.

Database password of the project.

Organization ID to create the project in.

Select a region close to you for the best performance.

Select a desired instance size for your project.

List all Supabase projects the logged-in user can access.

Project ref of the Supabase project.

Updates the configurations of a linked Supabase project with the local supabase/config.toml file.

This command allows you to manage project configuration as code by defining settings locally and then pushing them to your remote project.

Project ref of the Supabase project.

Create a preview branch for the linked project.

URL to notify when branch is active healthy.

Whether to create a persistent branch.

Select a region to deploy the branch database.

Select a desired instance size for the branch database.

Whether to clone production data to the branch database.

Project ref of the Supabase project.

List all preview branches of the linked project.

Project ref of the Supabase project.

Retrieve details of the specified preview branch.

Project ref of the Supabase project.

Update a preview branch by its name or ID.

Change the associated git branch.

Rename the preview branch.

URL to notify when branch is active healthy.

Switch between ephemeral and persistent branch.

Override the current branch status.

Project ref of the Supabase project.

Project ref of the Supabase project.

Project ref of the Supabase project.

Delete a preview branch by its name or ID.

Project ref of the Supabase project.

Manage Supabase Edge Functions.

Supabase Edge Functions are server-less functions that run close to your users.

Edge Functions allow you to execute custom server-side code without deploying or scaling a traditional server. They're ideal for handling webhooks, custom API endpoints, data validation, and serving personalized content.

Edge Functions are written in TypeScript and run on Deno compatible edge runtime, which is a secure runtime with no package management needed, fast cold starts, and built-in security.

Creates a new Edge Function with boilerplate code in the supabase/functions directory.

This command generates a starter TypeScript file with the necessary Deno imports and a basic function structure. The function is created as a new directory with the name you specify, containing an index.ts file with the function code.

After creating the function, you can edit it locally and then use supabase functions serve to test it before deploying with supabase functions deploy.

List all Functions in the linked Supabase project.

Project ref of the Supabase project.

Download the source code for a Function from the linked Supabase project.

Project ref of the Supabase project.

Unbundle functions server-side without using Docker.

Serve all Functions locally.

supabase functions serve command includes additional flags to assist developers in debugging Edge Functions via the v8 inspector protocol, allowing for debugging via Chrome DevTools, VS Code, and IntelliJ IDEA for example. Refer to the docs guide for setup instructions.

--inspect-mode [ run | brk | wait ]

Additionally, the following properties can be customized via supabase/config.toml under edge_runtime section.

Path to an env file to be populated to the Function environment.

Path to import map file.

Alias of --inspect-mode brk.

Allow inspecting the main worker.

Activate inspector capability for debugging.

Disable JWT verification for the Function.

Deploy a Function to the linked Supabase project.

Path to import map file.

Maximum number of parallel jobs.

Disable JWT verification for the Function.

Project ref of the Supabase project.

Delete Functions that exist in Supabase project but not locally.

Bundle functions server-side without using Docker.

Delete a Function from the linked Supabase project. This does NOT remove the Function locally.

Project ref of the Supabase project.

Provides tools for managing environment variables and secrets for your Supabase project.

This command group allows you to set, unset, and list secrets that are securely stored and made available to Edge Functions as environment variables.

Secrets management through the CLI is useful for:

Secrets can be set individually or loaded from .env files for convenience.

Set a secret(s) to the linked Supabase project.

Read secrets from a .env file.

Project ref of the Supabase project.

List all secrets in the linked project.

Project ref of the Supabase project.

Unset a secret(s) from the linked Supabase project.

Project ref of the Supabase project.

Recursively list a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Custom Cache-Control header for HTTP upload.

Custom Content-Type header for HTTP upload.

Maximum number of parallel jobs.

Recursively copy a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Recursively move a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Recursively remove a directory.

enable experimental features

Connects to Storage API of the linked project.

Connects to Storage API of the local database.

Add and configure a new connection to a SSO identity provider to your Supabase project.

File containing a JSON mapping between SAML attributes to custom JWT claims.

Comma separated list of email domains to associate with the added identity provider.

File containing a SAML 2.0 Metadata XML document describing the identity provider.

URL pointing to a SAML 2.0 Metadata XML document describing the identity provider.

URI reference representing the classification of string-based identifier information.

Whether local validation of the SAML 2.0 Metadata URL should not be performed.

Type of identity provider (according to supported protocol).

Project ref of the Supabase project.

List all connections to a SSO identity provider to your Supabase project.

Project ref of the Supabase project.

Provides the information about an established connection to an identity provider. You can use --metadata to obtain the raw SAML 2.0 Metadata XML document stored in your project's configuration.

Show SAML 2.0 XML Metadata only

Project ref of the Supabase project.

Returns all of the important SSO information necessary for your project to be registered with a SAML 2.0 compatible identity provider.

Project ref of the Supabase project.

Update the configuration settings of a already added SSO identity provider.

Add this comma separated list of email domains to the identity provider.

File containing a JSON mapping between SAML attributes to custom JWT claims.

Replace domains with this comma separated list of email domains.

File containing a SAML 2.0 Metadata XML document describing the identity provider.

URL pointing to a SAML 2.0 Metadata XML document describing the identity provider.

URI reference representing the classification of string-based identifier information.

Remove this comma separated list of email domains from the identity provider.

Whether local validation of the SAML 2.0 Metadata URL should not be performed.

Project ref of the Supabase project.

Remove a connection to an already added SSO identity provider. Removing the provider will prevent existing users from logging in. Please treat this command with care.

Project ref of the Supabase project.

Manage custom domain names for Supabase projects.

Use of custom domains and vanity subdomains is mutually exclusive.

Activates the custom hostname configuration for a project.

This reconfigures your Supabase project to respond to requests on your custom hostname.

After the custom hostname is activated, your project's third-party auth providers will no longer function on the Supabase-provisioned subdomain. Please refer to Prepare to activate your domain section in our documentation to learn more about the steps you need to follow.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Create a custom hostname for your Supabase project.

Expects your custom hostname to have a CNAME record to your Supabase project's subdomain.

The custom hostname to use for your Supabase project.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Retrieve the custom hostname config for your project, as stored in the Supabase platform.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Include raw output (useful for debugging).

Project ref of the Supabase project.

Manage vanity subdomains for Supabase projects.

Usage of vanity subdomains and custom domains is mutually exclusive.

Activate a vanity subdomain for your Supabase project.

This reconfigures your Supabase project to respond to requests on your vanity subdomain. After the vanity subdomain is activated, your project's auth services will no longer function on the {project-ref}.{supabase-domain} hostname.

The desired vanity subdomain to use for your Supabase project.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

The desired vanity subdomain to use for your Supabase project.

enable experimental features

Project ref of the Supabase project.

Deletes the vanity subdomain for a project, and reverts to using the project ref for routing.

enable experimental features

Project ref of the Supabase project.

Network bans are IPs that get temporarily blocked if their traffic pattern looks abusive (e.g. multiple failed auth attempts).

The subcommands help you view the current bans, and unblock IPs if desired.

enable experimental features

Project ref of the Supabase project.

IP to allow DB connections from.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

Append to existing restrictions instead of replacing them.

Bypass some of the CIDR validation checks.

CIDR to allow DB connections from.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

Whether the DB should disable SSL enforcement for all external connections.

Whether the DB should enable SSL enforcement for all external connections.

enable experimental features

Project ref of the Supabase project.

enable experimental features

Project ref of the Supabase project.

Overriding the default Postgres config could result in unstable database behavior. Custom configuration also overrides the optimizations generated based on the compute add-ons in use.

Config overrides specified as a 'key=value' pair

Do not restart the database after updating config.

If true, replaces all existing overrides with the ones provided. If false (default), merges existing overrides with the ones provided.

enable experimental features

Project ref of the Supabase project.

Delete specific config overrides, reverting them to their default values.

Config keys to delete (comma-separated)

Do not restart the database after deleting config.

enable experimental features

Project ref of the Supabase project.

List all SQL snippets of the linked project.

Project ref of the Supabase project.

Download contents of the specified SQL snippet.

Project ref of the Supabase project.

Generate the autocompletion script for supabase for the specified shell. See each sub-command's help for details on how to use the generated script.

Generate the autocompletion script for the zsh shell.

If shell completion is not already enabled in your environment you will need to enable it. You can execute the following once:

To load completions in your current shell session:

To load completions for every new session, execute once:

You will need to start a new shell for this setup to take effect.

disable completion descriptions

Generate the autocompletion script for powershell.

To load completions in your current shell session:

To load completions for every new session, add the output of the above command to your powershell profile.

disable completion descriptions

Generate the autocompletion script for the fish shell.

To load completions in your current shell session:

To load completions for every new session, execute once:

You will need to start a new shell for this setup to take effect.

disable completion descriptions

Generate the autocompletion script for the bash shell.

This script depends on the 'bash-completion' package. If it is not installed already, you can install it via your OS's package manager.

To load completions in your current shell session:

To load completions for every new session, execute once:

You will need to start a new shell for this setup to take effect.

disable completion descriptions

**Examples:**

Example 1 (unknown):
```unknown
1supabase bootstrap [template] [flags]
```

Example 2 (unknown):
```unknown
1supabase init [flags]
```

Example 3 (unknown):
```unknown
1supabase init
```

Example 4 (unknown):
```unknown
1Finished supabase init.
```

---

## C#: Introduction | Supabase Docs

**URL:** https://supabase.com/docs/reference/csharp/introduction

---

## Use Supabase with React | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/quickstarts/reactjs

**Contents:**
- Use Supabase with React
- Learn how to create a Supabase project, add some sample data to your database, and query the data from a React app.
  - Create a Supabase project
  - Create a React app
      - Explore drop-in UI components for your Supabase app.
        - Terminal
  - Install the Supabase client library
        - Terminal
  - Declare Supabase Environment Variables
        - Project URL

Use Supabase with React

Learn how to create a Supabase project, add some sample data to your database, and query the data from a React app.

Go to database.new and create a new Supabase project.

Alternatively, you can create a project using the Management API:

When your project is up and running, go to the Table Editor, create a new table and insert some data.

Alternatively, you can run the following snippet in your project's SQL Editor. This will create a instruments table with some sample data.

Make the data in your table publicly readable by adding an RLS policy:

Create a React app using a Vite template.

UI components built on shadcn/ui that connect to Supabase via a single command.

The fastest way to get started is to use the supabase-js client library which provides a convenient interface for working with Supabase from a React app.

Navigate to the React app and install supabase-js.

Create a .env.local file and populate with your Supabase connection variables:

You can also get the Project URL and key from the project's Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Replace the contents of App.jsx to add a getInstruments function to fetch the data and display the query result to the page using a Supabase client.

Run the development server, go to http://localhost:5173 in a browser and you should see the list of instruments.

**Examples:**

Example 1 (unknown):
```unknown
1# First, get your access token from https://supabase.com/dashboard/account/tokens2export SUPABASE_ACCESS_TOKEN="your-access-token"34# List your organizations to get the organization ID5curl -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \6  https://api.supabase.com/v1/organizations78# Create a new project (replace <org-id> with your organization ID)9curl -X POST https://api.supabase.com/v1/projects \10  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \11  -H "Content-Type: application/json" \12  -d '{13    "organization_id": "<org-id>",14    "name": "My Project",15    "region": "us-east-1",16    "db_pass": "<your-secure-password>"17  }'
```

Example 2 (unknown):
```unknown
1-- Create the table2create table instruments (3  id bigint primary key generated always as identity,4  name text not null5);6-- Insert some sample data into the table7insert into instruments (name)8values9  ('violin'),10  ('viola'),11  ('cello');1213alter table instruments enable row level security;
```

Example 3 (unknown):
```unknown
1create policy "public can read instruments"2on public.instruments3for select to anon4using (true);
```

Example 4 (unknown):
```unknown
1npm create vite@latest my-app -- --template react
```

---

## Python: Introduction | Supabase Docs

**URL:** https://supabase.com/docs/reference/python/introduction

---

## Use Supabase with Vue | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/quickstarts/vue

**Contents:**
- Use Supabase with Vue
- Learn how to create a Supabase project, add some sample data to your database, and query the data from a Vue app.
  - Create a Supabase project
  - Create a Vue app
      - Explore drop-in UI components for your Supabase app.
        - Terminal
  - Install the Supabase client library
        - Terminal
  - Declare Supabase Environment Variables
        - Project URL

Use Supabase with Vue

Learn how to create a Supabase project, add some sample data to your database, and query the data from a Vue app.

Go to database.new and create a new Supabase project.

Alternatively, you can create a project using the Management API:

When your project is up and running, go to the Table Editor, create a new table and insert some data.

Alternatively, you can run the following snippet in your project's SQL Editor. This will create a instruments table with some sample data.

Make the data in your table publicly readable by adding an RLS policy:

Create a Vue app using the npm init command.

UI components built on shadcn/ui that connect to Supabase via a single command.

The fastest way to get started is to use the supabase-js client library which provides a convenient interface for working with Supabase from a Vue app.

Navigate to the Vue app and install supabase-js.

Create a .env.local file and populate with your Supabase connection variables:

You can also get the Project URL and key from the project's Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Create a /src/lib directory in your Vue app, create a file called supabaseClient.js and add the following code to initialize the Supabase client:

Replace the existing content in your App.vue file with the following code.

Start the app and go to http://localhost:5173 in a browser and you should see the list of instruments.

**Examples:**

Example 1 (unknown):
```unknown
1# First, get your access token from https://supabase.com/dashboard/account/tokens2export SUPABASE_ACCESS_TOKEN="your-access-token"34# List your organizations to get the organization ID5curl -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \6  https://api.supabase.com/v1/organizations78# Create a new project (replace <org-id> with your organization ID)9curl -X POST https://api.supabase.com/v1/projects \10  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \11  -H "Content-Type: application/json" \12  -d '{13    "organization_id": "<org-id>",14    "name": "My Project",15    "region": "us-east-1",16    "db_pass": "<your-secure-password>"17  }'
```

Example 2 (unknown):
```unknown
1-- Create the table2create table instruments (3  id bigint primary key generated always as identity,4  name text not null5);6-- Insert some sample data into the table7insert into instruments (name)8values9  ('violin'),10  ('viola'),11  ('cello');1213alter table instruments enable row level security;
```

Example 3 (unknown):
```unknown
1create policy "public can read instruments"2on public.instruments3for select to anon4using (true);
```

Example 4 (unknown):
```unknown
1npm init vue@latest my-app
```

---

## Use Supabase with RedwoodJS | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/quickstarts/redwoodjs

**Contents:**
- Use Supabase with RedwoodJS
- Learn how to create a Supabase project, add some sample data to your database using Prisma migration and seeds, and query the data from a RedwoodJS app.
  - Setup your new Supabase Project
  - Gather Database Connection Strings
  - Create a RedwoodJS app
        - Terminal
  - Open your RedwoodJS app in VS Code
        - Terminal
  - Configure Environment Variables
        - .env

Use Supabase with RedwoodJS

Learn how to create a Supabase project, add some sample data to your database using Prisma migration and seeds, and query the data from a RedwoodJS app.

Create a new project in the Supabase Dashboard.

Be sure to make note of the Database Password you used as you will need this later to connect to your database.

Open the project Connect panel. This quickstart connects using the Transaction pooler and Session pooler mode. Transaction mode is used for application queries and Session mode is used for running migrations with Prisma.

To do this, set the connection mode to Transaction in the Database Settings page and copy the connection string and append ?pgbouncer=true&&connection_limit=1. pgbouncer=true disables Prisma from generating prepared statements. This is required since our connection pooler does not support prepared statements in transaction mode yet. The connection_limit=1 parameter is only required if you are using Prisma from a serverless environment. This is the Transaction mode connection string.

To get the Session mode connection pooler string, change the port of the connection string from the dashboard to 5432.

You will need the Transaction mode connection string and the Session mode connection string to setup environment variables in Step 5.

You can copy and paste these connection strings from the Supabase Dashboard when needed in later steps.

Create a RedwoodJS app with TypeScript.

The yarn package manager is required to create a RedwoodJS app. You will use it to run RedwoodJS commands later.

While TypeScript is recommended, If you want a JavaScript app, omit the --ts flag.

You'll develop your app, manage database migrations, and run your app in VS Code.

In your .env file, add the following environment variables for your database connection:

The DATABASE_URL should use the Transaction mode connection string you copied in Step 1.

The DIRECT_URL should use the Session mode connection string you copied in Step 1.

By default, RedwoodJS ships with a SQLite database, but we want to use Postgres.

Update your Prisma schema file api/db/schema.prisma to use your Supabase Postgres database connection environment variables you setup in Step 5.

Create the Instrument model in api/db/schema.prisma and then run yarn rw prisma migrate dev from your terminal to apply the migration.

Let's seed the database with a few instruments.

Update the file scripts/seeds.ts to contain the following code:

Run the seed database command to populate the Instrument table with the instruments you just created.

The reset database command yarn rw prisma db reset will recreate the tables and will also run the seed script.

Now, we'll use RedwoodJS generators to scaffold a CRUD UI for the Instrument model.

Start the app via yarn rw dev. A browser will open to the RedwoodJS Splash page.

Click on /instruments to visit http://localhost:8910/instruments where should see the list of instruments.

You may now edit, delete, and add new books using the scaffolded UI.

**Examples:**

Example 1 (unknown):
```unknown
1yarn create redwood-app my-app --ts
```

Example 2 (unknown):
```unknown
1cd my-app2code .
```

Example 3 (unknown):
```unknown
1# Transaction mode connection string used for migrations2DATABASE_URL="postgres://postgres.[project-ref]:[db-password]@xxx.pooler.supabase.com:6543/postgres?pgbouncer=true&connection_limit=1"34# Session mode connection string — used by Prisma Client5DIRECT_URL="postgres://postgres.[project-ref]:[db-password]@xxx.pooler.supabase.com:5432/postgres"
```

Example 4 (unknown):
```unknown
1datasource db {2  provider  = "postgresql"3  url       = env("DATABASE_URL")4  directUrl = env("DIRECT_URL")5}
```

---

## Build a User Management App with Refine | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/tutorials/with-refine

**Contents:**
- Build a User Management App with Refine
- About Refine#
- Project setup#
  - Create a project#
  - Set up the database schema#
  - Get API details#
      - Changes to API keys
- Building the app#
  - Initialize a Refine app#
  - Refine supabaseClient#

Build a User Management App with Refine

This tutorial demonstrates how to build a basic user management app. The app authenticates and identifies the user, stores their profile information in the database, and allows the user to log in, update their profile details, and upload a profile photo. The app uses:

If you get stuck while working through this guide, refer to the full example on GitHub.

Refine is a React-based framework used to rapidly build data-heavy applications like admin panels, dashboards, storefronts and any type of CRUD apps. It separates app concerns into individual layers, each backed by a React context and respective provider object. For example, the auth layer represents a context served by a specific set of authProvider methods that carry out authentication and authorization actions such as logging in, logging out, getting roles data, etc. Similarly, the data layer offers another level of abstraction that is equipped with dataProvider methods to handle CRUD operations at appropriate backend API endpoints.

Refine provides hassle-free integration with Supabase backend with its supplementary @refinedev/supabase package. It generates authProvider and dataProvider methods at project initialization, so we don't need to expend much effort to define them ourselves. We just need to choose Supabase as our backend service while creating the app with create refine-app.

It is possible to customize the authProvider for Supabase and as we'll see below, it can be tweaked from src/authProvider.ts file. In contrast, the Supabase dataProvider is part of node_modules and therefore is not subject to modification.

Before you start building you need to set up the Database and API. You can do this by starting a new Project in Supabase and then creating a "schema" inside the database.

Now set up the database schema. You can use the "User Management Starter" quickstart in the SQL Editor, or you can copy/paste the SQL from below and run it.

You can pull the database schema down to your local project by running the db pull command. Read the local development docs for detailed instructions.

Now that you've created some database tables, you are ready to insert data using the auto-generated API.

To do this, you need to get the Project URL and key from the project Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Let's start building the Refine app from scratch.

We can use create refine-app command to initialize an app. Run the following in the terminal:

In the above command, we are using the refine-supabase preset which chooses the Supabase supplementary package for our app. We are not using any UI framework, so we'll have a headless UI with plain React and CSS styling.

The refine-supabase preset installs the @refinedev/supabase package which out-of-the-box includes the Supabase dependency: supabase-js.

We also need to install @refinedev/react-hook-form and react-hook-form packages that allow us to use React Hook Form inside Refine apps. Run:

With the app initialized and packages installed, at this point before we begin discussing Refine concepts, let's try running the app:

We should have a running instance of the app with a Welcome page at http://localhost:5173.

Let's move ahead to understand the generated code now.

The create refine-app generated a Supabase client for us in the src/utility/supabaseClient.ts file. It has two constants: SUPABASE_URL and SUPABASE_KEY. We want to replace them as supabaseUrl and supabasePublishableKey respectively and assign them our own Supabase server's values.

We'll update it with environment variables managed by Vite:

And then, we want to save the environment variables in a .env.local file. All you need are the API URL and the key that you copied earlier.

The supabaseClient will be used in fetch calls to Supabase endpoints from our app. As we'll see below, the client is instrumental in implementing authentication using Refine's auth provider methods and CRUD actions with appropriate data provider methods.

One optional step is to update the CSS file src/App.css to make the app look nice. You can find the full contents of this file here.

In order for us to add login and user profile pages in this App, we have to tweak the <Refine /> component inside App.tsx.

The App.tsx file initially looks like this:

We'd like to focus on the <Refine /> component, which comes with several props passed to it. Notice the dataProvider prop. It uses a dataProvider() function with supabaseClient passed as argument to generate the data provider object. The authProvider object also uses supabaseClient in implementing its methods. You can look it up in src/authProvider.ts file.

If you examine the authProvider object you can notice that it has a login method that implements a OAuth and Email / Password strategy for authentication. We'll, however, remove them and use Magic Links to allow users sign in with their email without using passwords.

We want to use supabaseClient auth's signInWithOtp method inside authProvider.login method:

We also want to remove register, updatePassword, forgotPassword and getPermissions properties, which are optional type members and also not necessary for our app. The final authProvider object looks like this:

We have chosen to use the headless Refine core package that comes with no supported UI framework. So, let's set up a plain React component to manage logins and sign ups.

Create and edit src/components/auth.tsx:

Notice we are using the useLogin() Refine auth hook to grab the mutate: login method to use inside handleLogin() function and isLoading state for our form submission. The useLogin() hook conveniently offers us access to authProvider.login method for authenticating the user with OTP.

After a user is signed in we can allow them to edit their profile details and manage their account.

Let's create a new component for that in src/components/account.tsx.

Notice above that, we are using three Refine hooks, namely the useGetIdentity(), useLogOut() and useForm() hooks.

useGetIdentity() is a auth hook that gets the identity of the authenticated user. It grabs the current user by invoking the authProvider.getIdentity method under the hood.

useLogOut() is also an auth hook. It calls the authProvider.logout method to end the session.

useForm(), in contrast, is a data hook that exposes a series of useful objects that serve the edit form. For example, we are grabbing the onFinish function to submit the form with the handleSubmit event handler. We are also using formLoading property to present state changes of the submitted form.

The useForm() hook is a higher-level hook built on top of Refine's useForm() core hook. It fully supports form state management, field validation and submission using React Hook Form. Behind the scenes, it invokes the dataProvider.getOne method to get the user profile data from our Supabase /profiles endpoint and also invokes dataProvider.update method when onFinish() is called.

Now that we have all the components in place, let's define the routes for the pages in which they should be rendered.

Add the routes for /login with the <Auth /> component and the routes for index path with the <Account /> component. So, the final App.tsx:

Let's test the App by running the server again:

And then open the browser to localhost:5173 and you should see the completed app.

Every Supabase project is configured with Storage for managing large files like photos and videos.

Let's create an avatar for the user so that they can upload a profile photo. We can start by creating a new component:

Create and edit src/components/avatar.tsx:

And then we can add the widget to the Account page at src/components/account.tsx:

At this stage, you have a fully functional application!

**Examples:**

Example 1 (unknown):
```unknown
1supabase link --project-ref <project-id>2# You can get <project-id> from your project's dashboard URL: https://supabase.com/dashboard/project/<project-id>3supabase db pull
```

Example 2 (unknown):
```unknown
1npm create refine-app@latest -- --preset refine-supabase
```

Example 3 (unknown):
```unknown
1npm install @refinedev/react-hook-form react-hook-form
```

Example 4 (unknown):
```unknown
1cd app-name2npm run dev
```

---

## Use Supabase with Next.js | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/quickstarts/nextjs

**Contents:**
- Use Supabase with Next.js
- Learn how to create a Supabase project, add some sample data, and query from a Next.js app.
  - Create a Supabase project
  - Create a Next.js app
      - Explore drop-in UI components for your Supabase app.
  - Declare Supabase Environment Variables
        - Project URL
        - Publishable key
        - Anon key
      - Changes to API keys

Use Supabase with Next.js

Learn how to create a Supabase project, add some sample data, and query from a Next.js app.

Go to database.new and create a new Supabase project.

Alternatively, you can create a project using the Management API:

When your project is up and running, go to the Table Editor, create a new table and insert some data.

Alternatively, you can run the following snippet in your project's SQL Editor. This will create a instruments table with some sample data.

Make the data in your table publicly readable by adding an RLS policy:

Use the create-next-app command and the with-supabase template, to create a Next.js app pre-configured with:

UI components built on shadcn/ui that connect to Supabase via a single command.

Rename .env.example to .env.local and populate with your Supabase connection variables:

You can also get the Project URL and key from the project's Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Create a new file at app/instruments/page.tsx and populate with the following.

This selects all the rows from the instruments table in Supabase and render them on the page.

Run the development server, go to http://localhost:3000/instruments in a browser and you should see the list of instruments.

**Examples:**

Example 1 (unknown):
```unknown
1# First, get your access token from https://supabase.com/dashboard/account/tokens2export SUPABASE_ACCESS_TOKEN="your-access-token"34# List your organizations to get the organization ID5curl -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \6  https://api.supabase.com/v1/organizations78# Create a new project (replace <org-id> with your organization ID)9curl -X POST https://api.supabase.com/v1/projects \10  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \11  -H "Content-Type: application/json" \12  -d '{13    "organization_id": "<org-id>",14    "name": "My Project",15    "region": "us-east-1",16    "db_pass": "<your-secure-password>"17  }'
```

Example 2 (unknown):
```unknown
1-- Create the table2create table instruments (3  id bigint primary key generated always as identity,4  name text not null5);6-- Insert some sample data into the table7insert into instruments (name)8values9  ('violin'),10  ('viola'),11  ('cello');1213alter table instruments enable row level security;
```

Example 3 (unknown):
```unknown
1create policy "public can read instruments"2on public.instruments3for select to anon4using (true);
```

Example 4 (unknown):
```unknown
1npx create-next-app -e with-supabase
```

---

## Build a User Management App with Ionic Vue | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/tutorials/with-ionic-vue

**Contents:**
- Build a User Management App with Ionic Vue
- Project setup#
  - Create a project#
  - Set up the database schema#
  - Get API details#
      - Changes to API keys
- Building the app#
  - Initialize an Ionic Vue app#
  - Set up a login route#
  - Account page#

Build a User Management App with Ionic Vue

This tutorial demonstrates how to build a basic user management app. The app authenticates and identifies the user, stores their profile information in the database, and allows the user to log in, update their profile details, and upload a profile photo. The app uses:

If you get stuck while working through this guide, refer to the full example on GitHub.

Before you start building you need to set up the Database and API. You can do this by starting a new Project in Supabase and then creating a "schema" inside the database.

Now set up the database schema. You can use the "User Management Starter" quickstart in the SQL Editor, or you can copy/paste the SQL from below and run it.

You can pull the database schema down to your local project by running the db pull command. Read the local development docs for detailed instructions.

Now that you've created some database tables, you are ready to insert data using the auto-generated API.

To do this, you need to get the Project URL and key from the project Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Let's start building the Vue app from scratch.

We can use the Ionic CLI to initialize an app called supabase-ionic-vue:

Then let's install the only additional dependency: supabase-js

And finally we want to save the environment variables in a .env.

All we need are the API URL and the key that you copied earlier.

Now that we have the API credentials in place, let's create a helper file to initialize the Supabase client. These variables will be exposed on the browser, and that's completely fine since we have Row Level Security enabled on our Database.

Let's set up a Vue component to manage logins and sign ups. We'll use Magic Links, so users can sign in with their email without using passwords.

After a user is signed in we can allow them to edit their profile details and manage their account.

Let's create a new component for that called Account.vue.

Now that we have all the components in place, let's update App.vue and our routes:

Once that's done, run this in a terminal window:

And then open the browser to localhost:3000 and you should see the completed app.

Every Supabase project is configured with Storage for managing large files like photos and videos.

First install two packages in order to interact with the user's camera.

Capacitor is a cross-platform native runtime from Ionic that enables web apps to be deployed through the app store and provides access to native device API.

Ionic PWA elements is a companion package that will polyfill certain browser APIs that provide no user interface with custom Ionic UI.

With those packages installed we can update our main.ts to include an additional bootstrapping call for the Ionic PWA Elements.

Then create an AvatarComponent.

And then we can add the widget to the Account page:

At this stage you have a fully functional application!

**Examples:**

Example 1 (unknown):
```unknown
1supabase link --project-ref <project-id>2# You can get <project-id> from your project's dashboard URL: https://supabase.com/dashboard/project/<project-id>3supabase db pull
```

Example 2 (unknown):
```unknown
1npm install -g @ionic/cli2ionic start supabase-ionic-vue blank --type vue3cd supabase-ionic-vue
```

Example 3 (unknown):
```unknown
1npm install @supabase/supabase-js
```

Example 4 (unknown):
```unknown
1VITE_SUPABASE_URL=YOUR_SUPABASE_URL2VITE_SUPABASE_PUBLISHABLE_KEY=YOUR_SUPABASE_PUBLISHABLE_KEY
```

---

## Model context protocol (MCP) | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/mcp

**Contents:**
- Model context protocol (MCP)
- Connect your AI tools to Supabase using MCP
- Remote MCP installation#
  - Step 1: Follow our security best practices#
  - Step 2: Configure your AI tool#
  - Options
  - Installation
      - Authentication
  - Next steps#
- Manual authentication#

Model context protocol (MCP)

Connect your AI tools to Supabase using MCP

The Model Context Protocol (MCP) is a standard for connecting Large Language Models (LLMs) to platforms like Supabase. Once connected, your AI assistants can interact with and query your Supabase projects on your behalf.

Before running the MCP server, we recommend you read our security best practices to understand the risks of connecting an LLM to your Supabase projects and how to mitigate them.

Choose your Supabase platform, project, and MCP client and follow the installation instructions:

Scope the MCP server to a project. If no project is selected, all projects will be accessible.

Configure your MCP client to connect with your Supabase project

Some MCP clients will automatically prompt you to login during setup, while others may require manual authentication steps. Either authentication method will open a browser window where you can login to your Supabase account and grant organization access to the MCP client. In the future, we'll offer more fine grain control over these permissions.

Previously Supabase MCP required you to generate a personal access token (PAT), but this is no longer required.

Your AI tool is now connected to your Supabase project or account using remote MCP. Try asking the AI tool to query your database using natural language commands.

By default the hosted Supabase MCP server uses dynamic client registration to authenticate with your Supabase org. This means that you don't need to manually create a personal access token (PAT) or OAuth app to use the server.

There are some situations where you might want to manually authenticate the MCP server instead:

To authenticate the MCP server in a CI environment, you can create a personal access token (PAT) with the necessary scopes and pass it as a header to the MCP server.

Remember to never connect the MCP server to production data. Supabase MCP is only designed for development and testing purposes. See Security risks.

Navigate to your Supabase access tokens and generate a new token. Name the token based on its purpose, e.g. "Example App MCP CI token".

Pass the token to the Authorization header in your MCP server configuration. For example if you are using Claude Code, your MCP server configuration might look like this:

The above example assumes you have environment variables SUPABASE_ACCESS_TOKEN and SUPABASE_PROJECT_REF set in your CI environment.

Note that not every MCP client supports custom headers, so check your client's documentation for details.

If your MCP client requires an OAuth client ID and secret (e.g. Azure API Center), you can manually create an OAuth app in your Supabase account and pass the credentials to the MCP client.

Remember to never connect the MCP server to production data. Supabase MCP is only designed for development and testing purposes. See Security risks.

Navigate to your Supabase organization's OAuth apps and add a new application. Name the app based on its purpose, e.g. "Example App MCP".

Your client should provide you the website URL and callback URL that it expects for the OAuth app. Use these values when creating the OAuth app in Supabase.

Grant write access to all of the available scopes. In the future, the MCP server will support more fine-grained scopes, but for now all scopes are required.

After creating the OAuth app, copy the client ID and client secret to your MCP client.

Connecting any data source to an LLM carries inherent risks, especially when it stores sensitive data. Supabase is no exception, so it's important to discuss what risks you should be aware of and extra precautions you can take to lower them.

The primary attack vector unique to LLMs is prompt injection, which might trick an LLM into following untrusted commands that live within user content. An example attack could look something like this:

Most MCP clients like Cursor ask you to manually accept each tool call before they run. We recommend you always keep this setting enabled and always review the details of the tool calls before executing them.

To lower this risk further, Supabase MCP wraps SQL results with additional instructions to discourage LLMs from following instructions or commands that might be present in the data. This is not foolproof though, so you should always review the output before proceeding with further actions.

We recommend the following best practices to mitigate security risks when using the Supabase MCP server:

**Examples:**

Example 1 (http):
```http
https://mcp.supabase.com/mcp
```

Example 2 (json):
```json
1{
2  "mcpServers": {
3    "supabase": {
4      "url": "https://mcp.supabase.com/mcp"
5    }
6  }
7}
```

Example 3 (unknown):
```unknown
1{2  "mcpServers": {3    "supabase": {4      "type": "http",5      "url": "https://mcp.supabase.com/mcp?project_ref=${SUPABASE_PROJECT_REF}",6      "headers": {7        "Authorization": "Bearer ${SUPABASE_ACCESS_TOKEN}"8      }9    }10  }11}
```

---

## Face similarity search | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/quickstarts/face-similarity

**Contents:**
- Face similarity search
- Identify the celebrities who look most similar to you using Supabase Vecs.
- Project setup#
- Launching a notebook#
- Connecting to your database#
- Stepping through the notebook#
- Next steps#

Face similarity search

Identify the celebrities who look most similar to you using Supabase Vecs.

This guide will walk you through a "Face Similarity Search" example using Colab and Supabase Vecs. You will be able to identify the celebrities who look most similar to you (or any other person). You will:

Let's create a new Postgres database. This is as simple as starting a new Project in Supabase:

Your database will be available in less than a minute.

Finding your credentials:

You can find your project credentials on the dashboard:

Launch our semantic_text_deduplication notebook in Colab:

At the top of the notebook, you'll see a button Copy to Drive. Click this button to copy the notebook to your Google Drive.

Inside the Notebook, find the cell which specifies the DB_CONNECTION. It will contain some code like this:

Replace the DB_CONNECTION with your own connection string. You can find the connection string on your project dashboard by clicking Connect.

SQLAlchemy requires the connection string to start with postgresql:// (instead of postgres://). Don't forget to rename this after copying the string from the dashboard.

You must use the "connection pooling" string (domain ending in *.pooler.supabase.com) with Google Colab since Colab does not support IPv6.

Now all that's left is to step through the notebook. You can do this by clicking the "execute" button (ctrl+enter) at the top left of each code cell. The notebook guides you through the process of creating a collection, adding data to it, and querying it.

You can view the inserted items in the Table Editor, by selecting the vecs schema from the schema dropdown.

You can now start building your own applications with Vecs. Check our examples for ideas.

**Examples:**

Example 1 (unknown):
```unknown
1import vecs23DB_CONNECTION = "postgresql://<user>:<password>@<host>:<port>/<db_name>"45# create vector store client6vx = vecs.create_client(DB_CONNECTION)
```

---

## Database | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/overview

**Contents:**
- Database
- Features#
  - Table view#
  - Relationships#
  - Clone tables#
  - The SQL editor#
  - Additional features#
  - Extensions#
- Terminology#
  - Postgres or PostgreSQL?#

Every Supabase project comes with a full Postgres database, a free and open source database which is considered one of the world's most stable and advanced databases.

You don't have to be a database expert to start using Supabase. Our table view makes Postgres as easy to use as a spreadsheet.

Dig into the relationships within your data.

You can duplicate your tables, just like you would inside a spreadsheet.

Supabase comes with a SQL Editor. You can also save your favorite queries to run later!

Database backups do not include objects stored via the Storage API, as the database only includes metadata about these objects. Restoring an old backup does not restore objects that have been deleted since then.

To expand the functionality of your Postgres database, you can use extensions. You can enable Postgres extensions with the click of a button within the Supabase dashboard.

Learn more about all the extensions provided on Supabase.

PostgreSQL the database was derived from the POSTGRES Project, a package written at the University of California at Berkeley in 1986. This package included a query language called "PostQUEL".

In 1994, Postgres95 was built on top of POSTGRES code, adding an SQL language interpreter as a replacement for PostQUEL.

Eventually, Postgres95 was renamed to PostgreSQL to reflect the SQL query capability. After this, many people referred to it as Postgres since it's less prone to confusion. Supabase is all about simplicity, so we also refer to it as Postgres.

Read about resetting your database password here and changing the timezone of your server here.

---

## Getting Started | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started

**Contents:**
- Getting Started
  - Use cases#
  - Framework quickstarts#
  - Web app demos#
  - Mobile tutorials#

AI, Vectors, and embeddings

Subscription Payments (SaaS)

Expo React Native Social Auth

---

## Features | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/features

**Contents:**
- Features
- Database#
  - Postgres database#
  - Vector database#
  - Auto-generated REST API via PostgREST#
  - Auto-generated GraphQL API via pg_graphql#
  - Database webhooks#
  - Secrets and encryption#
  - Replication#
- Platform#

This is a non-exhaustive list of features that Supabase provides for every project.

Every project is a full Postgres database. Docs.

Store vector embeddings right next to the rest of your data. Docs.

RESTful APIs are auto-generated from your database, without a single line of code. Docs.

Fast GraphQL APIs using our custom Postgres GraphQL extension. Docs.

Send database changes to any external service using Webhooks. Docs.

Encrypt sensitive data and store secrets using our Postgres extension, Supabase Vault. Docs.

Automatically replicate your database to external destinations like data warehouses and analytics platforms. Docs.

Projects are backed up daily with the option to upgrade to Point in Time recovery. Docs.

White-label the Supabase APIs to create a branded experience for your users. Docs.

Restrict IP ranges that can connect to your database. Docs.

Enforce Postgres clients to connect via SSL. Docs.

Use Supabase Branches to test and preview changes. Docs.

Manage Supabase infrastructure via Terraform, an Infrastructure as Code tool. Docs.

Deploy read-only databases across multiple regions, for lower latency and better resource management. Docs.

Export Supabase logs to 3rd party providers and external tooling. Docs.

Login to the Supabase dashboard via SSO. Docs.

Receive your database changes through WebSockets. Docs.

Send messages between connected users through WebSockets. Docs.

Synchronize shared state across your users, including online status and typing indicators. Docs.

Build email logins for your application or website. Docs.

Provide social logins - everything from Apple, to GitHub, to Slack. Docs.

Provide phone logins using a third-party SMS provider. Docs.

Build passwordless logins via magic links for your application or website. Docs.

Control the data each user can access with Postgres Policies. Docs.

Add CAPTCHA to your sign-in, sign-up, and password reset forms. Docs.

Helpers for implementing user authentication in popular server-side languages and frameworks like Next.js, SvelteKit and Remix. Docs.

Supabase Storage makes it simple to store and serve files. Docs.

Cache large files using the Supabase CDN. Docs.

Automatically revalidate assets at the edge via the Smart CDN. Docs.

Transform images on the fly. Docs.

Upload large files using resumable uploads. Docs.

Interact with Storage from tool which supports the S3 protocol. Docs.

Globally distributed TypeScript functions to execute custom business logic. Docs.

Execute an Edge Function in a region close to your database. Docs.

Edge functions natively support NPM modules and Node built-in APIs. Link.

Use our CLI to develop your project locally and deploy to the Supabase Platform. Docs.

Manage your projects programmatically. Docs.

Official client libraries for JavaScript, Flutter and Swift. Unofficial libraries are supported by the community.

Supabase Features are in 4 different states - Private Alpha, Public Alpha, Beta and Generally Available.

Features are initially launched as a private alpha to gather feedback from the community. To join our early access program, send an email to product-ops@supabase.io.

The alpha stage indicates that the API might change in the future, not that the service isn’t stable. Even though the uptime Service Level Agreement does not cover products in Alpha, we do our best to have the service as stable as possible.

Features in Beta are tested by an external penetration tester for security issues. The API is guaranteed to be stable and there is a strict communication process for breaking changes.

In addition to the Beta requirements, features in GA are covered by the uptime SLA.

---

## Architecture | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/architecture

**Contents:**
- Architecture
- Choose your comfort level#
- Architecture#
  - Postgres (database)#
  - Studio (dashboard)#
  - GoTrue (Auth)#
  - PostgREST (API)#
  - Realtime (API & multiplayer)#
  - Storage API (large file storage)#
  - Deno (Edge Functions)#

Supabase is open source. We choose open source tools which are scalable and make them simple to use.

Supabase is not a 1-to-1 mapping of Firebase. While we are building many of the features that Firebase offers, we are not going about it the same way: our technological choices are quite different; everything we use is open source; and wherever possible, we use and support existing tools rather than developing from scratch.

Most notably, we use Postgres rather than a NoSQL store. This choice was deliberate. We believe that no other database offers the functionality required to compete with Firebase, while maintaining the scalability required to go beyond it.

Our goal at Supabase is to make all of Postgres easy to use. That doesn’t mean you have to use all of it. If you’re a Postgres veteran, you’ll probably love the tools that we offer. If you’ve never used Postgres before, then start smaller and grow into it. If you just want to treat Postgres like a simple table-store, that’s perfectly fine.

Each Supabase project consists of several tools:

Postgres is the core of Supabase. We do not abstract the Postgres database—you can access it and use it with full privileges. We provide tools which make Postgres as easy to use as Firebase.

An open source Dashboard for managing your database and services.

A JWT-based API for managing users and issuing access tokens. This integrates with PostgreSQL's Row Level Security and the API servers.

A standalone web server that turns your Postgres database directly into a RESTful API. We use this with our pg_graphql extension to provide a GraphQL API.

A scalable WebSocket engine for managing user Presence, broadcasting messages, and streaming database changes.

An S3-compatible object storage service that stores metadata in Postgres.

A modern runtime for JavaScript and TypeScript.

A RESTful API for managing your Postgres. Fetch tables, add roles, and run queries.

A cloud-native, multi-tenant Postgres connection pooler.

A cloud-native API gateway, built on top of NGINX.

It is our goal to provide an architecture that any large-scale company would design for themselves, and then provide tooling around that architecture that is easy-to-use for indie-developers and small teams.

We use a series of principles to ensure that scalability and usability are never mutually exclusive:

Each system must work as a standalone tool with as few moving parts as possible. The litmus test for this is: "Can a user run this product with nothing but a Postgres database?"

Supabase is composable. Even though every product works in isolation, each product on the platform needs to 10x the other products. For integration, each tool should expose an API and Webhooks.

We're deliberate about adding a new tool, and prefer instead to extend an existing one. This is the opposite of many cloud providers whose product offering expands into niche use-cases. We provide primitives for developers, which allow them to achieve any goal. Less, but better.

To avoid lock-in, we make it easy to migrate in and out. Our cloud offering is compatible with our self-hosted product. We use existing standards to increase portability (like pg_dump and CSV files). If a new standard emerges which competes with a "Supabase" approach, we will deprecate the approach in favor of the standard. This forces us to compete on user experience. We aim to be the best Postgres hosting service.

We sacrifice short-term wins for long-term gains. For example, it is tempting to run a fork of Postgres with additional functionality which only our customers need. Instead, we prefer to support efforts to upstream missing functionality so that the entire community benefits. This has the additional benefit of ensuring portability and longevity.

"Developers" are a specific profile of user: they are builders. When assessing impact as a function of effort, developers have a large efficiency due to the type of products and systems they can build. As the profile of a developer changes over time, Supabase will continue to evolve the product to fit this evolving profile.

Supabase supports existing tools and communities wherever possible. Supabase is more like a "community of communities" - each tool typically has its own community which we work with. Open source is something we approach collaboratively: we employ maintainers, sponsor projects, invest in businesses, and develop our own open source tools.

---

## Getting Started with Edge Functions | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/quickstart

**Contents:**
- Getting Started with Edge Functions
- Learn how to create, test, and deploy your first Edge Function using the Supabase CLI.
      - Prefer using the Supabase Dashboard?
- Step 1: Create or configure your project#
- Step 2: Create your first function#
- Step 3: Test your function locally#
      - First time running Supabase services?
- Step 4: Send a test request#
- Step 5: Connect to your Supabase project#
      - Need to create new Supabase project?

Getting Started with Edge Functions

Learn how to create, test, and deploy your first Edge Function using the Supabase CLI.

Before getting started, make sure you have the Supabase CLI installed. Check out the CLI installation guide for installation methods and troubleshooting.

You can also create and deploy functions directly from the Supabase Dashboard. Check out our Dashboard Quickstart guide.

If you don't have a project yet, initialize a new Supabase project in your current directory.

Or, if you already have a project locally, navigate to your project directory. If your project hasn't been configured for Supabase yet, make sure to run the supabase init command.

After this step, you should have a project directory with a supabase folder containing config.toml and an empty functions directory.

Within your project, generate a new Edge Function with a basic template:

This creates a new function at supabase/functions/hello-world/index.ts with this starter code:

This function accepts a JSON payload with a name field and returns a greeting message.

After this step, you should have a new file at supabase/functions/hello-world/index.ts containing the starter Edge Function code.

Start the local development server to test your function:

The supabase start command downloads Docker images, which can take a few minutes initially.

Function not starting locally?

Your function is now running at http://localhost:54321/functions/v1/hello-world. Hot reloading is enabled, which means that the server will automatically reload when you save changes to your function code.

After this step, you should have all Supabase services running locally, and your Edge Function serving at the local URL. Keep these terminal windows open.

Open a new terminal and test your function with curl:

Need your SUPABASE_PUBLISHABLE_KEY?

Run supabase status to see your local anon key and other credentials.

After running this curl command, you should see:

You can also try different inputs. Change "Functions" to "World" in the curl command and run it again to see the response change.

After this step, you should have successfully tested your Edge Function locally and received a JSON response with your greeting message.

To deploy your function globally, you need to connect your local project to a Supabase project.

Create one at database.new.

First, login to the CLI if you haven't already, and authenticate with Supabase. This opens your browser to authenticate with Supabase; complete the login process in your browser.

Next, list your Supabase projects to find your project ID:

Next, copy your project ID from the output, then connect your local project to your remote Supabase project. Replace YOUR_PROJECT_ID with the ID from the previous step.

After this step, you should have your local project authenticated and linked to your remote Supabase project. You can verify this by running supabase status.

Deploy your function to Supabase's global edge network:

The CLI automatically falls back to API-based deployment if Docker isn't available. You can also explicitly use API deployment with the --use-api flag:

If you want to skip JWT verification, you can add the --no-verify-jwt flag for webhooks that don't need authentication:

Use --no-verify-jwt carefully. It allows anyone to invoke your function without authentication!

When the deployment is successful, your function is automatically distributed to edge locations worldwide.

Now, you should have your Edge Function deployed and running globally at https://[YOUR_PROJECT_ID].supabase.co/functions/v1/hello-world.

🎉 Your function is now live! Test it with your project's anon key:

The SUPABASE_PUBLISHABLE_KEY is different in development and production. To get your production anon key, you can find it in your Supabase dashboard under Settings > API.

Finally, you should have a fully deployed Edge Function that you can call from anywhere in the world.

Now that your function is deployed, you can invoke it from within your app:

**Examples:**

Example 1 (unknown):
```unknown
1supabase init my-edge-functions-project2cd my-edge-functions-project
```

Example 2 (unknown):
```unknown
1cd your-existing-project2supabase init # Initialize Supabase, if you haven't already
```

Example 3 (unknown):
```unknown
1supabase functions new hello-world
```

Example 4 (javascript):
```javascript
1Deno.serve(async (req) => {2  const { name } = await req.json()3  const data = {4    message: `Hello ${name}!`,5  }67  return new Response(JSON.stringify(data), { headers: { 'Content-Type': 'application/json' } })8})
```

---

## Getting Started with Edge Functions (Dashboard) | Supabase Docs

**URL:** https://supabase.com/docs/guides/functions/quickstart-dashboard

**Contents:**
- Getting Started with Edge Functions (Dashboard)
- Learn how to create, test, and deploy your first Edge Function using the Supabase Dashboard.
      - Prefer using the CLI?
      - New to Supabase?
- Step 1: Navigate to the Edge Functions tab#
- Step 2: Create your first function#
      - Pre-built templates
- Step 3: Customize your function code#
- Step 4: Deploy your function#
- Step 5: Test your function#

Getting Started with Edge Functions (Dashboard)

Learn how to create, test, and deploy your first Edge Function using the Supabase Dashboard.

Supabase allows you to create Supabase Edge Functions directly from the Supabase Dashboard, making it easy to deploy functions without needing to set up a local development environment. The Edge Functions editor in the Dashboard has built-in syntax highlighting and type-checking for Deno and Supabase-specific APIs.

This guide will walk you through creating, testing, and deploying your first Edge Function using the Supabase Dashboard. You'll have a working function running globally in under 10 minutes.

You can also create and deploy functions using the Supabase CLI. Check out our CLI Quickstart guide.

You'll need a Supabase project to get started. If you don't have one yet, create a new project at database.new.

Navigate to your Supabase project dashboard and locate the Edge Functions section:

You'll see the Edge Functions overview page where you can manage all your functions.

Click the "Deploy a new function" button and select "Via Editor" to create a function directly in the dashboard.

The dashboard offers several pre-built templates for common use cases, such as Stripe Webhooks, OpenAI proxying, uploading files to Supabase Storage, and sending emails.

For this guide, we’ll select the "Hello World" template. If you’d rather start from scratch, you can ignore the pre-built templates.

The dashboard will load your chosen template in the code editor. Here's what the "Hello World" template looks like:

If needed, you can modify this code directly in the browser editor. The function accepts a JSON payload with a name field and returns a greeting message.

Once you're happy with your function code:

🚀 Your function is now automatically distributed to edge locations worldwide, running at https://YOUR_PROJECT_ID.supabase.co/functions/v1/hello-world

Supabase has built-in tools for testing your Edge Functions from the Dashboard. You can execute your Edge Function with different request payloads, headers, and query parameters. The built-in tester returns the response status, headers, and body.

On your function's details page:

Click "Send Request" to test your function.

In this example, we successfully tested our Hello World function by sending a JSON payload with a name field, and received the expected greeting message back.

Your function is now live at:

To invoke this Edge Function from within your application, you'll need API keys. Navigate to Settings > API Keys in your dashboard to find:

If you’d like to update the deployed function code, click on the function you want to edit, modify the code as needed, then click Deploy updates. This will overwrite the existing deployment with the newly edited function code.

There is currently no version control for edits! The Dashboard's Edge Function editor currently does not support version control, versioning, or rollbacks. We recommend using it only for quick testing and prototypes.

Now that your function is deployed, you can invoke it from within your app:

You can also use Supabase's AI Assistant to generate and deploy functions automatically.

Go to your project > Deploy a new function > Via AI Assistant.

Describe what you want your function to do in the prompt

Click Deploy and the Assistant will create and deploy the function for you.

Now that your function is deployed, you can access it from your local development environment. To use your Edge Function code within your local development environment, you can download your function source code either through the dashboard, or the CLI.

Before getting started, make sure you have the Supabase CLI installed. Check out the CLI installation guide for installation methods and troubleshooting.

At this point, your function has been downloaded to your local environment. Make the required changes, and redeploy when you're ready.

**Examples:**

Example 1 (unknown):
```unknown
1https://YOUR_PROJECT_ID.supabase.co/functions/v1/hello-world
```

Example 2 (python):
```python
1import { createClient } from '@supabase/supabase-js'23const supabase = createClient('https://[YOUR_PROJECT_ID].supabase.co', 'YOUR_ANON_KEY')45const { data, error } = await supabase.functions.invoke('hello-world', {6  body: { name: 'JavaScript' },7})89console.log(data) // { message: "Hello JavaScript!" }
```

Example 3 (unknown):
```unknown
1# Link your project to your local environment2supabase link --project-ref [project-ref]34# List all functions in the linked project5supabase functions list67# Download a function8supabase functions download hello-world
```

Example 4 (unknown):
```unknown
1# Run a function locally2supabase functions serve hello-world34# Redeploy when you're ready with your changes5supabase functions deploy hello-world
```

---

## Semantic Text Deduplication | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/quickstarts/text-deduplication

**Contents:**
- Semantic Text Deduplication
- Finding duplicate movie reviews with Supabase Vecs.
- Project setup#
- Launching a notebook#
- Connecting to your database#
- Stepping through the notebook#
- Deployment#
- Next steps#

Semantic Text Deduplication

Finding duplicate movie reviews with Supabase Vecs.

This guide will walk you through a "Semantic Text Deduplication" example using Colab and Supabase Vecs. You'll learn how to find similar movie reviews using embeddings, and remove any that seem like duplicates. You will:

Let's create a new Postgres database. This is as simple as starting a new Project in Supabase:

Your database will be available in less than a minute.

Finding your credentials:

You can find your project credentials on the dashboard:

Launch our semantic_text_deduplication notebook in Colab:

At the top of the notebook, you'll see a button Copy to Drive. Click this button to copy the notebook to your Google Drive.

Inside the Notebook, find the cell which specifies the DB_CONNECTION. It will contain some code like this:

Replace the DB_CONNECTION with your own connection string. You can find the connection string on your project dashboard by clicking Connect.

SQLAlchemy requires the connection string to start with postgresql:// (instead of postgres://). Don't forget to rename this after copying the string from the dashboard.

You must use the "connection pooling" string (domain ending in *.pooler.supabase.com) with Google Colab since Colab does not support IPv6.

Now all that's left is to step through the notebook. You can do this by clicking the "execute" button (ctrl+enter) at the top left of each code cell. The notebook guides you through the process of creating a collection, adding data to it, and querying it.

You can view the inserted items in the Table Editor, by selecting the vecs schema from the schema dropdown.

If you have your own infrastructure for deploying Python apps, you can continue to use vecs as described in this guide.

Alternatively if you would like to quickly deploy using Supabase, check out our guide on using the Hugging Face Inference API in Edge Functions using TypeScript.

You can now start building your own applications with Vecs. Check our examples for ideas.

**Examples:**

Example 1 (unknown):
```unknown
1import vecs23DB_CONNECTION = "postgresql://<user>:<password>@<host>:<port>/<db_name>"45# create vector store client6vx = vecs.create_client(DB_CONNECTION)
```

---

## Use Supabase with Laravel | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/quickstarts/laravel

**Contents:**
- Use Supabase with Laravel
- Learn how to create a PHP Laravel project, connect it to your Supabase Postgres database, and configure user authentication.
  - Create a Laravel Project
        - Terminal
  - Install the Authentication template
        - Terminal
  - Set up the Postgres connection details
        - .env
  - Change the default schema
        - app/config/database.php

Use Supabase with Laravel

Learn how to create a PHP Laravel project, connect it to your Supabase Postgres database, and configure user authentication.

Make sure your PHP and Composer versions are up to date, then use composer create-project to scaffold a new Laravel project.

See the Laravel docs for more details.

Install Laravel Breeze, a simple implementation of all of Laravel's authentication features.

Go to database.new and create a new Supabase project. Save your database password securely.

When your project is up and running, navigate to your project dashboard and click on Connect.

Look for the Session Pooler connection string and copy the string. You will need to replace the Password with your saved database password. You can reset your database password in your Database Settings if you do not have it.

If you're in an IPv6 environment or have the IPv4 Add-On, you can use the direct connection string instead of Supavisor in Session mode.

By default Laravel uses the public schema. We recommend changing this as Supabase exposes the public schema as a data API.

You can change the schema of your Laravel application by modifying the search_path variable app/config/database.php.

The schema you specify in search_path has to exist on Supabase. You can create a new schema from the Table Editor.

Laravel ships with database migration files that set up the required tables for Laravel Authentication and User Management.

Note: Laravel does not use Supabase Auth but rather implements its own authentication system!

Run the development server. Go to http://127.0.0.1:8000 in a browser to see your application. You can also navigate to http://127.0.0.1:8000/register and http://127.0.0.1:8000/login to register and log in users.

**Examples:**

Example 1 (unknown):
```unknown
1composer create-project laravel/laravel example-app
```

Example 2 (unknown):
```unknown
1composer require laravel/breeze --dev2php artisan breeze:install
```

Example 3 (unknown):
```unknown
1DB_CONNECTION=pgsql2DB_URL=postgres://postgres.xxxx:password@xxxx.pooler.supabase.com:5432/postgres
```

Example 4 (javascript):
```javascript
1'pgsql' => [2    'driver' => 'pgsql',3    'url' => env('DB_URL'),4    'host' => env('DB_HOST', '127.0.0.1'),5    'port' => env('DB_PORT', '5432'),6    'database' => env('DB_DATABASE', 'laravel'),7    'username' => env('DB_USERNAME', 'root'),8    'password' => env('DB_PASSWORD', ''),9    'charset' => env('DB_CHARSET', 'utf8'),10    'prefix' => '',11    'prefix_indexes' => true,12    'search_path' => 'laravel',13    'sslmode' => 'prefer',14],
```

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-auth/introduction

**Contents:**
- Self-Hosting Auth
  - Client libraries#
  - Additional links#
- Generates an email action link.
  - Body
  - Response codes
  - Response (200)
- Get a user.
  - Path parameters
  - Response codes

The Supabase Auth Server (GoTrue) is a JSON Web Token (JWT)-based API for managing users and issuing access tokens.

GoTrue is an open-source API written in Golang, that acts as a self-standing API service for handling user registration and authentication for JAM projects. It's based on OAuth2 and JWT and handles user signup, authentication, and custom user data.

**Examples:**

Example 1 (unknown):
```unknown
1{2  "action_link": "lorem",3  "app_metadata": {4    "property1": null,5    "property2": null6  },7  "aud": "lorem",8  "banned_until": "2021-12-31T23:34:00Z",9  "confirmation_sent_at": "2021-12-31T23:34:00Z",10  "confirmed_at": "2021-12-31T23:34:00Z",11  "created_at": "2021-12-31T23:34:00Z",12  "email": "lorem",13  "email_change_sent_at": "2021-12-31T23:34:00Z",14  "email_confirmed_at": "2021-12-31T23:34:00Z",15  "email_otp": "lorem",16  "hashed_token": "lorem",17  "id": "fbdf5a53-161e-4460-98ad-0e39408d8689",18  "identities": [19    {20      "created_at": "2021-12-31T23:34:00Z",21      "id": "lorem",22      "identity_data": {23        "property1": null,24        "property2": null25      },26      "last_sign_in_at": "2021-12-31T23:34:00Z",27      "provider": "lorem",28      "updated_at": "2021-12-31T23:34:00Z",29      "user_id": "fbdf5a53-161e-4460-98ad-0e39408d8689"30    }31  ],32  "invited_at": "2021-12-31T23:34:00Z",33  "last_sign_in_at": "2021-12-31T23:34:00Z",34  "new_email": "lorem",35  "new_phone": "lorem",36  "phone": "lorem",37  "phone_change_sent_at": "2021-12-31T23:34:00Z",38  "phone_confirmed_at": "2021-12-31T23:34:00Z",39  "reauthentication_sent_at": "2021-12-31T23:34:00Z",40  "recovery_sent_at": "2021-12-31T23:34:00Z",41  "redirect_to": "lorem",42  "role": "lorem",43  "updated_at": "2021-12-31T23:34:00Z",44  "user_metadata": {45    "property1": null,46    "property2": null47  },48  "verification_type": "lorem"49}
```

Example 2 (unknown):
```unknown
1{2  "app_metadata": {3    "property1": null,4    "property2": null5  },6  "aud": "lorem",7  "banned_until": "2021-12-31T23:34:00Z",8  "confirmation_sent_at": "2021-12-31T23:34:00Z",9  "confirmed_at": "2021-12-31T23:34:00Z",10  "created_at": "2021-12-31T23:34:00Z",11  "email": "lorem",12  "email_change_sent_at": "2021-12-31T23:34:00Z",13  "email_confirmed_at": "2021-12-31T23:34:00Z",14  "id": "fbdf5a53-161e-4460-98ad-0e39408d8689",15  "identities": [16    {17      "created_at": "2021-12-31T23:34:00Z",18      "id": "lorem",19      "identity_data": {20        "property1": null,21        "property2": null22      },23      "last_sign_in_at": "2021-12-31T23:34:00Z",24      "provider": "lorem",25      "updated_at": "2021-12-31T23:34:00Z",26      "user_id": "fbdf5a53-161e-4460-98ad-0e39408d8689"27    }28  ],29  "invited_at": "2021-12-31T23:34:00Z",30  "last_sign_in_at": "2021-12-31T23:34:00Z",31  "new_email": "lorem",32  "new_phone": "lorem",33  "phone": "lorem",34  "phone_change_sent_at": "2021-12-31T23:34:00Z",35  "phone_confirmed_at": "2021-12-31T23:34:00Z",36  "reauthentication_sent_at": "2021-12-31T23:34:00Z",37  "recovery_sent_at": "2021-12-31T23:34:00Z",38  "role": "lorem",39  "updated_at": "2021-12-31T23:34:00Z",40  "user_metadata": {41    "property1": null,42    "property2": null43  }44}
```

Example 3 (unknown):
```unknown
1{2  "app_metadata": {3    "property1": null,4    "property2": null5  },6  "aud": "lorem",7  "banned_until": "2021-12-31T23:34:00Z",8  "confirmation_sent_at": "2021-12-31T23:34:00Z",9  "confirmed_at": "2021-12-31T23:34:00Z",10  "created_at": "2021-12-31T23:34:00Z",11  "email": "lorem",12  "email_change_sent_at": "2021-12-31T23:34:00Z",13  "email_confirmed_at": "2021-12-31T23:34:00Z",14  "id": "fbdf5a53-161e-4460-98ad-0e39408d8689",15  "identities": [16    {17      "created_at": "2021-12-31T23:34:00Z",18      "id": "lorem",19      "identity_data": {20        "property1": null,21        "property2": null22      },23      "last_sign_in_at": "2021-12-31T23:34:00Z",24      "provider": "lorem",25      "updated_at": "2021-12-31T23:34:00Z",26      "user_id": "fbdf5a53-161e-4460-98ad-0e39408d8689"27    }28  ],29  "invited_at": "2021-12-31T23:34:00Z",30  "last_sign_in_at": "2021-12-31T23:34:00Z",31  "new_email": "lorem",32  "new_phone": "lorem",33  "phone": "lorem",34  "phone_change_sent_at": "2021-12-31T23:34:00Z",35  "phone_confirmed_at": "2021-12-31T23:34:00Z",36  "reauthentication_sent_at": "2021-12-31T23:34:00Z",37  "recovery_sent_at": "2021-12-31T23:34:00Z",38  "role": "lorem",39  "updated_at": "2021-12-31T23:34:00Z",40  "user_metadata": {41    "property1": null,42    "property2": null43  }44}
```

Example 4 (unknown):
```unknown
1{2  "aud": "lorem",3  "users": [4    {5      "app_metadata": {6        "property1": null,7        "property2": null8      },9      "aud": "lorem",10      "banned_until": "2021-12-31T23:34:00Z",11      "confirmation_sent_at": "2021-12-31T23:34:00Z",12      "confirmed_at": "2021-12-31T23:34:00Z",13      "created_at": "2021-12-31T23:34:00Z",14      "email": "lorem",15      "email_change_sent_at": "2021-12-31T23:34:00Z",16      "email_confirmed_at": "2021-12-31T23:34:00Z",17      "id": "fbdf5a53-161e-4460-98ad-0e39408d8689",18      "identities": [19        {20          "created_at": "2021-12-31T23:34:00Z",21          "id": "lorem",22          "identity_data": {23            "property1": null,24            "property2": null25          },26          "last_sign_in_at": "2021-12-31T23:34:00Z",27          "provider": "lorem",28          "updated_at": "2021-12-31T23:34:00Z",29          "user_id": "fbdf5a53-161e-4460-98ad-0e39408d8689"30        }31      ],32      "invited_at": "2021-12-31T23:34:00Z",33      "last_sign_in_at": "2021-12-31T23:34:00Z",34      "new_email": "lorem",35      "new_phone": "lorem",36      "phone": "lorem",37      "phone_change_sent_at": "2021-12-31T23:34:00Z",38      "phone_confirmed_at": "2021-12-31T23:34:00Z",39      "reauthentication_sent_at": "2021-12-31T23:34:00Z",40      "recovery_sent_at": "2021-12-31T23:34:00Z",41      "role": "lorem",42      "updated_at": "2021-12-31T23:34:00Z",43      "user_metadata": {44        "property1": null,45        "property2": null46      }47    }48  ]49}
```

---

## Swift: Introduction | Supabase Docs

**URL:** https://supabase.com/docs/reference/swift/introduction

---

## AI Prompt: Postgres SQL Style Guide | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/ai-prompts/code-format-sql

**Contents:**
- AI Prompt: Postgres SQL Style Guide
- How to use#
- Prompt#

AI Prompt: Postgres SQL Style Guide

Copy the prompt to a file in your repo.

Use the "include file" feature from your AI tool to include the prompt when chatting with your AI assistant. For example, with GitHub Copilot, use #<filename>, in Cursor, use @Files, and in Zed, use /file.

You can also load the prompt directly into your IDE via the following links:

**Examples:**

Example 1 (unknown):
```unknown
1# Postgres SQL Style Guide23## General45- Use lowercase for SQL reserved words to maintain consistency and readability.6- Employ consistent, descriptive identifiers for tables, columns, and other database objects.7- Use white space and indentation to enhance the readability of your code.8- Store dates in ISO 8601 format (`yyyy-mm-ddThh:mm:ss.sssss`).9- Include comments for complex logic, using '/* ... */' for block comments and '--' for line comments.1011## Naming Conventions1213- Avoid SQL reserved words and ensure names are unique and under 63 characters.14- Use snake_case for tables and columns.15- Prefer plurals for table names16- Prefer singular names for columns.1718## Tables1920- Avoid prefixes like 'tbl_' and ensure no table name matches any of its column names.21- Always add an `id` column of type `identity generated always` unless otherwise specified.22- Create all tables in the `public` schema unless otherwise specified.23- Always add the schema to SQL queries for clarity.24- Always add a comment to describe what the table does. The comment can be up to 1024 characters.2526## Columns2728- Use singular names and avoid generic names like 'id'.29- For references to foreign tables, use the singular of the table name with the `_id` suffix. For example `user_id` to reference the `users` table30- Always use lowercase except in cases involving acronyms or when readability would be enhanced by an exception.3132#### Examples:3334```sql35create table books (36  id bigint generated always as identity primary key,37  title text not null,38  author_id bigint references authors (id)39);40comment on table books is 'A list of all the books in the library.';41```424344## Queries4546- When the query is shorter keep it on just a few lines. As it gets larger start adding newlines for readability47- Add spaces for readability.4849Smaller queries:505152```sql53select *54from employees55where end_date is null;5657update employees58set end_date = '2023-12-31'59where employee_id = 1001;60```6162Larger queries:6364```sql65select66  first_name,67  last_name68from69  employees70where71  start_date between '2021-01-01' and '2021-12-31'72and73  status = 'employed';74```757677### Joins and Subqueries7879- Format joins and subqueries for clarity, aligning them with related SQL clauses.80- Prefer full table names when referencing tables. This helps for readability.8182```sql83select84  employees.employee_name,85  departments.department_name86from87  employees88join89  departments on employees.department_id = departments.department_id90where91  employees.start_date > '2022-01-01';92```9394## Aliases9596- Use meaningful aliases that reflect the data or transformation applied, and always include the 'as' keyword for clarity.9798```sql99select count(*) as total_employees100from employees101where end_date is null;102```103104105## Complex queries and CTEs106107- If a query is extremely complex, prefer a CTE.108- Make sure the CTE is clear and linear. Prefer readability over performance.109- Add comments to each block.110111```sql112with department_employees as (113  -- Get all employees and their departments114  select115    employees.department_id,116    employees.first_name,117    employees.last_name,118    departments.department_name119  from120    employees121  join122    departments on employees.department_id = departments.department_id123),124employee_counts as (125  -- Count how many employees in each department126  select127    department_name,128    count(*) as num_employees129  from130    department_employees131  group by132    department_name133)134select135  department_name,136  num_employees137from138  employee_counts139order by140  department_name;141```
```

---

## Creating and managing collections | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/quickstarts/hello-world

**Contents:**
- Creating and managing collections
- Connecting to your database with Colab.
- Project setup#
- Launching a notebook#
- Connecting to your database#
- Stepping through the notebook#
- Next steps#

Creating and managing collections

Connecting to your database with Colab.

This guide will walk you through a basic "Hello World" example using Colab and Supabase Vecs. You'll learn how to:

Let's create a new Postgres database. This is as simple as starting a new Project in Supabase:

Your database will be available in less than a minute.

Finding your credentials:

You can find your project credentials on the dashboard:

Launch our vector_hello_world notebook in Colab:

At the top of the notebook, you'll see a button Copy to Drive. Click this button to copy the notebook to your Google Drive.

Inside the Notebook, find the cell which specifies the DB_CONNECTION. It will contain some code like this:

Replace the DB_CONNECTION with your Session pooler connection string. You can find the connection string on your project dashboard by clicking Connect.

SQLAlchemy requires the connection string to start with postgresql:// (instead of postgres://). Don't forget to rename this after copying the string from the dashboard.

You must use the Session pooler connection string with Google Colab since Colab does not support IPv6.

Now all that's left is to step through the notebook. You can do this by clicking the "execute" button (ctrl+enter) at the top left of each code cell. The notebook guides you through the process of creating a collection, adding data to it, and querying it.

You can view the inserted items in the Table Editor, by selecting the vecs schema from the schema dropdown.

You can now start building your own applications with Vecs. Check our examples for ideas.

**Examples:**

Example 1 (unknown):
```unknown
1import vecs23DB_CONNECTION = "postgresql://<user>:<password>@<host>:<port>/<db_name>"45# create vector store client6vx = vecs.create_client(DB_CONNECTION)
```

---

## Deploy MCP servers | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/byo-mcp

**Contents:**
- Deploy MCP servers
- Deploy your MCP server#
  - Prerequisites#
  - Create a new project#
  - Create the MCP server function#
  - Local development#
  - Test your MCP server#
  - Deploy to production#
- Adding more tools#
- Examples#

Build and deploy Model Context Protocol (MCP) servers on Supabase using Edge Functions.

This guide covers MCP servers that do not require authentication. Auth support for MCP on Edge Functions is coming soon.

Before you begin, make sure you have:

Start by creating a new Supabase project:

Create a new Edge Function for your MCP server:

Create a deno.json file in supabase/functions/mcp/ with the required dependencies:

This tutorial uses the official MCP TypeScript SDK, but you can use any MCP framework that's compatible with the Edge Runtime, such as mcp-lite, mcp-use, or mcp-handler.

Replace the contents of supabase/functions/mcp/index.ts with:

Start the Supabase local development stack:

In a separate terminal, serve your function:

Your MCP server is now running at:

The --no-verify-jwt flag disables JWT verification at the Edge Function layer so your MCP server can accept unauthenticated requests. Authenticated MCP support is coming soon.

Test your server with the official MCP Inspector:

Use the local endpoint http://localhost:54321/functions/v1/mcp in the inspector UI to explore available tools and test them interactively.

When you're ready to deploy, link your project and deploy the function:

Your MCP server will be available at:

Update your MCP client configuration to use the production URL.

Extend your MCP server by registering additional tools. Here's an example that queries your Supabase database:

You can find ready-to-use MCP server implementations here:

**Examples:**

Example 1 (unknown):
```unknown
1mkdir my-mcp-server2cd my-mcp-server3supabase init
```

Example 2 (unknown):
```unknown
1supabase functions new mcp
```

Example 3 (unknown):
```unknown
1{2  "imports": {3    "@hono/mcp": "npm:@hono/mcp@^0.1.1",4    "@modelcontextprotocol/sdk": "npm:@modelcontextprotocol/sdk@^1.24.3",5    "hono": "npm:hono@^4.9.2",6    "zod": "npm:zod@^4.1.13"7  }8}
```

Example 4 (python):
```python
1// Setup type definitions for built-in Supabase Runtime APIs2import 'jsr:@supabase/functions-js/edge-runtime.d.ts'34import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'5import { StreamableHTTPTransport } from '@hono/mcp'6import { Hono } from 'hono'7import { z } from 'zod'89// Create Hono app10const app = new Hono()1112// Create your MCP server13const server = new McpServer({14  name: 'mcp',15  version: '0.1.0',16})1718// Register a simple addition tool19server.registerTool(20  'add',21  {22    title: 'Addition Tool',23    description: 'Add two numbers together',24    inputSchema: { a: z.number(), b: z.number() },25  },26  ({ a, b }) => ({27    content: [{ type: 'text', text: String(a + b) }],28  })29)3031// Handle MCP requests at the root path32app.all('/', async (c) => {33  const transport = new StreamableHTTPTransport()34  await server.connect(transport)35  return transport.handleRequest(c)36})3738Deno.serve(app.fetch)
```

---

## Use Supabase with Refine | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/quickstarts/refine

**Contents:**
- Use Supabase with Refine
- Learn how to create a Supabase project, add some sample data to your database, and query the data from a Refine app.
  - Create a Supabase project
  - Create a Refine app
        - Terminal
  - Open your Refine app in VS Code
        - Terminal
  - Start the app
        - Terminal
  - Update `supabaseClient`

Use Supabase with Refine

Learn how to create a Supabase project, add some sample data to your database, and query the data from a Refine app.

Go to database.new and create a new Supabase project.

Alternatively, you can create a project using the Management API:

When your project is up and running, go to the Table Editor, create a new table and insert some data.

Alternatively, you can run the following snippet in your project's SQL Editor. This will create a instruments table with some sample data.

Make the data in your table publicly readable by adding an RLS policy:

Create a Refine app using the create refine-app.

The refine-supabase preset adds @refinedev/supabase supplementary package that supports Supabase in a Refine app. @refinedev/supabase out-of-the-box includes the Supabase dependency: supabase-js.

You will develop your app, connect to the Supabase backend and run the Refine app in VS Code.

Start the app, go to http://localhost:5173 in a browser, and you should be greeted with the Refine Welcome page.

You now have to update the supabaseClient with the SUPABASE_URL and SUPABASE_KEY of your Supabase API. The supabaseClient is used in auth provider and data provider methods that allow the Refine app to connect to your Supabase backend.

You can also get the Project URL and key from the project's Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

You have to then configure resources and define pages for instruments resource.

Use the following command to automatically add resources and generate code for pages for instruments using Refine Inferencer.

This defines pages for list, create, show and edit actions inside the src/pages/instruments/ directory with <HeadlessInferencer /> component.

The <HeadlessInferencer /> component depends on @refinedev/react-table and @refinedev/react-hook-form packages. In order to avoid errors, you should install them as dependencies with npm install @refinedev/react-table @refinedev/react-hook-form.

The <HeadlessInferencer /> is a Refine Inferencer component that automatically generates necessary code for the list, create, show and edit pages.

More on how the Inferencer works is available in the docs here.

Add routes for the list, create, show, and edit pages.

You should remove the index route for the Welcome page presented with the <Welcome /> component.

Now you should be able to see the instruments pages along the /instruments routes. You may now edit and add new instruments using the Inferencer generated UI.

The Inferencer auto-generated code gives you a good starting point on which to keep building your list, create, show and edit pages. They can be obtained by clicking the Show the auto-generated code buttons in their respective pages.

**Examples:**

Example 1 (unknown):
```unknown
1# First, get your access token from https://supabase.com/dashboard/account/tokens2export SUPABASE_ACCESS_TOKEN="your-access-token"34# List your organizations to get the organization ID5curl -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \6  https://api.supabase.com/v1/organizations78# Create a new project (replace <org-id> with your organization ID)9curl -X POST https://api.supabase.com/v1/projects \10  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \11  -H "Content-Type: application/json" \12  -d '{13    "organization_id": "<org-id>",14    "name": "My Project",15    "region": "us-east-1",16    "db_pass": "<your-secure-password>"17  }'
```

Example 2 (unknown):
```unknown
1-- Create the table2create table instruments (3  id bigint primary key generated always as identity,4  name text not null5);6-- Insert some sample data into the table7insert into instruments (name)8values9  ('violin'),10  ('viola'),11  ('cello');1213alter table instruments enable row level security;
```

Example 3 (unknown):
```unknown
1create policy "public can read instruments"2on public.instruments3for select to anon4using (true);
```

Example 4 (unknown):
```unknown
1npm create refine-app@latest -- --preset refine-supabase my-app
```

---

## Quickstart | Supabase Docs

**URL:** https://supabase.com/docs/guides/queues/quickstart

**Contents:**
- Quickstart
- Learn how to use Supabase Queues to add and read messages
- Concepts#
  - Pull-Based Queue#
  - Message#
  - Queue types#
- Create Queues#
  - What happens when you create a queue?#
- Expose Queues to client-side consumers#
  - Enable RLS on your tables in pgmq schema#

Learn how to use Supabase Queues to add and read messages

This guide is an introduction to interacting with Supabase Queues via the Dashboard and official client library. Check out Queues API Reference for more details on our API.

Supabase Queues is a pull-based Message Queue consisting of three main components: Queues, Messages, and Queue Types.

A pull-based Queue is a Message storage and delivery system where consumers actively fetch Messages when they're ready to process them - similar to constantly refreshing a webpage to display the latest updates. Our pull-based Queues process Messages in a First-In-First-Out (FIFO) manner without priority levels.

A Message in a Queue is a JSON object that is stored until a consumer explicitly processes and removes it, like a task waiting in a to-do list until someone checks and completes it.

Supabase Queues offers three types of Queues:

Basic Queue: A durable Queue that stores Messages in a logged table.

Unlogged Queue: A transient Queue that stores Messages in an unlogged table for better performance but may result in loss of Queue Messages.

Partitioned Queue (Coming Soon): A durable and scalable Queue that stores Messages in multiple table partitions for better performance.

To get started, navigate to the Supabase Queues Postgres Module under Integrations in the Dashboard and enable the pgmq extension.

pgmq extension is available in Postgres version 15.6.1.143 or later.

If you've already created a Queue click the Create a queue button instead.

Queue names can only be lowercase and hyphens and underscores are permitted.

Every new Queue creates two tables in the pgmq schema. These tables are pgmq.q_<queue_name> to store and process active messages and pgmq.a_<queue_name> to store any archived messages.

A "Basic Queue" will create pgmq.q_<queue_name> and pgmq.a_<queue_name> tables as logged tables.

However, an "Unlogged Queue" will create pgmq.q_<queue_name> as an unlogged table for better performance while sacrificing durability. The pgmq.a_<queue_name> table will still be created as a logged table so your archived messages remain safe and secure.

Queues, by default, are not exposed over Supabase Data API and are only accessible via Postgres clients.

However, you may grant client-side consumers access to your Queues by enabling the Supabase Data API and granting permissions to the Queues API, which is a collection of database functions in the pgmq_public schema that wraps the database functions in the pgmq schema.

This is to prevent direct access to the pgmq schema and its tables (RLS is not enabled by default on any tables) and database functions.

To get started, navigate to the Queues Settings page and toggle on “Expose Queues via PostgREST”. Once enabled, Supabase creates and exposes a pgmq_public schema containing database function wrappers to a subset of pgmq's database functions.

For security purposes, you must enable Row Level Security (RLS) on all Queue tables (all tables in pgmq schema that begin with q_) if the Data API is enabled.

You’ll want to create RLS policies for any Queues you want your client-side consumers to interact with.

On top of enabling RLS and writing RLS policies on the underlying Queue tables, you must grant the correct permissions to the pgmq_public database functions for each Data API role.

The permissions required for each Queue API database function:

To manage your queue permissions, click on the Queue Settings button.

Then enable the required roles permissions.

postgres and service_role roles should never be exposed client-side.

Once your Queue has been created, you can begin enqueueing and dequeueing Messages.

**Examples:**

Example 1 (python):
```python
1import { createClient } from '@supabase/supabase-js'23const supabaseUrl = 'supabaseURL'4const supabaseKey = 'supabaseKey'56const supabase = createClient(supabaseUrl, supabaseKey)78const QueuesTest: React.FC = () => {9  //Add a Message10  const sendToQueue = async () => {11    const result = await supabase.schema('pgmq_public').rpc('send', {12      queue_name: 'foo',13      message: { hello: 'world' },14      sleep_seconds: 30,15    })16    console.log(result)17  }1819  //Dequeue Message20  const popFromQueue = async () => {21    const result = await supabase.schema('pgmq_public').rpc('pop', { queue_name: 'foo' })22    console.log(result)23  }2425  return (26    <div className="p-6">27      <h2 className="text-2xl font-bold mb-4">Queue Test Component</h2>28      <button29        onClick={sendToQueue}30        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 mr-4"31      >32        Add Message33      </button>34      <button35        onClick={popFromQueue}36        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"37      >38        Pop Message39      </button>40    </div>41  )42}4344export default QueuesTest
```

---

## Quickstart | Supabase Docs

**URL:** https://supabase.com/docs/guides/cron/quickstart

**Contents:**
- Quickstart
- Schedule a job#
- Edit a job#
- Activate/Deactivate a job#
- Unschedule a job#
- Inspecting job runs#
- Examples#
  - Delete data every week#
  - Run a vacuum every day#
  - Call a database function every 5 minutes#

Job names are case sensitive and cannot be edited once created.

Attempting to create a second Job with the same name (and case) will overwrite the first Job.

You can input seconds for your Job schedule interval as long as you're on Postgres version 15.1.1.61 or later.

Delete old data every Saturday at 3:30AM (GMT):

Vacuum every day at 3:00AM (GMT):

Create a hello_world() database function and then call it every 5 minutes:

To use a stored procedure, you can call it like this:

Make a POST request to a Supabase Edge Function every 30 seconds:

This requires the pg_net extension to be enabled.

Be extremely careful when setting up Jobs for system maintenance tasks as they can have unintended consequences.

For instance, scheduling a command to terminate idle connections with pg_terminate_backend(pid) can disrupt critical background processes like nightly backups. Often, there is an existing Postgres setting, such as idle_session_timeout, that can perform these common maintenance tasks without the risk.

Reach out to Supabase Support if you're unsure if that applies to your use case.

**Examples:**

Example 1 (unknown):
```unknown
1select cron.schedule (2  'saturday-cleanup', -- name of the cron job3  '30 3 * * 6', -- Saturday at 3:30AM (GMT)4  $$ delete from events where event_time < now() - interval '1 week' $$5);
```

Example 2 (unknown):
```unknown
1select cron.schedule('nightly-vacuum', '0 3 * * *', 'VACUUM');
```

Example 3 (unknown):
```unknown
1select cron.schedule('call-db-function', '*/5 * * * *', 'SELECT hello_world()');
```

Example 4 (unknown):
```unknown
1select cron.schedule('call-db-procedure', '*/5 * * * *', 'CALL my_procedure()');
```

---

## Build a User Management App with SvelteKit | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/tutorials/with-sveltekit

**Contents:**
- Build a User Management App with SvelteKit
- Project setup#
  - Create a project#
  - Set up the database schema#
  - Get API details#
      - Changes to API keys
- Building the app#
  - Initialize a Svelte app#
  - App styling (optional)#
  - Creating a Supabase client for SSR#

Build a User Management App with SvelteKit

This tutorial demonstrates how to build a basic user management app. The app authenticates and identifies the user, stores their profile information in the database, and allows the user to log in, update their profile details, and upload a profile photo. The app uses:

If you get stuck while working through this guide, refer to the full example on GitHub.

Before you start building you need to set up the Database and API. You can do this by starting a new Project in Supabase and then creating a "schema" inside the database.

Now set up the database schema. You can use the "User Management Starter" quickstart in the SQL Editor, or you can copy/paste the SQL from below and run it.

You can pull the database schema down to your local project by running the db pull command. Read the local development docs for detailed instructions.

Now that you've created some database tables, you are ready to insert data using the auto-generated API.

To do this, you need to get the Project URL and key from the project Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Start building the Svelte app from scratch.

Use the SvelteKit Skeleton Project to initialize an app called supabase-sveltekit (for this tutorial, select "SvelteKit minimal" and use TypeScript):

Then install the Supabase client library: supabase-js

And finally, save the environment variables in a .env file. All you need are the PUBLIC_SUPABASE_URL and the key that you copied earlier.

An optional step is to update the CSS file src/styles.css to make the app look nice. You can find the full contents of this file in the example repository.

The ssr package configures Supabase to use Cookies, which are required for server-side languages and frameworks.

Install the SSR package:

Creating a Supabase client with the ssr package automatically configures it to use Cookies. This means the user's session is available throughout the entire SvelteKit stack - page, layout, server, and hooks.

Add the code below to a src/hooks.server.ts file to initialize the client on the server:

Note that auth.getSession reads the auth token and the unencoded session data from the local storage medium. It doesn't send a request back to the Supabase Auth server unless the local session is expired.

You should never trust the unencoded session data if you're writing server code, since it could be tampered with by the sender. If you need verified, trustworthy user data, call auth.getUser instead, which always makes a request to the Auth server to fetch trusted data.

As this tutorial uses TypeScript the compiler complains about event.locals.supabase and event.locals.safeGetSession, you can fix this by updating the src/app.d.ts with the content below:

Create a new src/routes/+layout.server.ts file to handle the session on the server-side.

Start the dev server (npm run dev) to generate the ./$types files we are referencing in our project.

Create a new src/routes/+layout.ts file to handle the session and the supabase object on the client-side.

Create src/routes/+layout.svelte:

Create a magic link login/signup page for your application by updating the routes/+page.svelte file:

Create a src/routes/+page.server.ts file that handles the magic link form when submitted.

Change the email template to support a server-side authentication flow.

Before we proceed, let's change the email template to support sending a token hash:

Did you know? You can also customize emails sent out to new users, including the email's looks, content, and query parameters. Check out the settings of your project.

As this is a server-side rendering (SSR) environment, you need to create a server endpoint responsible for exchanging the token_hash for a session.

The following code snippet performs the following steps:

If there is an error with confirming the token, redirect the user to an error page.

After a user signs in, they need to be able to edit their profile details page. Create a new src/routes/account/+page.svelte file with the content below.

Now, create the associated src/routes/account/+page.server.ts file that handles loading data from the server through the load function and handle all form actions through the actions object.

With all the pages in place, run this command in a terminal:

And then open the browser to localhost:5173 and you should see the completed app.

Every Supabase project is configured with Storage for managing large files like photos and videos.

Create an avatar for the user so that they can upload a profile photo. Start by creating a new component called Avatar.svelte in the src/routes/account directory:

Add the widget to the Account page:

At this stage you have a fully functional application!

**Examples:**

Example 1 (unknown):
```unknown
1supabase link --project-ref <project-id>2# You can get <project-id> from your project's dashboard URL: https://supabase.com/dashboard/project/<project-id>3supabase db pull
```

Example 2 (unknown):
```unknown
1npx sv create supabase-sveltekit2cd supabase-sveltekit3npm install
```

Example 3 (unknown):
```unknown
1npm install @supabase/supabase-js
```

Example 4 (unknown):
```unknown
1PUBLIC_SUPABASE_URL="YOUR_SUPABASE_URL"2PUBLIC_SUPABASE_PUBLISHABLE_KEY="YOUR_SUPABASE_PUBLISHABLE_KEY"
```

---

## Build a Social Auth App with Expo React Native | Supabase Docs

**URL:** https://supabase.com/docs/guides/auth/quickstarts/with-expo-react-native-social-auth

**Contents:**
- Build a Social Auth App with Expo React Native
- Project setup#
  - Create a project#
  - Set up the database schema#
  - Get API details#
      - Changes to API keys
- Building the app#
  - Initialize a React Native app#
  - Set up environment variables#
  - Set up protected navigation#

Build a Social Auth App with Expo React Native

This tutorial demonstrates how to build a React Native app with Expo that implements social authentication. The app showcases a complete authentication flow with protected navigation using:

If you get stuck while working through this guide, refer to the full example on GitHub.

Before you start building you need to set up the Database and API. You can do this by starting a new Project in Supabase and then creating a "schema" inside the database.

Now set up the database schema. You can use the "User Management Starter" quickstart in the SQL Editor, or you can copy/paste the SQL from below and run it.

You can pull the database schema down to your local project by running the db pull command. Read the local development docs for detailed instructions.

Now that you've created some database tables, you are ready to insert data using the auto-generated API.

To do this, you need to get the Project URL and key from the project Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Start by building the React Native app from scratch.

Use Expo to initialize an app called expo-social-auth with the standard template:

Install the additional dependencies:

Now, create a helper file to initialize the Supabase client for both web and React Native platforms using platform-specific storage adapters: Expo SecureStore for mobile and AsyncStorage for web.

You need the API URL and the anon key copied earlier. These variables are safe to expose in your Expo app since Supabase has Row Level Security enabled on your database.

Create a .env file containing these variables:

Next, you need to protect app navigation to prevent unauthenticated users from accessing protected routes. Use the Expo SplashScreen to display a loading screen while fetching the user profile and verifying authentication status.

Create a React context to manage the authentication session, making it accessible from any component:

Next, create a provider component to manage the authentication session throughout the app:

Create a SplashScreenController component to display the Expo SplashScreen while the authentication session is loading:

Create a logout button component to handle user sign-out:

And add it to the app/(tabs)/index.tsx file used to display the user profile data and the logout button:

Next, create a basic login screen component:

Wrap the navigation with the AuthProvider and SplashScreenController.

Using Expo Router's protected routes, you can secure navigation:

You can now test the app by running:

Verify that the app works as expected. The splash screen displays while fetching the user profile, and the login page appears even when attempting to navigate to the home screen using the Link button.

By default Supabase Auth requires email verification before a session is created for the user. To support email verification you need to implement deep link handling!

While testing, you can disable email confirmation in your project's email auth provider settings.

Now integrate social authentication with Supabase Auth, starting with Apple authentication. If you only need to implement Google authentication, you can skip to the Google authentication section.

Start by adding the button inside the login screen:

For Apple authentication, you can choose between:

For either option, you need to obtain a Service ID from the Apple Developer Console.

To enable Apple sign-up on Android and Web, you also need to register the tunnelled URL (e.g., https://arnrer1-anonymous-8081.exp.direct) obtained by running:

And add it to the Redirect URLs field in your Supabase dashboard Authentication configuration.

For more information, follow the Supabase Login with Apple guide.

Before proceeding, ensure you have followed the Invertase prerequisites documented in the Invertase Initial Setup Guide and the Invertase Android Setup Guide.

You need to add two new environment variables to the .env file:

Install the @invertase/react-native-apple-authentication library:

Then create the iOS specific button component AppleSignInButton:

To test functionality on the simulator, remove the getCredentialStateForUser check:

Enable the Apple authentication capability in iOS:

Add the capabilities to the Info.plist file by following the Expo documentation.

Before testing the app, if you've already built the iOS app, clean the project artifacts:

If issues persist, try completely cleaning the cache, as reported by many users in this closed issue.

Finally, update the iOS project by installing the Pod library and running the Expo prebuild command:

Now test the application on a physical device:

You should see the login screen with the Apple authentication button.

If you get stuck while working through this guide, refer to the full Invertase example on GitHub.

Install the required libraries:

Next, create the Android-specific AppleSignInButton component:

You should now be able to test the authentication by running it on a physical device or simulator:

Start by adding the button to the login screen:

For Google authentication, you can choose between the following options:

The GN Google Sign In Free doesn't support iOS or Android, as it doesn't allow to pass a custom nonce to the sign-in request.

For either option, you need to obtain a Web Client ID from the Google Cloud Engine, as explained in the Google Sign In guide.

This guide only uses the @react-oauth/google@latest option for the Web, and the signInWithOAuth for the mobile platforms.

Before proceeding, add a new environment variable to the .env file:

Install the @react-oauth/google library:

Enable the expo-web-browser plugin in app.json:

Then create the iOS specific button component GoogleSignInButton:

Test the authentication in your browser using the tunnelled HTTPS URL:

To allow the Google Sign In to work, as you did before for Apple, you need to register the tunnelled URL (e.g., https://arnrer1-anonymous-8081.exp.direct) obtained to the Authorized JavaScript origins list of your Google Cloud Console's OAuth 2.0 Client IDs configuration.

**Examples:**

Example 1 (unknown):
```unknown
1supabase link --project-ref <project-id>2# You can get <project-id> from your project's dashboard URL: https://supabase.com/dashboard/project/<project-id>3supabase db pull
```

Example 2 (unknown):
```unknown
1npx create-expo-app@latest23cd expo-social-auth
```

Example 3 (unknown):
```unknown
1npx expo install @supabase/supabase-js @react-native-async-storage/async-storage expo-secure-store expo-splash-screen
```

Example 4 (python):
```python
1import AsyncStorage from '@react-native-async-storage/async-storage';2import { createClient } from '@supabase/supabase-js';3import 'react-native-url-polyfill/auto';45const ExpoWebSecureStoreAdapter = {6  getItem: (key: string) => {7    console.debug("getItem", { key })8    return AsyncStorage.getItem(key)9  },10  setItem: (key: string, value: string) => {11    return AsyncStorage.setItem(key, value)12  },13  removeItem: (key: string) => {14    return AsyncStorage.removeItem(key)15  },16};1718export const supabase = createClient(19  process.env.EXPO_PUBLIC_SUPABASE_URL ?? '',20  process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY ?? '',21  {22    auth: {23      storage: ExpoWebSecureStoreAdapter,24      autoRefreshToken: true,25      persistSession: true,26      detectSessionInUrl: false,27    },28  },29);
```

---

## Use Supabase with Nuxt | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/quickstarts/nuxtjs

**Contents:**
- Use Supabase with Nuxt
- Learn how to create a Supabase project, add some sample data to your database, and query the data from a Nuxt app.
  - Create a Supabase project
  - Create a Nuxt app
      - Explore drop-in UI components for your Supabase app.
        - Terminal
  - Install the Supabase client library
        - Terminal
  - Declare Supabase Environment Variables
        - Project URL

Use Supabase with Nuxt

Learn how to create a Supabase project, add some sample data to your database, and query the data from a Nuxt app.

Go to database.new and create a new Supabase project.

Alternatively, you can create a project using the Management API:

When your project is up and running, go to the Table Editor, create a new table and insert some data.

Alternatively, you can run the following snippet in your project's SQL Editor. This will create a instruments table with some sample data.

Make the data in your table publicly readable by adding an RLS policy:

Create a Nuxt app using the npx nuxi command.

UI components built on shadcn/ui that connect to Supabase via a single command.

The fastest way to get started is to use the supabase-js client library which provides a convenient interface for working with Supabase from a Nuxt app.

Navigate to the Nuxt app and install supabase-js.

Create a .env file and populate with your Supabase connection variables:

You can also get the Project URL and key from the project's Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

In app.vue, create a Supabase client using your config values and replace the existing content with the following code.

Start the app, navigate to http://localhost:3000 in the browser, open the browser console, and you should see the list of instruments.

The community-maintained @nuxtjs/supabase module provides an alternate DX for working with Supabase in Nuxt.

**Examples:**

Example 1 (unknown):
```unknown
1# First, get your access token from https://supabase.com/dashboard/account/tokens2export SUPABASE_ACCESS_TOKEN="your-access-token"34# List your organizations to get the organization ID5curl -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \6  https://api.supabase.com/v1/organizations78# Create a new project (replace <org-id> with your organization ID)9curl -X POST https://api.supabase.com/v1/projects \10  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \11  -H "Content-Type: application/json" \12  -d '{13    "organization_id": "<org-id>",14    "name": "My Project",15    "region": "us-east-1",16    "db_pass": "<your-secure-password>"17  }'
```

Example 2 (unknown):
```unknown
1-- Create the table2create table instruments (3  id bigint primary key generated always as identity,4  name text not null5);6-- Insert some sample data into the table7insert into instruments (name)8values9  ('violin'),10  ('viola'),11  ('cello');1213alter table instruments enable row level security;
```

Example 3 (unknown):
```unknown
1create policy "public can read instruments"2on public.instruments3for select to anon4using (true);
```

Example 4 (unknown):
```unknown
1npx nuxi@latest init my-app
```

---

## Storage Quickstart | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/quickstart

**Contents:**
- Storage Quickstart
- Learn how to use Supabase to store and serve files.
- Concepts#
  - Files#
  - Folders#
  - Buckets#
- Create a bucket#
- Upload a file#
- Download a file#
- Add security rules#

Learn how to use Supabase to store and serve files.

This guide shows the basic functionality of Supabase Storage. Find a full example application on GitHub.

Supabase Storage consists of Files, Folders, and Buckets.

Files can be any sort of media file. This includes images, GIFs, and videos. It is best practice to store files outside of your database because of their sizes. For security, HTML files are returned as plain text.

Folders are a way to organize your files (just like on your computer). There is no right or wrong way to organize your files. You can store them in whichever folder structure suits your project.

Buckets are distinct containers for files and folders. You can think of them like "super folders". Generally you would create distinct buckets for different Security and Access Rules. For example, you might keep all video files in a "video" bucket, and profile pictures in an "avatar" bucket.

File, Folder, and Bucket names must follow AWS object key naming guidelines and avoid use of any other characters.

You can create a bucket using the Supabase Dashboard. Since the storage is interoperable with your Postgres database, you can also use SQL or our client libraries. Here we create a bucket called "avatars":

You can upload a file from the Dashboard, or within a browser using our JS libraries.

You can download a file from the Dashboard, or within a browser using our JS libraries.

To restrict access to your files you can use either the Dashboard or SQL.

---

## Use Supabase with SolidJS | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/quickstarts/solidjs

**Contents:**
- Use Supabase with SolidJS
- Learn how to create a Supabase project, add some sample data to your database, and query the data from a SolidJS app.
  - Create a Supabase project
  - Create a SolidJS app
        - Terminal
  - Install the Supabase client library
        - Terminal
  - Declare Supabase Environment Variables
        - Project URL
        - Publishable key

Use Supabase with SolidJS

Learn how to create a Supabase project, add some sample data to your database, and query the data from a SolidJS app.

Go to database.new and create a new Supabase project.

Alternatively, you can create a project using the Management API:

When your project is up and running, go to the Table Editor, create a new table and insert some data.

Alternatively, you can run the following snippet in your project's SQL Editor. This will create a instruments table with some sample data.

Make the data in your table publicly readable by adding an RLS policy:

Create a SolidJS app using the degit command.

The fastest way to get started is to use the supabase-js client library which provides a convenient interface for working with Supabase from a SolidJS app.

Navigate to the SolidJS app and install supabase-js.

Create a .env.local file and populate with your Supabase connection variables:

You can also get the Project URL and key from the project's Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

In App.jsx, create a Supabase client to fetch the instruments data.

Add a getInstruments function to fetch the data and display the query result to the page.

Start the app and go to http://localhost:3000 in a browser and you should see the list of instruments.

**Examples:**

Example 1 (unknown):
```unknown
1# First, get your access token from https://supabase.com/dashboard/account/tokens2export SUPABASE_ACCESS_TOKEN="your-access-token"34# List your organizations to get the organization ID5curl -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \6  https://api.supabase.com/v1/organizations78# Create a new project (replace <org-id> with your organization ID)9curl -X POST https://api.supabase.com/v1/projects \10  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \11  -H "Content-Type: application/json" \12  -d '{13    "organization_id": "<org-id>",14    "name": "My Project",15    "region": "us-east-1",16    "db_pass": "<your-secure-password>"17  }'
```

Example 2 (unknown):
```unknown
1-- Create the table2create table instruments (3  id bigint primary key generated always as identity,4  name text not null5);6-- Insert some sample data into the table7insert into instruments (name)8values9  ('violin'),10  ('viola'),11  ('cello');1213alter table instruments enable row level security;
```

Example 3 (unknown):
```unknown
1create policy "public can read instruments"2on public.instruments3for select to anon4using (true);
```

Example 4 (unknown):
```unknown
1npx degit solidjs/templates/js my-app
```

---

## OrioleDB Overview | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/orioledb

**Contents:**
- OrioleDB Overview
- Concepts#
  - Index-organized tables#
  - No buffer mapping#
  - Undo log#
  - Copy-on-write checkpoints#
- Usage#
  - Creating OrioleDB project#
  - Creating tables#
  - Creating indexes#

The OrioleDB Postgres extension provides a drop-in replacement storage engine for the default heap storage method. It is designed to improve Postgres' scalability and performance.

OrioleDB addresses PostgreSQL's scalability limitations by removing bottlenecks in the shared memory cache under high concurrency. It also optimizes write-ahead-log (WAL) insertion through row-level WAL logging. These changes lead to significant improvements in the industry standard TPC-C benchmark, which approximates a real-world transactional workload. The following benchmark was performed on a c7g.metal instance and shows OrioleDB's performance outperforming the default Postgres heap method with a 3.3x speedup.

OrioleDB is in active development and currently has certain limitations. Currently, only B-tree indexes are supported, so features like pg_vector's HNSW indexes are not yet available. An Index Access Method bridge to unlock support for all index types used with heap storage is under active development. In the Supabase OrioleDB image the default storage method has been updated to use OrioleDB, granting better performance out of the box.

OrioleDB uses index-organized tables, where table data is stored in the index structure. This design eliminates the need for separate heap storage, reduces overhead and improves lookup performance for primary key queries.

In-memory pages are connected to the storage pages using direct links. This allows OrioleDB to bypass PostgreSQL's shared buffer pool and eliminate the associated complexity and contention in buffer mapping.

Multi-Version Concurrency Control (MVCC) is implemented using an undo log. The undo log stores previous row versions and transaction information, which enables consistent reads while removing the need for table vacuuming completely.

OrioleDB implements copy-on-write checkpoints to persist data efficiently. This approach writes only modified data during a checkpoint, reducing the I/O overhead compared to traditional Postgres checkpointing and allowing row-level WAL logging.

You can get started with OrioleDB by enabling the extension in your Supabase dashboard. To get started with OrioleDB you need to create a new Supabase project and choose OrioleDB Public Alpha Postgres version.

To create a table using the OrioleDB storage engine just execute the standard CREATE TABLE statement. By default it will create a table using OrioleDB storage engine. For example:

OrioleDB tables always have a primary key. If it wasn't defined explicitly, a hidden primary key is created using the ctid column. Additionally you can create secondary indexes.

Currently, only B-tree indexes are supported, so features like pg_vector's HNSW indexes are not yet available.

You can query and modify data in OrioleDB tables using standard SQL statements, including SELECT, INSERT, UPDATE, DELETE and INSERT ... ON CONFLICT.

You can see the execution plan using standard EXPLAIN statement.

**Examples:**

Example 1 (unknown):
```unknown
1-- Create a table2create table blog_post (3  id int8 not null,4  title text not null,5  body text not null,6  author text not null,7  published_at timestamptz not null default CURRENT_TIMESTAMP,8  views bigint not null,9  primary key (id)10);
```

Example 2 (unknown):
```unknown
1-- Create an index2create index blog_post_published_at on blog_post (published_at);34create index blog_post_views on blog_post (views) where (views > 1000);
```

Example 3 (unknown):
```unknown
1INSERT INTO blog_post (id, title, body, author, views)2VALUES (1, 'Hello, World!', 'This is my first blog post.', 'John Doe', 1000);34SELECT * FROM blog_post ORDER BY published_at DESC LIMIT 10;5 id │     title     │            body             │  author  │         published_at          │ views6────┼───────────────┼─────────────────────────────┼──────────┼───────────────────────────────┼───────7  1 │ Hello, World! │ This is my first blog post. │ John Doe │ 2024-11-15 12:04:18.756824+01 │  1000
```

Example 4 (unknown):
```unknown
1EXPLAIN SELECT * FROM blog_post ORDER BY published_at DESC LIMIT 10;2                                                 QUERY PLAN3────────────────────────────────────────────────────────────────────────────────────────────────────────────4 Limit  (cost=0.15..1.67 rows=10 width=120)5   ->  Index Scan Backward using blog_post_published_at on blog_post  (cost=0.15..48.95 rows=320 width=120)67EXPLAIN SELECT * FROM blog_post WHERE id = 1;8                                    QUERY PLAN9──────────────────────────────────────────────────────────────────────────────────10 Index Scan using blog_post_pkey on blog_post  (cost=0.15..8.17 rows=1 width=120)11   Index Cond: (id = 1)1213EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM blog_post ORDER BY published_at DESC LIMIT 10;14                                                                      QUERY PLAN15──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────16 Limit  (cost=0.15..1.67 rows=10 width=120) (actual time=0.052..0.054 rows=1 loops=1)17   ->  Index Scan Backward using blog_post_published_at on blog_post  (cost=0.15..48.95 rows=320 width=120) (actual time=0.050..0.052 rows=1 loops=1)18 Planning Time: 0.186 ms19 Execution Time: 0.088 ms
```

---

## Build a User Management App with Svelte | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/tutorials/with-svelte

**Contents:**
- Build a User Management App with Svelte
- Project setup#
  - Create a project#
  - Set up the database schema#
  - Get API details#
      - Changes to API keys
- Building the app#
  - Initialize a Svelte app#
        - src/supabaseClient.ts
  - App styling (optional)#

Build a User Management App with Svelte

This tutorial demonstrates how to build a basic user management app. The app authenticates and identifies the user, stores their profile information in the database, and allows the user to log in, update their profile details, and upload a profile photo. The app uses:

If you get stuck while working through this guide, refer to the full example on GitHub.

Before you start building you need to set up the Database and API. You can do this by starting a new Project in Supabase and then creating a "schema" inside the database.

Now set up the database schema. You can use the "User Management Starter" quickstart in the SQL Editor, or you can copy/paste the SQL from below and run it.

You can pull the database schema down to your local project by running the db pull command. Read the local development docs for detailed instructions.

Now that you've created some database tables, you are ready to insert data using the auto-generated API.

To do this, you need to get the Project URL and key from the project Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Start building the Svelte app from scratch.

You can use the Vite Svelte TypeScript Template to initialize an app called supabase-svelte:

Install the only additional dependency: supabase-js

Finally, save the environment variables in a .env. All you need are the API URL and the key that you copied earlier.

Now you have the API credentials in place, create a helper file to initialize the Supabase client. These variables will be exposed on the browser, and that's fine since you have Row Level Security enabled on the Database.

Optionally, update the CSS file src/app.css to make the app look nice. You can find the full contents of this file on GitHub.

Set up a Svelte component to manage logins and sign ups. It uses Magic Links, so users can sign in with their email without using passwords.

After a user is signed in, allow them to edit their profile details and manage their account. Create a new component for that called Account.svelte.

Now that you have all the components in place, update App.svelte:

Once that's done, run this in a terminal window:

And then open the browser to localhost:5173 and you should see the completed app.

Svelte uses Vite and the default port is 5173, Supabase uses port 3000. To change the redirection port for Supabase go to: Authentication > URL Configuration and change the Site URL to http://localhost:5173/

Every Supabase project is configured with Storage for managing large files like photos and videos.

Create an avatar for the user so that they can upload a profile photo. Start by creating a new component:

And then you can add the widget to the Account page:

At this stage you have a fully functional application!

**Examples:**

Example 1 (unknown):
```unknown
1supabase link --project-ref <project-id>2# You can get <project-id> from your project's dashboard URL: https://supabase.com/dashboard/project/<project-id>3supabase db pull
```

Example 2 (unknown):
```unknown
1npm create vite@latest supabase-svelte -- --template svelte-ts2cd supabase-svelte3npm install
```

Example 3 (unknown):
```unknown
1npm install @supabase/supabase-js
```

Example 4 (unknown):
```unknown
1VITE_SUPABASE_URL=YOUR_SUPABASE_URL2VITE_SUPABASE_PUBLISHABLE_KEY=YOUR_SUPABASE_PUBLISHABLE_KEY
```

---

## Use Supabase with Ruby on Rails | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/quickstarts/ruby-on-rails

**Contents:**
- Use Supabase with Ruby on Rails
- Learn how to create a Rails project and connect it to your Supabase Postgres database.
  - Create a Rails Project
        - Terminal
  - Set up the Postgres connection details
        - Terminal
  - Create and run a database migration
        - Terminal
  - Use the Model to interact with the database
        - Terminal

Use Supabase with Ruby on Rails

Learn how to create a Rails project and connect it to your Supabase Postgres database.

Make sure your Ruby and Rails versions are up to date, then use rails new to scaffold a new Rails project. Use the -d=postgresql flag to set it up for Postgres.

Go to the Rails docs for more details.

Go to database.new and create a new Supabase project. Save your database password securely.

When your project is up and running, navigate to your project dashboard and click on Connect.

Look for the Session Pooler connection string and copy the string. You will need to replace the Password with your saved database password. You can reset your database password in your Database Settings if you do not have it.

If you're in an IPv6 environment or have the IPv4 Add-On, you can use the direct connection string instead of Supavisor in Session mode.

Rails includes Active Record as the ORM as well as database migration tooling which generates the SQL migration files for you.

Create an example Article model and generate the migration files.

You can use the included Rails console to interact with the database. For example, you can create new entries or list all entries in a Model's table.

Run the development server. Go to http://127.0.0.1:3000 in a browser to see your application running.

**Examples:**

Example 1 (unknown):
```unknown
1rails new blog -d=postgresql
```

Example 2 (unknown):
```unknown
1export DATABASE_URL=postgres://postgres.xxxx:password@xxxx.pooler.supabase.com:5432/postgres
```

Example 3 (unknown):
```unknown
1bin/rails generate model Article title:string body:text2bin/rails db:migrate
```

Example 4 (unknown):
```unknown
1bin/rails console
```

---

## Use Supabase with Hono | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/quickstarts/hono

**Contents:**
- Use Supabase with Hono
- Learn how to create a Supabase project, add some sample data to your database, secure it with auth, and query the data from a Hono app.
  - Create a Hono app
        - Terminal
  - Install the Supabase client library
        - Terminal
  - Set up the required environment variables
        - Project URL
        - Publishable key
        - Anon key

Use Supabase with Hono

Learn how to create a Supabase project, add some sample data to your database, secure it with auth, and query the data from a Hono app.

Bootstrap the Hono example app from the Supabase Samples using the CLI.

The package.json file in the project includes the necessary dependencies, including @supabase/supabase-js and @supabase/ssr to help with server-side auth.

Copy the .env.example file to .env and update the values with your Supabase project URL and anon key.

Lastly, enable anonymous sign-ins in the Auth settings.

You can also get the Project URL and key from the project's Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Start the app, go to http://localhost:5173.

Learn how server side auth works with Hono.

**Examples:**

Example 1 (unknown):
```unknown
1npx supabase@latest bootstrap hono
```

Example 2 (unknown):
```unknown
1npm install
```

Example 3 (unknown):
```unknown
1cp .env.example .env
```

Example 4 (unknown):
```unknown
1npm run dev
```

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-analytics/introduction

**Contents:**
- Self-Hosting Analytics
      - Logflare Technical Docs
- Backends Supported#
- Getting Started#
- Postgres Backend Setup#
  - Configuration and Requirements#
- BigQuery Backend Setup#
  - Configuration and Requirements#
    - Setting up BigQuery Service Account#
    - Download the Service Account Keys#

The Supabase Analytics server is a Logflare self-hostable instance that manages the ingestion and query pipelines for searching and aggregating structured analytics events.

When self-hosting the Analytics server, the full logging experience matching that of the Supabase Platform is available in the Studio instance, allowing for an integrated and enhanced development experience. However, it's important to note that certain differences may arise due to the platform's infrastructure.

All Logflare technical documentation is available at https://docs.logflare.app.

The Analytics server supports either Postgres or BigQuery as the backend. The supabase-cli experience uses the Postgres backend out-of-the-box. However, the Supabase Platform uses the BigQuery backend for storing all platform logs.

When using the BigQuery backend, a BigQuery dataset is created in the provided Google Cloud project, and tables are created for each source. Log events are streamed into each table, and all queries generated by Studio or by the Logs Explorer are executed against the BigQuery API. This backend requires internet access to work, and cannot be run fully locally.

When using the Postgres backend, tables are created for each source within the provided schema (for supabase-cli, this would be _analytics). Log events received by Logflare are inserted directly into the respective tables. All BigQuery-dialect SQL queries from Studio will be handled by a translation layer within the Analytics server. This translation layer translates the query to PostgreSQL dialect, and then executes it against the Postgres database.

The Postgres backend is not yet optimized for a high volume of inserts, or for heavy query usage. Today the translation layer only handles a limited subset of the BigQuery dialect. As such, the Log Explorer may produce errors for more advanced queries when using the Postgres Backend.

The Postgres backend is recommended when familiarizing and experimenting with self-hosting Supabase. For production, we recommend using the BigQuery backend. See production recommendations for more information.

To set up logging in self-hosted Supabase, see the docker-compose example. Two compose services are required: Logflare, and Vector. Logflare is the HTTP Analytics server, while Vector is the logging pipeline to route all compose services' syslog to the Logflare sever.

Regardless of the backend chosen, the following environment variables must be set for the supabase/logflare docker image:

For all other configuration environment variables, please refer to the Logflare self-hosting documentation.

The example docker-compose uses the Postgres backend out of the box.

The BigQuery backend is a more robust and scalable backend option that is battle-tested and production ready. Use this backend if you intend to have heavy logging usage and require advanced querying features such as the Logs Explorer.

The requirements are as follows after creating the project:

You must enable billing on your Google Cloud project, as a valid billing account is required for streaming inserts.

The service account used must have sufficient permissions to insert into your Google Cloud BigQuery. Ensure that the service account has either:

You can create the service account via the web console or gcloud CLI, as per the Google Cloud documentation. In the web console, you can create the key by navigating to IAM > Service Accounts > Actions (dropdown) > Manage Keys

We recommend setting the BigQuery Admin role, as it simplifies permissions setup.

After the service account is created, you will need to create a key for the service account. This key will sign the JWTs for API requests that the Analytics server makes with BigQuery. This can be done through the IAM section in Google Cloud console.

Using the example self-hosting stack based on docker-compose, you include the logging related services using the following command

Thereafter, you can start the example stack using the following command:

Currently, all BigQuery datasets stored and managed by Analytics, whether via CLI or self-hosted, will default to the US region.

In the Docker Compose example, Vector is used for the logging pipieline, where log events are forwarded to the Analytics API for ingestion.

Please refer to the Vector configuration file when customizing your own setup.

You must ensure that the payloads matches the expected event schema structure. Without the correct structure, it would cause the Studio Logs UI features to break.

API logs rely on Kong instead of the Supabase Cloud API Gateway. Logs from Kong are not enriched with platform-only data.

Within the self-hosted setup, all logs are routed to Logflare via Vector. As Kong routes API requests to PostgREST, self-hosted or local deployments will result in Kong request logs instead. This would result in differences in the log event metadata between self-hosted API requests and Supabase Platform requests.

To self-host in a production setting, we recommend performing the following for a better experience.

Self-hosted Logflare has UI authentication disabled and is intended for exposure to the internet. We recommend restricting access to the dashboard, accessible at the /dashboard path. If dashboard access is required for managing sources, we recommend having an authentication layer, such as a VPN.

Logflare requires a Postgres database to function. However, if there is an issue with you self-hosted Postgres service, you would not be able to debug it as it would also bring Logflare down together.

The self-hosted example is only used as a minimal example on running the entire stack, however it is not recommended to use the same database server for both production and observability.

The current Postgres Ingestion backend isn't optimized for production usage. We recommend using Big Query for more heavy use cases.

We recommend using the BigQuery backend for production environments as it offers better scaling and querying/debugging experiences.

The Logflare server uses the a Base64 encryption key set on the LOGFLARE_DB_ENCRYPTION_KEY environment variable to perform encryption at rest for sensitive database columns.

To perform encryption key rotation, move the retired key to the LOGFLARE_DB_ENCRYPTION_KEY_RETIRED environment variable, and replace the LOGFLARE_DB_ENCRYPTION_KEY environement variable with the new key. Perform a server restart and check info logs for the migration to be detected and performed.

Once migration is complete, you can safely remove the retired key.

**Examples:**

Example 1 (unknown):
```unknown
1# clone the supabase/supabase repo, and run the following2cd docker3docker compose -f docker-compose.yml up
```

Example 2 (unknown):
```unknown
1# assuming you clone the supabase/supabase repo.2cd docker3docker compose -f docker-compose.yml
```

Example 3 (unknown):
```unknown
1[2  {3    "cache_duration_seconds": 42,4    "enable_auth": true,5    "inserted_at": "2021-12-31T23:34:00Z",6    "max_limit": 42,7    "name": "lorem",8    "proactive_requerying_seconds": 42,9    "query": "lorem",10    "sandboxable": true,11    "source_mapping": {},12    "token": "lorem",13    "updated_at": "2021-12-31T23:34:00Z"14  }15]
```

Example 4 (unknown):
```unknown
1{2  "cache_duration_seconds": 42,3  "enable_auth": true,4  "inserted_at": "2021-12-31T23:34:00Z",5  "max_limit": 42,6  "name": "lorem",7  "proactive_requerying_seconds": 42,8  "query": "lorem",9  "sandboxable": true,10  "source_mapping": {},11  "token": "lorem",12  "updated_at": "2021-12-31T23:34:00Z"13}
```

---

## Use Supabase with Flutter | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/quickstarts/flutter

**Contents:**
- Use Supabase with Flutter
- Learn how to create a Supabase project, add some sample data to your database, and query the data from a Flutter app.
  - Create a Supabase project
  - Create a Flutter app
        - Terminal
  - Install the Supabase client library
        - pubspec.yaml
  - Initialize the Supabase client
        - Project URL
        - Publishable key

Use Supabase with Flutter

Learn how to create a Supabase project, add some sample data to your database, and query the data from a Flutter app.

Go to database.new and create a new Supabase project.

Alternatively, you can create a project using the Management API:

When your project is up and running, go to the Table Editor, create a new table and insert some data.

Alternatively, you can run the following snippet in your project's SQL Editor. This will create a instruments table with some sample data.

Make the data in your table publicly readable by adding an RLS policy:

Create a Flutter app using the flutter create command. You can skip this step if you already have a working app.

The fastest way to get started is to use the supabase_flutter client library which provides a convenient interface for working with Supabase from a Flutter app.

Open the pubspec.yaml file inside your Flutter app and add supabase_flutter as a dependency.

Open lib/main.dart and edit the main function to initialize Supabase using your project URL and public API (anon) key:

You can also get the Project URL and key from the project's Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Use a FutureBuilder to fetch the data when the home page loads and display the query result in a ListView.

Replace the default MyApp and MyHomePage classes with the following code.

Run your app on a platform of your choosing! By default an app should launch in your web browser.

Note that supabase_flutter is compatible with web, iOS, Android, macOS, and Windows apps. Running the app on macOS requires additional configuration to set the entitlements.

Many sign in methods require deep links to redirect the user back to your app after authentication. Read more about setting deep links up for all platforms (including web) in the Flutter Mobile Guide.

In production, your Android app needs explicit permission to use the internet connection on the user's device which is required to communicate with Supabase APIs. To do this, add the following line to the android/app/src/main/AndroidManifest.xml file.

**Examples:**

Example 1 (unknown):
```unknown
1# First, get your access token from https://supabase.com/dashboard/account/tokens2export SUPABASE_ACCESS_TOKEN="your-access-token"34# List your organizations to get the organization ID5curl -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \6  https://api.supabase.com/v1/organizations78# Create a new project (replace <org-id> with your organization ID)9curl -X POST https://api.supabase.com/v1/projects \10  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \11  -H "Content-Type: application/json" \12  -d '{13    "organization_id": "<org-id>",14    "name": "My Project",15    "region": "us-east-1",16    "db_pass": "<your-secure-password>"17  }'
```

Example 2 (unknown):
```unknown
1-- Create the table2create table instruments (3  id bigint primary key generated always as identity,4  name text not null5);6-- Insert some sample data into the table7insert into instruments (name)8values9  ('violin'),10  ('viola'),11  ('cello');1213alter table instruments enable row level security;
```

Example 3 (unknown):
```unknown
1create policy "public can read instruments"2on public.instruments3for select to anon4using (true);
```

Example 4 (unknown):
```unknown
1flutter create my_app
```

---

## Build a User Management App with Vue 3 | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/tutorials/with-vue-3

**Contents:**
- Build a User Management App with Vue 3
      - Explore drop-in UI components for your Supabase app.
- Project setup#
  - Create a project#
  - Set up the database schema#
  - Get API details#
      - Changes to API keys
- Building the app#
  - Initialize a Vue 3 app#
  - Set up a login component#

Build a User Management App with Vue 3

UI components built on shadcn/ui that connect to Supabase via a single command.

This tutorial demonstrates how to build a basic user management app. The app authenticates and identifies the user, stores their profile information in the database, and allows the user to log in, update their profile details, and upload a profile photo. The app uses:

If you get stuck while working through this guide, refer to the full example on GitHub.

Before you start building you need to set up the Database and API. You can do this by starting a new Project in Supabase and then creating a "schema" inside the database.

Now set up the database schema. You can use the "User Management Starter" quickstart in the SQL Editor, or you can copy/paste the SQL from below and run it.

You can pull the database schema down to your local project by running the db pull command. Read the local development docs for detailed instructions.

Now that you've created some database tables, you are ready to insert data using the auto-generated API.

To do this, you need to get the Project URL and key from the project Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Let's start building the Vue 3 app from scratch.

We can quickly use Vite with Vue 3 Template to initialize an app called supabase-vue-3:

Then let's install the only additional dependency: supabase-js

And finally we want to save the environment variables in a .env. All we need are the API URL and the key that you copied earlier.

With the API credentials in place, create an src/supabase.js helper file to initialize the Supabase client. These variables are exposed on the browser, and that's completely fine since we have Row Level Security enabled on our Database.

Optionally, update src/style.css to style the app.

Set up an src/components/Auth.vue component to manage logins and sign ups. We'll use Magic Links, so users can sign in with their email without using passwords.

After a user is signed in we can allow them to edit their profile details and manage their account. Create a new src/components/Account.vue component to handle this.

Now that we have all the components in place, let's update App.vue:

Once that's done, run this in a terminal window:

And then open the browser to localhost:5173 and you should see the completed app.

Every Supabase project is configured with Storage for managing large files like photos and videos.

Create a new src/components/Avatar.vue component that allows users to upload profile photos:

And then we can add the widget to the Account page in src/components/Account.vue:

At this stage you have a fully functional application!

**Examples:**

Example 1 (unknown):
```unknown
1supabase link --project-ref <project-id>2# You can get <project-id> from your project's dashboard URL: https://supabase.com/dashboard/project/<project-id>3supabase db pull
```

Example 2 (unknown):
```unknown
1# npm 6.x2npm create vite@latest supabase-vue-3 --template vue34# npm 7+, extra double-dash is needed:5npm create vite@latest supabase-vue-3 -- --template vue67cd supabase-vue-3
```

Example 3 (unknown):
```unknown
1npm install @supabase/supabase-js
```

Example 4 (unknown):
```unknown
1VITE_SUPABASE_URL=YOUR_SUPABASE_URL2VITE_SUPABASE_PUBLISHABLE_KEY=YOUR_SUPABASE_PUBLISHABLE_KEY
```

---

## Use Supabase Auth with React | Supabase Docs

**URL:** https://supabase.com/docs/guides/auth/quickstarts/react

**Contents:**
- Use Supabase Auth with React
- Learn how to use Supabase Auth with React.js.
  - Create a new Supabase project
        - SQL_EDITOR
  - Create a React app
        - Terminal
  - Install the Supabase client library
        - Terminal
  - Declare Supabase Environment Variables
        - Project URL

Use Supabase Auth with React

Learn how to use Supabase Auth with React.js.

Launch a new project in the Supabase Dashboard.

Your new database has a table for storing your users. You can see that this table is currently empty by running some SQL in the SQL Editor.

Create a React app using a Vite template.

Navigate to the React app and install the Supabase libraries.

Rename .env.example to .env.local and populate with your Supabase connection variables:

You can also get the Project URL and key from the project's Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

UI components built on shadcn/ui that connect to Supabase via a single command.

In App.jsx, create a Supabase client using your Project URL and key.

You can configure the Auth component to display whenever there is no session inside supabase.auth.getSession()

Before proceeding, change the email template to support support a server-side authentication flow that sends a token hash:

Start the app, go to http://localhost:5173 in a browser, and open the browser console and you should be able to register and log in.

**Examples:**

Example 1 (unknown):
```unknown
1select * from auth.users;
```

Example 2 (unknown):
```unknown
1npm create vite@latest my-app -- --template react
```

Example 3 (unknown):
```unknown
1cd my-app && npm install @supabase/supabase-js
```

Example 4 (unknown):
```unknown
1VITE_SUPABASE_URL=your-project-url2VITE_SUPABASE_PUBLISHABLE_DEFAULT_KEY=sb_publishable_... or anon key
```

---

## Generate Embeddings | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/quickstarts/generate-text-embeddings

**Contents:**
- Generate Embeddings
- Generate text embeddings using Edge Functions.
- Build the Edge Function#
  - Set up Supabase locally
  - Create Edge Function
  - Setup Inference Session
  - Implement request handler
  - Test it!
- Next steps#

Generate text embeddings using Edge Functions.

This guide will walk you through how to generate high quality text embeddings in Edge Functions using its built-in AI inference API, so no external API is required.

Let's build an Edge Function that will accept an input string and generate an embedding for it. Edge Functions are server-side TypeScript HTTP endpoints that run on-demand closest to your users.

Make sure you have the latest version of the Supabase CLI installed.

Initialize Supabase in the root directory of your app and start your local stack.

Create an Edge Function that we will use to generate embeddings. We'll call this embed (you can name this anything you like).

This will create a new TypeScript file called index.ts under ./supabase/functions/embed.

Let's create a new inference session to be used in the lifetime of this function. Multiple requests can use the same inference session.

Currently, only the gte-small (https://huggingface.co/Supabase/gte-small) text embedding model is supported in Supabase's Edge Runtime.

Modify our request handler to accept an input string from the POST request JSON body.

Then generate the embedding by calling session.run(input).

Note the two options we pass to session.run():

To test the Edge Function, first start a local functions server.

Then in a new shell, create an HTTP request using cURL and pass in your input in the JSON body.

Be sure to replace ANON_KEY with your project's anonymous key. You can get this key by running supabase status.

**Examples:**

Example 1 (unknown):
```unknown
1supabase init2supabase start
```

Example 2 (unknown):
```unknown
1supabase functions new embed
```

Example 3 (javascript):
```javascript
1const session = new Supabase.ai.Session('gte-small');
```

Example 4 (javascript):
```javascript
1Deno.serve(async (req) => {2  // Extract input string from JSON body3  const { input } = await req.json();45  // Generate the embedding from the user input6  const embedding = await session.run(input, {7    mean_pool: true,8    normalize: true,9  });1011  // Return the embedding12  return new Response(13    JSON.stringify({ embedding }),14    { headers: { 'Content-Type': 'application/json' } }15  );16});
```

---

## Build a User Management App with Angular | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/tutorials/with-angular

**Contents:**
- Build a User Management App with Angular
- Project setup#
  - Create a project#
  - Set up the database schema#
  - Get API details#
      - Changes to API keys
- Building the app#
  - Initialize an Angular app#
  - Set up a login component#
  - Account page#

Build a User Management App with Angular

This tutorial demonstrates how to build a basic user management app. The app authenticates and identifies the user, stores their profile information in the database, and allows the user to log in, update their profile details, and upload a profile photo. The app uses:

If you get stuck while working through this guide, refer to the full example on GitHub.

Before you start building you need to set up the Database and API. You can do this by starting a new Project in Supabase and then creating a "schema" inside the database.

Now set up the database schema. You can use the "User Management Starter" quickstart in the SQL Editor, or you can copy/paste the SQL from below and run it.

You can pull the database schema down to your local project by running the db pull command. Read the local development docs for detailed instructions.

Now that you've created some database tables, you are ready to insert data using the auto-generated API.

To do this, you need to get the Project URL and key from the project Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Start with building the Angular app from scratch.

You can use the Angular CLI to initialize an app called supabase-angular. The command sets some defaults, that you change to suit your needs:

Then, install the only additional dependency: supabase-js

Finally, save the environment variables in the src/environments/environment.ts file. All you need are the API URL and the key that you copied earlier. The application exposes these variables in the browser, and that's fine as you have Row Level Security enabled on the Database.

Now you have the API credentials in place, create a SupabaseService with ng g s supabase and add the following code to initialize the Supabase client and implement functions to communicate with the Supabase API.

Optionally, update src/styles.css with the following styles to style the app.

Next, set up an Angular component to manage logins and sign ups. The component uses Magic Links, so users can sign in with their email without using passwords.

Create an AuthComponent with the ng g c auth Angular CLI command and add the following code.

Users also need a way to edit their profile details and manage their accounts after signing in. Create an AccountComponent with the ng g c account Angular CLI command and add the following code.

Now you have all the components in place, update AppComponent:

You also need to change app.module.ts to include the ReactiveFormsModule from the @angular/forms package.

Once that's done, run the application in a terminal:

Open the browser to localhost:4200 and you should see the completed app.

Every Supabase project is configured with Storage for managing large files like photos and videos.

Create an avatar for the user so that they can upload a profile photo. Create an AvatarComponent with ng g c avatar Angular CLI command and add the following code.

And then we can add the widget on top of the AccountComponent HTML template:

And add an updateAvatar function along with an avatarUrl getter to the AccountComponent typescript file:

At this stage you have a fully functional application!

**Examples:**

Example 1 (unknown):
```unknown
1supabase link --project-ref <project-id>2# You can get <project-id> from your project's dashboard URL: https://supabase.com/dashboard/project/<project-id>3supabase db pull
```

Example 2 (unknown):
```unknown
1npx ng new supabase-angular --routing false --style css --standalone false --zoneless true --ssr false2cd supabase-angular
```

Example 3 (unknown):
```unknown
1npm install @supabase/supabase-js
```

Example 4 (javascript):
```javascript
1export const environment = {2  production: false,3  supabaseUrl: 'YOUR_SUPABASE_URL',4  supabaseKey: 'YOUR_SUPABASE_KEY',5}
```

---

## Analytics Buckets | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/analytics/introduction

**Contents:**
- Analytics Buckets
- Store large datasets for analytics and reporting.
      - This feature is in alpha
- Why Analytics buckets?#
- Ideal use cases#

Store large datasets for analytics and reporting.

Expect rapid changes, limited features, and possible breaking updates. share feedback as we refine the experience and expand access.

Analytics buckets enable analytical workflows on large-scale datasets while keeping your primary database optimized for transactional operations.

Postgres tables are purpose-built for transactional workloads with frequent inserts, updates, deletes, and low-latency queries. Analytical workloads have fundamentally different requirements:

Analytics buckets address these requirements using Apache Iceberg, an open-table format specifically designed for efficient management of large analytical datasets.

Analytics buckets are perfect for:

By separating transactional and analytical workloads, Supabase lets you build scalable analytics pipelines without compromising your primary Postgres performance.

---

## JavaScript: Introduction | Supabase Docs

**URL:** https://supabase.com/docs/reference/javascript/introduction

---

## Flutter: Introduction | Supabase Docs

**URL:** https://supabase.com/docs/reference/dart/introduction

---

## Build an API route in less than 2 minutes. | Supabase Docs

**URL:** https://supabase.com/docs/guides/api/quickstart

**Contents:**
- Build an API route in less than 2 minutes.
- Create your first API route by creating a table called todos to store tasks.
  - Set up a Supabase project with a 'todos' table
  - Allow public access
  - Insert some dummy data
  - Fetch the data
- Bonus#
  - Browser#
  - Client libraries#

Build an API route in less than 2 minutes.

Create your first API route by creating a table called todos to store tasks.

Let's create our first REST route which we can query using cURL or the browser.

We'll create a database table called todos for storing tasks. This creates a corresponding API route /rest/v1/todos which can accept GET, POST, PATCH, & DELETE requests.

Create a new project in the Supabase Dashboard.

After your project is ready, create a table in your Supabase database. You can do this with either the Table interface or the SQL Editor.

Let's turn on Row Level Security for this table and allow public access.

Now we can add some data to our table which we can access through our API.

Find your API URL and Keys in your Dashboard API Settings. You can now query your "todos" table by appending /rest/v1/todos to the API URL.

Copy this block of code, substitute <PROJECT_REF> and <ANON_KEY>, then run it from a terminal.

There are several options for accessing your data:

You can query the route in your browser, by appending the anon key as a query parameter:

https://<PROJECT_REF>.supabase.co/rest/v1/todos?apikey=<ANON_KEY>

We provide a number of Client Libraries.

**Examples:**

Example 1 (unknown):
```unknown
1-- Create a table called "todos"2-- with a column to store tasks.3create table todos (4  id serial primary key,5  task text6);
```

Example 2 (unknown):
```unknown
1-- Turn on security2alter table "todos"3enable row level security;45-- Allow anonymous access6create policy "Allow public access"7  on todos8  for select9  to anon10  using (true);
```

Example 3 (unknown):
```unknown
1insert into todos (task)2values3  ('Create tables'),4  ('Enable security'),5  ('Add data'),6  ('Fetch data from the API');
```

Example 4 (unknown):
```unknown
1curl 'https://<PROJECT_REF>.supabase.co/rest/v1/todos' \2-H "apikey: <ANON_KEY>" \3-H "Authorization: Bearer <ANON_KEY>"
```

---

## Build a User Management App with React | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/tutorials/with-react

**Contents:**
- Build a User Management App with React
      - Explore drop-in UI components for your Supabase app.
- Project setup#
  - Create a project#
  - Set up the database schema#
  - Get API details#
      - Changes to API keys
- Building the app#
  - Initialize a React app#
  - App styling (optional)#

Build a User Management App with React

UI components built on shadcn/ui that connect to Supabase via a single command.

This tutorial demonstrates how to build a basic user management app. The app authenticates and identifies the user, stores their profile information in the database, and allows the user to log in, update their profile details, and upload a profile photo. The app uses:

If you get stuck while working through this guide, refer to the full example on GitHub.

Before you start building you need to set up the Database and API. You can do this by starting a new Project in Supabase and then creating a "schema" inside the database.

Now set up the database schema. You can use the "User Management Starter" quickstart in the SQL Editor, or you can copy/paste the SQL from below and run it.

You can pull the database schema down to your local project by running the db pull command. Read the local development docs for detailed instructions.

Now that you've created some database tables, you are ready to insert data using the auto-generated API.

To do this, you need to get the Project URL and key from the project Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Let's start building the React app from scratch.

We can use Vite to initialize an app called supabase-react:

Then let's install the only additional dependency: supabase-js.

And finally, save the environment variables in a .env.local file. All we need are the Project URL and the key that you copied earlier.

Now that we have the API credentials in place, let's create a helper file to initialize the Supabase client. These variables will be exposed on the browser, and that's completely fine since we have Row Level Security enabled on our Database.

Create and edit src/supabaseClient.js:

An optional step is to update the CSS file src/index.css to make the app look nice. You can find the full contents of this file here.

Let's set up a React component to manage logins and sign ups. We'll use Magic Links, so users can sign in with their email without using passwords.

Create and edit src/Auth.jsx:

After a user is signed in we can allow them to edit their profile details and manage their account.

Let's create a new component for that called src/Account.jsx.

Now that we have all the components in place, let's update src/App.jsx:

Once that's done, run this in a terminal window:

And then open the browser to localhost:5173 and you should see the completed app.

Every Supabase project is configured with Storage for managing large files like photos and videos.

Let's create an avatar for the user so that they can upload a profile photo. We can start by creating a new component:

Create and edit src/Avatar.jsx:

And then we can add the widget to the Account page at src/Account.jsx:

At this stage you have a fully functional application!

**Examples:**

Example 1 (unknown):
```unknown
1supabase link --project-ref <project-id>2# You can get <project-id> from your project's dashboard URL: https://supabase.com/dashboard/project/<project-id>3supabase db pull
```

Example 2 (unknown):
```unknown
1npm create vite@latest supabase-react -- --template react2cd supabase-react
```

Example 3 (unknown):
```unknown
1npm install @supabase/supabase-js
```

Example 4 (unknown):
```unknown
1VITE_SUPABASE_URL=YOUR_SUPABASE_URL2VITE_SUPABASE_PUBLISHABLE_KEY=YOUR_SUPABASE_PUBLISHABLE_KEY
```

---

## Postgres Extensions Overview | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/extensions

**Contents:**
- Postgres Extensions Overview
  - Enable and disable extensions#
  - Upgrade extensions#
  - Full list of extensions#

Postgres Extensions Overview

Extensions are exactly as they sound - they "extend" the database with functionality which isn't part of the Postgres core. Supabase has pre-installed some of the most useful open source extensions.

Most extensions are installed under the extensions schema, which is accessible to public by default. To avoid namespace pollution, we do not recommend creating other entities in the extensions schema.

If you need to restrict user access to tables managed by extensions, we recommend creating a separate schema for installing that specific extension.

Some extensions can only be created under a specific schema, for example, postgis_tiger_geocoder extension creates a schema named tiger. Before enabling such extensions, make sure you have not created a conflicting schema with the same name.

In addition to the pre-configured extensions, you can also install your own SQL extensions directly in the database using Supabase's SQL editor. The SQL code for the extensions, including plpgsql extensions, can be added through the SQL editor.

If a new version of an extension becomes available on Supabase, you need to initiate a software upgrade in the Infrastructure Settings to access it. Software upgrades can also be initiated by restarting your server in the General Settings.

Supabase is pre-configured with over 50 extensions and you can install additional extensions through the database.dev package manager.

You can install pure SQL extensions directly in the database using the SQL editor or any Postgres client.

If you would like to request an extension, add (or upvote) it in the GitHub Discussion.

---

## Use Supabase with Android Kotlin | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/quickstarts/kotlin

**Contents:**
- Use Supabase with Android Kotlin
- Learn how to create a Supabase project, add some sample data to your database, and query the data from an Android Kotlin app.
  - Create a Supabase project
  - Create an Android app with Android Studio
  - Install the Dependencies
  - Add internet access permission
  - Initialize the Supabase client
        - Project URL
        - Publishable key
        - Anon key

Use Supabase with Android Kotlin

Learn how to create a Supabase project, add some sample data to your database, and query the data from an Android Kotlin app.

Go to database.new and create a new Supabase project.

Alternatively, you can create a project using the Management API:

When your project is up and running, go to the Table Editor, create a new table and insert some data.

Alternatively, you can run the following snippet in your project's SQL Editor. This will create a instruments table with some sample data.

Make the data in your table publicly readable by adding an RLS policy:

Open Android Studio > New > New Android Project.

Open build.gradle.kts (app) file and add the serialization plug, Ktor client, and Supabase client.

Replace the version placeholders $kotlin_version with the Kotlin version of the project, and $supabase_version and $ktor_version with the respective latest versions.

The latest supabase-kt version can be found here and Ktor version can be found here.

Add the following line to the AndroidManifest.xml file under the manifest tag and outside the application tag.

You can create a Supabase client whenever you need to perform an API call.

For the sake of simplicity, we will create a client in the MainActivity.kt file at the top just below the imports.

Replace the supabaseUrl and supabaseKey with your own:

You can also get the Project URL and key from the project's Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Create a serializable data class to represent the data from the database.

Add the following below the createSupabaseClient function in the MainActivity.kt file.

Use LaunchedEffect to fetch data from the database and display it in a LazyColumn.

Replace the default MainActivity class with the following code.

Note that we are making a network request from our UI code. In production, you should probably use a ViewModel to separate the UI and data fetching logic.

Run the app on an emulator or a physical device by clicking the Run app button in Android Studio.

**Examples:**

Example 1 (unknown):
```unknown
1# First, get your access token from https://supabase.com/dashboard/account/tokens2export SUPABASE_ACCESS_TOKEN="your-access-token"34# List your organizations to get the organization ID5curl -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \6  https://api.supabase.com/v1/organizations78# Create a new project (replace <org-id> with your organization ID)9curl -X POST https://api.supabase.com/v1/projects \10  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \11  -H "Content-Type: application/json" \12  -d '{13    "organization_id": "<org-id>",14    "name": "My Project",15    "region": "us-east-1",16    "db_pass": "<your-secure-password>"17  }'
```

Example 2 (unknown):
```unknown
1-- Create the table2create table instruments (3  id bigint primary key generated always as identity,4  name text not null5);6-- Insert some sample data into the table7insert into instruments (name)8values9  ('violin'),10  ('viola'),11  ('cello');1213alter table instruments enable row level security;
```

Example 3 (unknown):
```unknown
1create policy "public can read instruments"2on public.instruments3for select to anon4using (true);
```

Example 4 (unknown):
```unknown
1plugins {2  ...3  kotlin("plugin.serialization") version "$kotlin_version"4}5...6dependencies {7  ...8  implementation(platform("io.github.jan-tennert.supabase:bom:$supabase_version"))9  implementation("io.github.jan-tennert.supabase:postgrest-kt")10  implementation("io.ktor:ktor-client-android:$ktor_version")11}
```

---

## Getting Started with OAuth 2.1 Server | Supabase Docs

**URL:** https://supabase.com/docs/guides/auth/oauth-server/getting-started

**Contents:**
- Getting Started with OAuth 2.1 Server
- Prerequisites#
- Overview#
- Enable OAuth 2.1 server#
- Configure your authorization path#
- Build your authorization UI#
  - Example authorization UI#
  - How it works#
- Register an OAuth client#
- Customizing tokens (optional)#

Getting Started with OAuth 2.1 Server

This guide will walk you through setting up your Supabase project as an OAuth 2.1 identity provider, from enabling the feature to registering your first client application.

Before you begin, make sure you have:

Setting up OAuth 2.1 in your Supabase project involves these steps:

Testing OAuth flows is often easier on a Supabase project since it's already accessible on the web, no tunnel or additional configuration needed.

OAuth 2.1 server is currently in beta and free to use during the beta period on all Supabase plans.

Once enabled, your project will expose the necessary OAuth endpoints:

Use asymmetric JWT signing keys for better security

By default, Supabase uses HS256 (symmetric) for signing JWTs. For OAuth use cases, we recommend migrating to asymmetric algorithms like RS256 or ES256. Asymmetric keys are more scalable and secure because:

Learn more about configuring JWT signing keys.

Note: If you plan to use OpenID Connect ID tokens (by requesting the openid scope), asymmetric signing algorithms are required. ID token generation will fail with HS256.

Before registering clients, you need to configure where your authorization UI will live.

The authorization path is combined with your Site URL (configured in Authentication > URL Configuration) to create the full authorization endpoint URL.

Your authorization UI will be at the combined Site URL + Authorization Path. For example:

When OAuth clients initiate the authorization flow, Supabase Auth will redirect users to this URL with an authorization_id query parameter. You'll use Supabase JavaScript library OAuth methods to handle the authorization:

This is where you build the frontend for your authorization flow. When third-party apps initiate OAuth, users will be redirected to your authorization path (configured in the previous step) with an authorization_id query parameter.

Your authorization UI should:

The authorization details include a scopes field that contains the scopes requested by the client (e.g., ["openid", "email", "profile"]). You should display these scopes to the user so they understand what information will be shared.

This is a frontend implementation. You're building the UI that displays the consent screen and handles user interactions. The actual OAuth token generation is handled by Supabase Auth after you call the approve/deny methods.

Here's how to build a minimal authorization page at your configured path (e.g., /oauth/consent):

Before third-party applications can use your project as an identity provider, you need to register them as OAuth clients.

Store the client secret securely. It will only be shown once. If you lose it, you can regenerate a new one from the OAuth Apps page.

By default, OAuth access tokens include standard claims like user_id, role, and client_id. If you need to customize tokens—for example, to set a specific audience claim for third-party validation or add client-specific metadata—use Custom Access Token Hooks.

Custom Access Token Hooks are triggered for all token issuance, including OAuth flows. You can use the client_id parameter to customize tokens based on which OAuth client is requesting them.

For more examples, see Token Security & RLS.

Redirect URIs are critical for OAuth security. Supabase Auth will only redirect to URIs that are explicitly registered with the client.

Not to be confused with general redirect URLs

This section is about OAuth client redirect URIs - where to send users after they authorize third-party apps to access your Supabase project. This is different from the general Redirect URLs setting, which controls where to send users after they sign in TO your app using social providers.

Exact matches only - No wildcards or patterns

OAuth client redirect URIs require exact, complete URL matches. Unlike general redirect URLs (which support wildcards), OAuth client redirect URIs do NOT support wildcards, patterns, or partial URLs. You must register the full, exact callback URL.

Now that you've registered your first OAuth client, you're ready to:

**Examples:**

Example 1 (python):
```python
1// app/oauth/consent/page.tsx2import { createServerClient } from '@supabase/ssr'3import { cookies } from 'next/headers'4import { redirect } from 'next/navigation'56export default async function ConsentPage({7  searchParams,8}: {9  searchParams: { authorization_id?: string }10}) {11  const authorizationId = searchParams.authorization_id1213  if (!authorizationId) {14    return <div>Error: Missing authorization_id</div>15  }1617  const supabase = createServerClient(18    process.env.NEXT_PUBLIC_SUPABASE_URL!,19    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,20    {21      cookies: {22        getAll: async () => (await cookies()).getAll(),23        setAll: async (cookiesToSet) => {24          const cookieStore = await cookies()25          cookiesToSet.forEach(({ name, value, options }) => cookieStore.set(name, value, options))26        },27      },28    }29  )3031  // Check if user is authenticated32  const {33    data: { user },34  } = await supabase.auth.getUser()3536  if (!user) {37    // Redirect to login, preserving authorization_id38    redirect(`/login?redirect=/oauth/consent?authorization_id=${authorizationId}`)39  }4041  // Get authorization details using the authorization_id42  const { data: authDetails, error } =43    await supabase.auth.oauth.getAuthorizationDetails(authorizationId)4445  if (error || !authDetails) {46    return <div>Error: {error?.message || 'Invalid authorization request'}</div>47  }4849  return (50    <div>51      <h1>Authorize {authDetails.client.name}</h1>52      <p>This application wants to access your account.</p>5354      <div>55        <p>56          <strong>Client:</strong> {authDetails.client.name}57        </p>58        <p>59          <strong>Redirect URI:</strong> {authDetails.redirect_uri}60        </p>61        {authDetails.scopes && authDetails.scopes.length > 0 && (62          <div>63            <strong>Requested permissions:</strong>64            <ul>65              {authDetails.scopes.map((scope) => (66                <li key={scope}>{scope}</li>67              ))}68            </ul>69          </div>70        )}71      </div>7273      <form action="/api/oauth/decision" method="POST">74        <input type="hidden" name="authorization_id" value={authorizationId} />75        <button type="submit" name="decision" value="approve">76          Approve77        </button>78        <button type="submit" name="decision" value="deny">79          Deny80        </button>81      </form>82    </div>83  )84}
```

Example 2 (python):
```python
1// app/api/oauth/decision/route.ts2import { createServerClient } from '@supabase/ssr'3import { cookies } from 'next/headers'4import { NextResponse } from 'next/server'56export async function POST(request: Request) {7  const formData = await request.formData()8  const decision = formData.get('decision')9  const authorizationId = formData.get('authorization_id') as string1011  if (!authorizationId) {12    return NextResponse.json({ error: 'Missing authorization_id' }, { status: 400 })13  }1415  const supabase = createServerClient(16    process.env.NEXT_PUBLIC_SUPABASE_URL!,17    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,18    {19      cookies: {20        getAll: async () => (await cookies()).getAll(),21        setAll: async (cookiesToSet) => {22          const cookieStore = await cookies()23          cookiesToSet.forEach(({ name, value, options }) => cookieStore.set(name, value, options))24        },25      },26    }27  )2829  if (decision === 'approve') {30    const { data, error } = await supabase.auth.oauth.approveAuthorization(authorizationId)3132    if (error) {33      return NextResponse.json({ error: error.message }, { status: 400 })34    }3536    // Redirect back to the client with authorization code37    return NextResponse.redirect(data.redirect_to)38  } else {39    const { data, error } = await supabase.auth.oauth.denyAuthorization(authorizationId)4041    if (error) {42      return NextResponse.json({ error: error.message }, { status: 400 })43    }4445    // Redirect back to the client with error46    return NextResponse.redirect(data.redirect_to)47  }48}
```

---

## Management API Reference | Supabase Docs

**URL:** https://supabase.com/docs/reference/api/introduction

**Contents:**
- Management API
- Authentication#
- Rate limits#
  - Standard rate limit#
  - Rate limit scope#
  - Rate limit response headers#
  - How rate limits are tracked#
  - Endpoint exceptions#
  - Best practices#
- Gets project performance advisors.deprecated

Manage your Supabase organizations and projects programmatically.

All API requests require an access token to be included in the Authorization header: Authorization Bearer <access_token>.

There are two ways to generate an access token:

Personal access token (PAT): PATs are long-lived tokens that you manually generate to access the Management API. They are useful for automating workflows or developing against the Management API. PATs carry the same privileges as your user account, so be sure to keep it secret.

To generate or manage your personal access tokens, visit your account page.

OAuth2: OAuth2 allows your application to generate tokens on behalf of a Supabase user, providing secure and limited access to their account without requiring their credentials. Use this if you're building a third-party app that needs to create or manage Supabase projects on behalf of your users. Tokens generated via OAuth2 are short-lived and tied to specific scopes to ensure your app can only perform actions that are explicitly approved by the user.

See Build a Supabase Integration to set up OAuth2 for your application.

All API requests must be authenticated and made over HTTPS.

Rate limits are applied to prevent abuse and ensure fair usage of the Management API. Rate limits are based on a per-user, per-scope model, meaning each user gets independent rate limits for each project and organization they interact with.

When you exceed this rate limit, all subsequent API calls will return a 429 Too Many Requests response for the remainder of the minute. Once the time window expires, your request quota resets and you can make requests again.

Rate limits are applied with per-user + per-scope isolation:

This means you can make 120 requests to Project A and 120 requests to Project B within the same minute without hitting rate limits, as they are tracked separately.

Every API response includes rate limit information in the following headers:

You can use these headers to monitor your usage and implement proactive rate limit handling before receiving a 429 response.

Your requests are identified and tracked using one of the following identifiers, in this order of priority:

Each identifier is combined with the scope (project or organization) to create a unique tracking key. This ensures that rate limits are isolated per user and per scope, preventing one project or organization from affecting another.

Some endpoints have stricter rate limits than the standard 120 requests per minute to prevent abuse of resource-intensive operations:

Note: The GET /v1/projects/:ref/database/context endpoint has dual rate limiting. You can make up to 10 requests per minute, but also no more than 1 request per second to prevent burst traffic.

The Management API is subject to our fair-use policy. All resources created via the API are subject to the pricing detailed on our Pricing pages.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Executes a SQL query on the project's logs.

Either the iso_timestamp_start and iso_timestamp_end parameters must be provided. If both are not provided, only the last 1 minute of logs will be queried. The timestamp range must be no more than 24 hours and is rounded to the nearest minute. If the range is more than 24 hours, a validation error will be thrown.

Note: Unless the sql parameter is provided, only edge_logs will be queried. See the log query docs for all available sources.

Custom SQL query to execute on the logs. See querying logs for more details.

Selects an addon variant, for example scaling the project’s compute instance up or down, and applies it to the project.

Returns the billing addons that are currently applied, including the active compute instance size, and lists every addon option that can be provisioned with pricing metadata.

Disables the selected addon variant, including rolling the compute instance back to its previous size.

Only available to selected partner OAuth apps

Authorizes the request to assume a role in the project database

Remove JIT mappings of a user, revoking all JIT database access

Returns the TypeScript types of your schema for use with supabase-js.

Only available to selected partner OAuth apps

This is an experimental endpoint. It is subject to change or removal in future versions. Use it with caution, as it may not remain supported or stable.

Mappings of roles a user can assume in the project database

Mappings of roles a user can assume in the project database

Only available to selected partner OAuth apps

Only available to selected partner OAuth apps

All entity references must be schema qualified.

Only available to selected partner OAuth apps

Rollback migrations greater or equal to this version

Modifies the roles that can be assumed and for how long

Only available to selected partner OAuth apps

Bulk update functions. It will create a new function or replace existing. The operation is idempotent. NOTE: You will need to manually bump the version.

This endpoint is deprecated - use the deploy endpoint. Creates a function and adds it to the specified project.

Boolean string, true or false

Boolean string, true or false

Deletes a function with the specified slug from the specified project.

A new endpoint to deploy functions. It will create if function does not exist.

Boolean string, true or false

Retrieves a function with the specified slug and project.

Retrieves a function body for the specified slug and project.

Returns all functions you've previously added to the specified project.

Updates a function with the specified slug and project.

Boolean string, true or false

Boolean string, true or false

Returns the total number of action runs of the specified project.

Creates a database branch from the specified project.

Deletes the specified database branch. By default, deletes immediately. Use force=false to schedule deletion with 1-hour grace period (only when soft deletion is enabled).

If set to false, schedule deletion with 1-hour grace period (only when soft deletion is enabled).

Diffs the specified database branch

Disables preview branching for the specified project

Fetches the specified database branch by its name.

Fetches configurations of the specified database branch

Returns the current status of the specified action run.

Returns the logs from the specified action run.

Returns a paginated list of action runs of the specified project.

Returns all database branches of the specified project.

Merges the specified database branch

Pushes the specified database branch

Resets the specified database branch

Cancels scheduled deletion and restores the branch to active state

Updates the configuration of the specified database branch

Updates the status of an ongoing action run.

Resource indicator for MCP (Model Context Protocol) clients

Initiates the OAuth authorization flow for the specified provider. After successful authentication, the user can claim ownership of the specified project.

Returns a list of organizations that you currently belong to.

Returns a paginated list of projects for the specified organization.

Number of projects to skip

Number of projects to return per page

Search projects by name

Sort order for projects

A comma-separated list of project statuses to filter by.

The following values are supported: ACTIVE_HEALTHY, INACTIVE.

Slug of your organization

Continent code to determine regional recommendations: NA (North America), SA (South America), EU (Europe), AF (Africa), AS (Asia), OC (Oceania), AN (Antarctica)

Desired instance size

Returns a list of all projects you've previously created.

Creates multiple secrets and adds them to the specified project.

Deletes all secrets with the given names from the specified project

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Boolean string, true or false

Returns all secrets you've previously added to the specified project.

Boolean string, true or false

Boolean string, true or false

**Examples:**

Example 1 (unknown):
```unknown
1curl https://api.supabase.com/v1/projects \2  -H "Authorization: Bearer sbp_bdd0••••••••••••••••••••••••••••••••4f23"
```

Example 2 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 3 (unknown):
```unknown
1{2  "lints": [3    {4      "name": "unindexed_foreign_keys",5      "title": "lorem",6      "level": "ERROR",7      "facing": "EXTERNAL",8      "categories": [9        "PERFORMANCE"10      ],11      "description": "lorem",12      "detail": "lorem",13      "remediation": "lorem",14      "metadata": {15        "schema": "lorem",16        "name": "lorem",17        "entity": "lorem",18        "type": "table",19        "fkey_name": "lorem",20        "fkey_columns": [21          4222        ]23      },24      "cache_key": "lorem"25    }26  ]27}
```

Example 4 (unknown):
```unknown
1{2  "result": [3    null4  ],5  "error": "lorem"6}
```

---

## Build a User Management App with Ionic Angular | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/tutorials/with-ionic-angular

**Contents:**
- Build a User Management App with Ionic Angular
- Project setup#
  - Create a project#
  - Set up the database schema#
  - Get API details#
      - Changes to API keys
- Building the app#
  - Initialize an Ionic Angular app#
  - Set up a login route#
  - Account page#

Build a User Management App with Ionic Angular

This tutorial demonstrates how to build a basic user management app. The app authenticates and identifies the user, stores their profile information in the database, and allows the user to log in, update their profile details, and upload a profile photo. The app uses:

If you get stuck while working through this guide, refer to the full example on GitHub.

Before you start building you need to set up the Database and API. You can do this by starting a new Project in Supabase and then creating a "schema" inside the database.

Now set up the database schema. You can use the "User Management Starter" quickstart in the SQL Editor, or you can copy/paste the SQL from below and run it.

You can pull the database schema down to your local project by running the db pull command. Read the local development docs for detailed instructions.

Now that you've created some database tables, you are ready to insert data using the auto-generated API.

To do this, you need to get the Project URL and key from the project Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Let's start building the Angular app from scratch.

We can use the Ionic CLI to initialize an app called supabase-ionic-angular:

Then let's install the only additional dependency: supabase-js

And finally, we want to save the environment variables in the src/environments/environment.ts file. All we need are the API URL and the key that you copied earlier. These variables will be exposed on the browser, and that's completely fine since we have Row Level Security enabled on our Database.

Now that we have the API credentials in place, let's create a SupabaseService with ionic g s supabase to initialize the Supabase client and implement functions to communicate with the Supabase API.

Let's set up a route to manage logins and signups. We'll use Magic Links so users can sign in with their email without using passwords. Create a LoginPage with the ionic g page login Ionic CLI command.

This guide will show the template inline, but the example app will have templateUrls

After a user is signed in, we can allow them to edit their profile details and manage their account. Create an AccountComponent with ionic g page account Ionic CLI command.

Now that we have all the components in place, let's update AppComponent:

Then update the AppRoutingModule

Once that's done, run this in a terminal window:

And the browser will automatically open to show the app.

Every Supabase project is configured with Storage for managing large files like photos and videos.

Let's create an avatar for the user so that they can upload a profile photo.

First, install two packages in order to interact with the user's camera.

Capacitor is a cross-platform native runtime from Ionic that enables web apps to be deployed through the app store and provides access to native device API.

Ionic PWA elements is a companion package that will polyfill certain browser APIs that provide no user interface with custom Ionic UI.

With those packages installed, we can update our main.ts to include an additional bootstrapping call for the Ionic PWA Elements.

Then create an AvatarComponent with this Ionic CLI command:

And then, we can add the widget on top of the AccountComponent HTML template:

At this stage, you have a fully functional application!

**Examples:**

Example 1 (unknown):
```unknown
1supabase link --project-ref <project-id>2# You can get <project-id> from your project's dashboard URL: https://supabase.com/dashboard/project/<project-id>3supabase db pull
```

Example 2 (unknown):
```unknown
1npm install -g @ionic/cli2ionic start supabase-ionic-angular blank --type angular3cd supabase-ionic-angular
```

Example 3 (unknown):
```unknown
1npm install @supabase/supabase-js
```

Example 4 (javascript):
```javascript
1export const environment = {2  production: false,3  supabaseUrl: 'YOUR_SUPABASE_URL',4  supabaseKey: 'YOUR_SUPABASE_KEY',5}
```

---

## Vector Buckets | Supabase Docs

**URL:** https://supabase.com/docs/guides/storage/vector/introduction

**Contents:**
- Vector Buckets
- Store, index, and query vector embeddings at scale with similarity search.
      - This feature is in alpha
- What are Vector buckets?#
- Key features#
- Ideal use cases#
- Comparison to pgvector#
- How Vector buckets work#
- Next steps#

Store, index, and query vector embeddings at scale with similarity search.

Expect rapid changes, limited features, and possible breaking updates. Share feedback as we refine the experience and expand access.

Vector buckets enable efficient storage and similarity search of vector embeddings. Built on S3-compatible storage, they provide high-performance semantic search capabilities for AI and machine learning applications.

Vector buckets are specialized storage containers optimized for vector data. Unlike traditional databases optimized for transactional queries, vector buckets use specialized indexing and distance metrics to perform fast similarity searches across millions of embeddings.

Each vector bucket contains:

Vector buckets excel at:

Vector buckets share similarities to pgvector and matches the developer experience of using pgvector as much as possible, but Vector buckets and any Foreign Data Wrappers (FDW) they use only support one similarity search algorithm, the <===> distance operator.

This makes Vector buckets ideal for:

And pgvector is ideal for:

The system automatically handles indexing and optimization, making searches fast and reliable even with millions of vectors.

Get started by learning how to create vector buckets or dive into storing vectors.

---

## Build a User Management App with SolidJS | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/tutorials/with-solidjs

**Contents:**
- Build a User Management App with SolidJS
- Project setup#
  - Create a project#
  - Set up the database schema#
  - Get API details#
      - Changes to API keys
- Building the app#
  - Initialize a SolidJS app#
  - App styling (optional)#
  - Set up a login component#

Build a User Management App with SolidJS

This tutorial demonstrates how to build a basic user management app. The app authenticates and identifies the user, stores their profile information in the database, and allows the user to log in, update their profile details, and upload a profile photo. The app uses:

If you get stuck while working through this guide, refer to the full example on GitHub.

Before you start building you need to set up the Database and API. You can do this by starting a new Project in Supabase and then creating a "schema" inside the database.

Now set up the database schema. You can use the "User Management Starter" quickstart in the SQL Editor, or you can copy/paste the SQL from below and run it.

You can pull the database schema down to your local project by running the db pull command. Read the local development docs for detailed instructions.

Now that you've created some database tables, you are ready to insert data using the auto-generated API.

To do this, you need to get the Project URL and key from the project Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Let's start building the SolidJS app from scratch.

We can use degit to initialize an app called supabase-solid:

Then let's install the only additional dependency: supabase-js

And finally we want to save the environment variables in a .env. All we need are the API URL and the key that you copied earlier.

Now that we have the API credentials in place, let's create a helper file to initialize the Supabase client. These variables will be exposed on the browser, and that's completely fine since we have Row Level Security enabled on our Database.

An optional step is to update the CSS file src/index.css to make the app look nice. You can find the full contents of this file here.

Let's set up a SolidJS component to manage logins and sign ups. We'll use Magic Links, so users can sign in with their email without using passwords.

After a user is signed in we can allow them to edit their profile details and manage their account.

Let's create a new component for that called Account.tsx.

Now that we have all the components in place, let's update App.tsx:

Once that's done, run this in a terminal window:

And then open the browser to localhost:3000 and you should see the completed app.

Every Supabase project is configured with Storage for managing large files like photos and videos.

Let's create an avatar for the user so that they can upload a profile photo. We can start by creating a new component:

And then we can add the widget to the Account page:

At this stage you have a fully functional application!

**Examples:**

Example 1 (unknown):
```unknown
1supabase link --project-ref <project-id>2# You can get <project-id> from your project's dashboard URL: https://supabase.com/dashboard/project/<project-id>3supabase db pull
```

Example 2 (unknown):
```unknown
1npx degit solidjs/templates/ts supabase-solid2cd supabase-solid
```

Example 3 (unknown):
```unknown
1npm install @supabase/supabase-js
```

Example 4 (unknown):
```unknown
1VITE_SUPABASE_URL=YOUR_SUPABASE_URL2VITE_SUPABASE_PUBLISHABLE_KEY=YOUR_SUPABASE_PUBLISHABLE_KEY
```

---

## AI Prompt: Supabase Realtime AI Assistant Guide | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/ai-prompts/use-realtime

**Contents:**
- AI Prompt: Supabase Realtime AI Assistant Guide
- How to use#
- Prompt#

AI Prompt: Supabase Realtime AI Assistant Guide

Copy the prompt to a file in your repo.

Use the "include file" feature from your AI tool to include the prompt when chatting with your AI assistant. For example, with GitHub Copilot, use #<filename>, in Cursor, use @Files, and in Zed, use /file.

**Examples:**

Example 1 (javascript):
```javascript
1# Supabase Realtime AI Assistant Guide23You are an expert developer assistant specializing in Supabase Realtime implementations. This guide provides structured, actionable patterns for AI-driven development assistance.45## Implementation Rules67### Do8- Use `broadcast` for all realtime events (database changes via triggers, messaging, notifications, game state)9- Use `presence` sparingly for user state tracking (online status, user counters)10- Create indexes for all columns used in RLS policies11- Advice to use topic names that corrolate with concepts and tables: `scope:entity` (e.g., `room:123:messages`)12- Use snake_case for event names: `entity_action` (e.g., `message_created`)13- Include unsubscribe/cleanup logic in all implementations14- Set `private: true` for channels using database triggers or RLS policies15- Give preference to use private channels over public channels (better security and control)16- Implement proper error handling and reconnection logic1718### Don't19- Use `postgres_changes` for new applications (single-threaded, doesn't scale well) and help migrate to `broadcast from database` on existing applications if necessary20- Create multiple subscriptions without proper cleanup21- Write complex RLS queries without proper indexing22- Use generic event names like "update" or "change"23- Subscribe directly in render functions without state management24- Use database functions (`realtime.send`, `realtime.broadcast_changes`) in client code2526## Function Selection Decision Table2728| Use Case | Recommended Function | Why Not postgres_changes |29|----------|---------------------|--------------------------|30| Custom payloads with business logic | `broadcast` | More flexible, better performance |31| Database change notifications | `broadcast` via database triggers | More scalable, customizable payloads |32| High-frequency updates | `broadcast` with minimal payload | Better throughput and control |33| User presence/status tracking | `presence` (sparingly) | Specialized for state synchronization |34| Simple table mirroring | `broadcast` via database triggers | More scalable, customizable payloads |35| Client to client communication | `broadcast` without triggers and using only websockets | More flexible, better performance |3637**Note:** `postgres_changes` should be avoided due to scalability limitations. Use `broadcast` with database triggers (`realtime.broadcast_changes`) for all database change notifications.3839## Scalability Best Practices4041### Dedicated Topics for Better Performance42Using dedicated, granular topics ensures messages are only sent to relevant listeners, significantly improving scalability:4344**❌ Avoid Broad Topics:**45```javascript46// This broadcasts to ALL users, even those not interested47const channel = supabase.channel('global:notifications')48```4950**✅ Use Dedicated Topics:**51```javascript52// This only broadcasts to users in a specific room53const channel = supabase.channel(`room:${roomId}:messages`)5455// This only broadcasts to a specific user56const channel = supabase.channel(`user:${userId}:notifications`)5758// This only broadcasts to users with specific permissions59const channel = supabase.channel(`admin:${orgId}:alerts`)60```6162### Benefits of Dedicated Topics:63- **Reduced Network Traffic**: Messages only reach interested clients64- **Better Performance**: Fewer unnecessary message deliveries65- **Improved Security**: Easier to implement targeted RLS policies66- **Scalability**: System can handle more concurrent users efficiently67- **Cost Optimization**: Reduced bandwidth and processing overhead6869### Topic Naming Strategy:70- **One topic per room**: `room:123:messages`, `room:123:presence`71- **One topic per user**: `user:456:notifications`, `user:456:status`72- **One topic per organization**: `org:789:announcements`73- **One topic per feature**: `game:123:moves`, `game:123:chat`7475## Naming Conventions7677### Topics (Channels)78- **Pattern:** `scope:entity` or `scope:entity:id`79- **Examples:** `room:123:messages`, `game:456:moves`, `user:789:notifications`80- **Public channels:** `public:announcements`, `global:status`8182### Events83- **Pattern:** `entity_action` (snake_case)84- **Examples:** `message_created`, `user_joined`, `game_ended`, `status_changed`85- **Avoid:** Generic names like `update`, `change`, `event`8687## Client Setup Patterns8889```javascript90// Basic setup91const supabase = createClient('URL', 'ANON_KEY')9293// Channel configuration94const channel = supabase.channel('room:123:messages', {95  config: {96    broadcast: { self: true, ack: true },97    presence: { key: 'user-session-id', enabled: true },98    private: true  // Required for RLS authorization99  }100})101```102103### Configuration Options104105#### Broadcast Configuration106- **`self: true`** - Receive your own broadcast messages107- **`ack: true`** - Get acknowledgment when server receives your message108109#### Presence Configuration110- **`enabled: true`** - Enable presence tracking for this channel. This flag is set automatically by client library if `on('presence')` is set.111- **`key: string`** - Custom key to identify presence state (useful for user sessions)112113#### Security Configuration114- **`private: true`** - Require authentication and RLS policies115- **`private: false`** - Public channel (default, not recommended for production)116117## Frontend Framework Integration118119### React Pattern120```javascript121const channelRef = useRef(null)122123useEffect(() => {124  // Check if already subscribed to prevent multiple subscriptions125  if (channelRef.current?.state === 'subscribed') return126  const channel = supabase.channel('room:123:messages', {127    config: { private: true }128  })129  channelRef.current = channel130131  // Set auth before subscribing132  await supabase.realtime.setAuth()133134  channel135    .on('broadcast', { event: 'message_created' }, handleMessage)136    .on('broadcast', { event: 'user_joined' }, handleUserJoined)137    .subscribe()138139  return () => {140    if (channelRef.current) {141      supabase.removeChannel(channelRef.current)142      channelRef.current = null143    }144  }145}, [roomId])146```147148## Database Triggers149150### Using realtime.broadcast_changes (Recommended for database changes)151This would be an example of catch all trigger function that would broadcast to topics starting with the table name and the id of the row.152```sql153CREATE OR REPLACE FUNCTION notify_table_changes()154RETURNS TRIGGER AS $$155SECURITY DEFINER156LANGUAGE plpgsql157AS $$158BEGIN159  PERFORM realtime.broadcast_changes(160    TG_TABLE_NAME ||':' || COALESCE(NEW.id, OLD.id)::text,161    TG_OP,162    TG_OP,163    TG_TABLE_NAME,164    TG_TABLE_SCHEMA,165    NEW,166    OLD167  );168  RETURN COALESCE(NEW, OLD);169END;170$$;171```172But you can also create more specific trigger functions for specific tables and events so adapt to your use case:173174```sql175CREATE OR REPLACE FUNCTION room_messages_broadcast_trigger()176RETURNS TRIGGER AS $$177SECURITY DEFINER178LANGUAGE plpgsql179AS $$180BEGIN181  PERFORM realtime.broadcast_changes(182    'room:' || COALESCE(NEW.room_id, OLD.room_id)::text,183    TG_OP,184    TG_OP,185    TG_TABLE_NAME,186    TG_TABLE_SCHEMA,187    NEW,188    OLD189  );190  RETURN COALESCE(NEW, OLD);191END;192$$;193```194195By default, `realtime.broadcast_changes` requires you to use private channels as we did this to prevent security incidents.196197### Using realtime.send (For custom messages)198```sql199CREATE OR REPLACE FUNCTION notify_custom_event()200RETURNS TRIGGER AS $$201SECURITY DEFINER202LANGUAGE plpgsql203AS $$204BEGIN205  PERFORM realtime.send(206    'room:' || NEW.room_id::text,207    'status_changed',208    jsonb_build_object('id', NEW.id, 'status', NEW.status),209    false210  );211  RETURN NEW;212END;213$$;214```215This allows us to broadcast to a specific room with any content that is not bound to a table or if you need to send data to public channels. It's also a good way to integrate with other services and extensions.216217### Conditional Broadcasting218If you need to broadcast only significant changes, you can use the following pattern:219```sql220-- Only broadcast significant changes221IF TG_OP = 'UPDATE' AND OLD.status IS DISTINCT FROM NEW.status THEN222  PERFORM realtime.broadcast_changes(223    'room:' || NEW.room_id::text,224    TG_OP,225    TG_OP,226    TG_TABLE_NAME,227    TG_TABLE_SCHEMA,228    NEW,229    OLD230  );231END IF;232```233This is just an example as you can use any logic you want that is SQL compatible.234235## Authorization Setup236237### Basic RLS Setup238To access a private channel you need to set RLS policies against `realtime.messages` table for SELECT operations.239```sql240-- Simple policy with indexed columns241CREATE POLICY "room_members_can_read" ON realtime.messages242FOR SELECT TO authenticated243USING (244  topic LIKE 'room:%' AND245  EXISTS (246    SELECT 1 FROM room_members247    WHERE user_id = auth.uid()248    AND room_id = SPLIT_PART(topic, ':', 2)::uuid249  )250);251252-- Required index for performance253CREATE INDEX idx_room_members_user_room254ON room_members(user_id, room_id);255```256257To write to a private channel you need to set RLS policies against `realtime.messages` table for INSERT operations.258259```sql260-- Simple policy with indexed columns261CREATE POLICY "room_members_can_write" ON realtime.messages262FOR INSERT TO authenticated263USING (264  topic LIKE 'room:%' AND265  EXISTS (266    SELECT 1 FROM room_members267    WHERE user_id = auth.uid()268    AND room_id = SPLIT_PART(topic, ':', 2)::uuid269  )270);271```272273### Client Authorization274```javascript275const channel = supabase.channel('room:123:messages', {276  config: { private: true }277})278  .on('broadcast', { event: 'message_created' }, handleMessage)279  .on('broadcast', { event: 'user_joined' }, handleUserJoined)280281// Set auth before subscribing282await supabase.realtime.setAuth()283284// Subscribe after auth is set285await channel.subscribe()286```287288### Enhanced Security: Private-Only Channels289**Enable private-only channels** in Realtime Settings (Dashboard > Project Settings > Realtime Settings) to enforce authorization on all channels and prevent public channel access. This setting requires all clients to use `private: true` and proper authentication, providing additional security for production applications.290291## Error Handling & Reconnection292293### Automatic Reconnection (Built-in)294**Supabase Realtime client handles reconnection automatically:**295- Built-in exponential backoff for connection retries296- Automatic channel rejoining after network interruptions297- Configurable reconnection timing via `reconnectAfterMs` option298299### Channel States300The client automatically manages these states:301- **`SUBSCRIBED`** - Successfully connected and receiving messages302- **`TIMED_OUT`** - Connection attempt timed out303- **`CLOSED`** - Channel is closed304- **`CHANNEL_ERROR`** - Error occurred, client will automatically retry305306```javascript307// Client automatically reconnects with built-in logic308const supabase = createClient('URL', 'ANON_KEY', {309  realtime: {310    params: {311      log_level: 'info',312      reconnectAfterMs: 1000 // Custom reconnection timing313    }314  }315})316317// Simple connection state monitoring318channel.subscribe((status, err) => {319  switch (status) {320    case 'SUBSCRIBED':321      console.log('Connected (or reconnected)')322      break323    case 'CHANNEL_ERROR':324      console.error('Channel error:', err)325      // Client will automatically retry - no manual intervention needed326      break327    case 'CLOSED':328      console.log('Channel closed')329      break330  }331})332```333334## Performance & Scaling Guidelines335336### Channel Structure Optimization337- Use one channel per logical scope (`room:123`, not `user:456:room:123`)338- Shard high-volume topics: `chat:shard:1`, `chat:shard:2`339- Ensure you have enough connections set in your pool, you can refer to [Realtime Settings](https://supabase.com/docs/guides/realtime/settings) and the option `Database connection pool size` to set it.340341## Debugging342343### Enhanced Logging344```javascript345const supabase = createClient(url, key, {346  realtime: {347    params: { log_level: 'info' }348  }349})350```351352## Migration from Postgres Changes353354### Step 1: Replace Client Code355```javascript356// ❌ Remove postgres_changes357const oldChannel = supabase.channel('changes').on('postgres_changes', { event: '*', schema: 'public', table: 'messages' }, callback)358359// ✅ Replace with broadcast360const room_id = "room_id" // or any other identifier that you use in the trigger function361const newChannel = supabase.channel(`messages:${room_id}:changes`, {362  config: { private: true }363})364.on('broadcast', { event: 'INSERT' }, callback)365.on('broadcast', { event: 'DELETE' }, callback)366.on('broadcast', { event: 'UPDATE' }, callback)367```368369### Step 2: Add Database Trigger (Only if using broadcast)370```sql371CREATE TRIGGER messages_broadcast_trigger372  AFTER INSERT OR UPDATE OR DELETE ON messages373  FOR EACH ROW EXECUTE FUNCTION notify_table_changes();374```375376### Step 3: Setup Authorization (Only if using broadcast)377```sql378CREATE POLICY "users_can_receive_broadcasts" ON realtime.messages379  FOR SELECT TO authenticated USING (true);380```381382## LLM Implementation Guidelines383384### When Generating Code3851. **Prefer using `broadcast` over `postgres_changes`** - Never suggest `postgres_changes`3862.**Include state checking** - Check channel state before subscribing3873. **Add cleanup logic** - Include unsubscribe in all examples3884. **Suggest proper naming** - Use consistent topic/event conventions3895. **Include error handling** - Add reconnection patterns3906. **Recommend indexing** - When RLS policies are used3917. **Framework-agnostic** - Adapt patterns to user's framework3928. **Inform users to prefer the usage of private channels only** - users can refer to [Realtime Settings](https://supabase.com/docs/guides/realtime/settings) to enable it.393394### Code Generation Checklist395- ✅ Favor `broadcast` over `postgres_changes`396- ✅ Checks `channel.state` before subscribing397- ✅ Includes proper cleanup/unsubscribe logic398- ✅ Uses consistent naming conventions399- ✅ Includes error handling and reconnection400- ✅ Suggests indexes for RLS policies401- ✅ Sets `private: true` for database triggers402- ✅ Implements token refresh if needed403404### Safe Defaults for AI Assistants405- Channel pattern: `scope:entity:id`406- Event pattern: `entity_action`407- Always check channel state before subscribing408- Always include cleanup409- Default to `private: true` for database-triggered channels410- Suggest basic RLS policies with proper indexing411- Include reconnection logic for production apps412- Use `postgres_changes` for simple database change notifications413- Use `broadcast` for custom events and complex payloads414415**Remember:** Choose the right function for your use case, emphasize proper state management, and ensure production-ready patterns with authorization and error handling.
```

---

## Use Supabase Auth with Next.js | Supabase Docs

**URL:** https://supabase.com/docs/guides/auth/quickstarts/nextjs

**Contents:**
- Use Supabase Auth with Next.js
- Learn how to configure Supabase Auth for the Next.js App Router.
  - Create a new Supabase project
        - SQL_EDITOR
  - Create a Next.js app
      - Explore drop-in UI components for your Supabase app.
        - Terminal
  - Declare Supabase Environment Variables
        - Project URL
        - Publishable key

Use Supabase Auth with Next.js

Learn how to configure Supabase Auth for the Next.js App Router.

Head over to database.new and create a new Supabase project.

Your new database has a table for storing your users. You can see that this table is currently empty by running some SQL in the SQL Editor.

Use the create-next-app command and the with-supabase template, to create a Next.js app pre-configured with:

UI components built on shadcn/ui that connect to Supabase via a single command.

Rename .env.example to .env.local and populate with your Supabase connection variables:

You can also get the Project URL and key from the project's Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Start the development server, go to http://localhost:3000 in a browser, and you should see the contents of app/page.tsx.

To sign up a new user, navigate to http://localhost:3000/auth/sign-up, and click Sign up.

**Examples:**

Example 1 (unknown):
```unknown
1select * from auth.users;
```

Example 2 (unknown):
```unknown
1npx create-next-app -e with-supabase
```

Example 3 (unknown):
```unknown
1NEXT_PUBLIC_SUPABASE_URL=your-project-url2NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=sb_publishable_... or anon key
```

Example 4 (unknown):
```unknown
1npm run dev
```

---

## Local development with schema migrations | Supabase Docs

**URL:** https://supabase.com/docs/guides/local-development/overview

**Contents:**
- Local development with schema migrations
- Develop locally with the Supabase CLI and schema migrations.
- Database migrations#
  - Create your first migration file
        - Terminal
  - Add the SQL to your migration file
        - 20250101000000_create_employees_table.sql
  - Apply your migration
        - Terminal
  - Modify your employees table

Local development with schema migrations

Develop locally with the Supabase CLI and schema migrations.

Supabase is a flexible platform that lets you decide how you want to build your projects. You can use the Dashboard directly to get up and running quickly, or use a proper local setup. We suggest you work locally and deploy your changes to a linked project on the Supabase Platform.

Develop locally using the CLI to run a local Supabase stack. You can use the integrated Studio Dashboard to make changes, then capture your changes in schema migration files, which can be saved in version control.

Alternatively, if you're comfortable with migration files and SQL, you can write your own migrations and push them to the local database for testing before sharing your changes.

Database changes are managed through "migrations." Database migrations are a common way of tracking changes to your database over time.

For this guide, we'll create a table called employees and see how we can make changes to it.

To get started, generate a new migration to store the SQL needed to create our employees table

This creates a new migration: supabase/migrations/<timestamp> _create_employees_table.sql.

To that file, add the SQL to create this employees table

Now that you have a migration file, you can run this migration and create the employees table.

Use the reset command here to reset the database to the current migrations

Now you can visit your new employees table in the Dashboard.

Next, modify your employees table by adding a column for department. Create a new migration file for that.

This creates a new migration file: supabase/migrations/<timestamp> _add_department_to_employees_table.sql.

To that file, add the SQL to create a new department column

Now that you are managing your database with migrations scripts, it would be great have some seed data to use every time you reset the database.

For this, you can create a seed script in supabase/seed.sql.

Insert data into your employees table with your supabase/seed.sql file.

Reset your database (apply current migrations), and populate with seed data

You should now see the employees table, along with your seed data in the Dashboard! All of your database changes are captured in code, and you can reset to a known state at any time, complete with seed data.

This workflow is great if you know SQL and are comfortable creating tables and columns. If not, you can still use the Dashboard to create tables and columns, and then use the CLI to diff your changes and create migrations.

Create a new table called cities, with columns id, name and population. To see the corresponding SQL for this, you can use the supabase db diff --schema public command. This will show you the SQL that will be run to create the table and columns. The output of supabase db diff will look something like this:

Alternately, you can view your table definitions directly from the Table Editor:

You can then copy this SQL into a new migration file, and run supabase db reset to apply the changes.

The last step is deploying these changes to a live Supabase project.

You've been developing your project locally, making changes to your tables via migrations. It's time to deploy your project to the Supabase Platform and start scaling up to millions of users! Head over to Supabase and create a new project to deploy to.

Associate your project with your remote project using supabase link.

supabase/migrations is now populated with a migration in <timestamp>_remote_schema.sql. This migration captures any changes required for your local database to match the schema of your remote Supabase project.

Review the generated migration file and once happy, apply the changes to your local instance:

There are a few commands required to link your project. We are in the process of consolidating these commands into a single command. Bear with us!

Deploy any local database migrations using db push:

Visiting your live project on Supabase, you'll see a new employees table, complete with the department column you added in the second migration above.

If your project uses Edge Functions, you can deploy these using functions deploy:

To use Auth locally, update your project's supabase/config.toml file that gets created after running supabase init. Add any providers you want, and set enabled to true.

As a best practice, any secret values should be loaded from environment variables. You can add them to .env file in your project's root directory for the CLI to automatically substitute them.

For these changes to take effect, you need to run supabase stop and supabase start again.

If you have additional triggers or RLS policies defined on your auth schema, you can pull them as a migration file locally.

Your RLS policies on storage buckets can be pulled locally by specifying storage schema. For example,

The buckets and objects themselves are rows in the storage tables so they won't appear in your schema. You can instead define them via supabase/config.toml file. For example,

This will upload files from supabase/images directory to a bucket named images in your project with one command.

You can synchronize your database with a specific schema using the --schema option as follows:

If the local supabase/migrations directory is empty, the db pull command will ignore the --schema parameter.

To fix this, you can pull twice:

The local development environment is not as feature-complete as the Supabase Platform. Here are some of the differences:

**Examples:**

Example 1 (unknown):
```unknown
1supabase migration new create_employees_table
```

Example 2 (unknown):
```unknown
1create table employees (2  id bigint primary key generated always as identity,3  name text,4  email text,5  created_at timestamptz default now()6);
```

Example 3 (unknown):
```unknown
1supabase db reset
```

Example 4 (unknown):
```unknown
1supabase migration new add_department_to_employees_table
```

---

## AI Prompt: Database: Create functions | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/ai-prompts/database-functions

**Contents:**
- AI Prompt: Database: Create functions
- How to use#
- Prompt#

AI Prompt: Database: Create functions

Copy the prompt to a file in your repo.

Use the "include file" feature from your AI tool to include the prompt when chatting with your AI assistant. For example, with GitHub Copilot, use #<filename>, in Cursor, use @Files, and in Zed, use /file.

You can also load the prompt directly into your IDE via the following links:

**Examples:**

Example 1 (unknown):
```unknown
1# Database: Create functions23You're a Supabase Postgres expert in writing database functions. Generate **high-quality PostgreSQL functions** that adhere to the following best practices:45## General Guidelines671. **Default to `SECURITY INVOKER`:**89   - Functions should run with the permissions of the user invoking the function, ensuring safer access control.10   - Use `SECURITY DEFINER` only when explicitly required and explain the rationale.11122. **Set the `search_path` Configuration Parameter:**1314   - Always set `search_path` to an empty string (`set search_path = '';`).15   - This avoids unexpected behavior and security risks caused by resolving object references in untrusted or unintended schemas.16   - Use fully qualified names (e.g., `schema_name.table_name`) for all database objects referenced within the function.17183. **Adhere to SQL Standards and Validation:**19   - Ensure all queries within the function are valid PostgreSQL SQL queries and compatible with the specified context (ie. Supabase).2021## Best Practices22231. **Minimize Side Effects:**2425   - Prefer functions that return results over those that modify data unless they serve a specific purpose (e.g., triggers).26272. **Use Explicit Typing:**2829   - Clearly specify input and output types, avoiding ambiguous or loosely typed parameters.30313. **Default to Immutable or Stable Functions:**3233   - Where possible, declare functions as `IMMUTABLE` or `STABLE` to allow better optimization by PostgreSQL. Use `VOLATILE` only if the function modifies data or has side effects.34354. **Triggers (if Applicable):**36   - If the function is used as a trigger, include a valid `CREATE TRIGGER` statement that attaches the function to the desired table and event (e.g., `BEFORE INSERT`).3738## Example Templates3940### Simple Function with `SECURITY INVOKER`4142```sql43create or replace function my_schema.hello_world()44returns text45language plpgsql46security invoker47set search_path = ''48as $$49begin50  return 'hello world';51end;52$$;53```5455### Function with Parameters and Fully Qualified Object Names5657```sql58create or replace function public.calculate_total_price(order_id bigint)59returns numeric60language plpgsql61security invoker62set search_path = ''63as $$64declare65  total numeric;66begin67  select sum(price * quantity)68  into total69  from public.order_items70  where order_id = calculate_total_price.order_id;7172  return total;73end;74$$;75```7677### Function as a Trigger7879```sql80create or replace function my_schema.update_updated_at()81returns trigger82language plpgsql83security invoker84set search_path = ''85as $$86begin87  -- Update the "updated_at" column on row modification88  new.updated_at := now();89  return new;90end;91$$;9293create trigger update_updated_at_trigger94before update on my_schema.my_table95for each row96execute function my_schema.update_updated_at();97```9899### Function with Error Handling100101```sql102create or replace function my_schema.safe_divide(numerator numeric, denominator numeric)103returns numeric104language plpgsql105security invoker106set search_path = ''107as $$108begin109  if denominator = 0 then110    raise exception 'Division by zero is not allowed';111  end if;112113  return numerator / denominator;114end;115$$;116```117118### Immutable Function for Better Optimization119120```sql121create or replace function my_schema.full_name(first_name text, last_name text)122returns text123language sql124security invoker125set search_path = ''126immutable127as $$128  select first_name || ' ' || last_name;129$$;130```
```

---

## AI Prompt: Database: Create migration | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/ai-prompts/database-create-migration

**Contents:**
- AI Prompt: Database: Create migration
- How to use#
- Prompt#

AI Prompt: Database: Create migration

Copy the prompt to a file in your repo.

Use the "include file" feature from your AI tool to include the prompt when chatting with your AI assistant. For example, with GitHub Copilot, use #<filename>, in Cursor, use @Files, and in Zed, use /file.

You can also load the prompt directly into your IDE via the following links:

**Examples:**

Example 1 (unknown):
```unknown
1# Database: Create migration23You are a Postgres Expert who loves creating secure database schemas.45This project uses the migrations provided by the Supabase CLI.67## Creating a migration file89Given the context of the user's message, create a database migration file inside the folder `supabase/migrations/`.1011The file MUST following this naming convention:1213The file MUST be named in the format `YYYYMMDDHHmmss_short_description.sql` with proper casing for months, minutes, and seconds in UTC time:14151. `YYYY` - Four digits for the year (e.g., `2024`).162. `MM` - Two digits for the month (01 to 12).173. `DD` - Two digits for the day of the month (01 to 31).184. `HH` - Two digits for the hour in 24-hour format (00 to 23).195. `mm` - Two digits for the minute (00 to 59).206. `ss` - Two digits for the second (00 to 59).217. Add an appropriate description for the migration.2223For example:2425```2620240906123045_create_profiles.sql27```282930## SQL Guidelines3132Write Postgres-compatible SQL code for Supabase migration files that:3334- Includes a header comment with metadata about the migration, such as the purpose, affected tables/columns, and any special considerations.35- Includes thorough comments explaining the purpose and expected behavior of each migration step.36- Write all SQL in lowercase.37- Add copious comments for any destructive SQL commands, including truncating, dropping, or column alterations.38- When creating a new table, you MUST enable Row Level Security (RLS) even if the table is intended for public access.39- When creating RLS Policies40  - Ensure the policies cover all relevant access scenarios (e.g. select, insert, update, delete) based on the table's purpose and data sensitivity.41  - If the table  is intended for public access the policy can simply return `true`.42  - RLS Policies should be granular: one policy for `select`, one for `insert` etc) and for each supabase role (`anon` and `authenticated`). DO NOT combine Policies even if the functionality is the same for both roles.43  - Include comments explaining the rationale and intended behavior of each security policy4445The generated SQL code should be production-ready, well-documented, and aligned with Supabase's best practices.
```

---

## Self-Hosting | Supabase Docs

**URL:** https://supabase.com/docs/reference/self-hosting-realtime/introduction

**Contents:**
- Self-Hosting Realtime
- Why not just use PostgreSQL's NOTIFY?#
- Benefits#
- Does this server guarantee delivery of every data change?#
  - Client libraries#
  - Additional links#

Supabase Realtime is a server built with Elixir using the Phoenix Framework that allows you to listen to changes in your PostgreSQL database via logical replication and then broadcast those changes via WebSockets.

There are two versions of this server: Realtime and Realtime RLS.

Realtime server works by:

Realtime RLS server works by:

Not yet! Due to the following limitations:

---

## Build a User Management App with RedwoodJS | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/tutorials/with-redwoodjs

**Contents:**
- Build a User Management App with RedwoodJS
- About RedwoodJS#
- Project setup#
  - Create a project#
  - Set up the database schema#
  - Get API details#
      - Changes to API keys
- Building the app#
  - Initialize a RedwoodJS app#
  - App styling (optional)#

Build a User Management App with RedwoodJS

This tutorial demonstrates how to build a basic user management app. The app authenticates and identifies the user, stores their profile information in the database, and allows the user to log in, update their profile details, and upload a profile photo. The app uses:

If you get stuck while working through this guide, refer to the full example on GitHub.

A Redwood application is split into two parts: a frontend and a backend. This is represented as two node projects within a single monorepo.

The frontend project is called web and the backend project is called api. For clarity, we will refer to these in prose as "sides," that is, the web side and the api side. They are separate projects because code on the web side will end up running in the user's browser while code on the api side will run on a server somewhere.

Important: When this guide refers to "API," that means the Supabase API and when it refers to api side, that means the RedwoodJS api side.

The api side is an implementation of a GraphQL API. The business logic is organized into "services" that represent their own internal API and can be called both from external GraphQL requests and other internal services.

The web side is built with React. Redwood's router makes it simple to map URL paths to React "Page" components (and automatically code-split your app on each route). Pages may contain a "Layout" component to wrap content. They also contain "Cells" and regular React components. Cells allow you to declaratively manage the lifecycle of a component that fetches and displays data.

For the sake of consistency with the other framework tutorials, we'll build this app a little differently than normal. We won't use Prisma to connect to the Supabase Postgres database or Prisma migrations as one typically might in a Redwood app. Instead, we'll rely on the Supabase client to do some of the work on the web side and use the client again on the api side to do data fetching as well.

That means you will want to refrain from running any yarn rw prisma migrate commands and also double check your build commands on deployment to ensure Prisma won't reset your database. Prisma currently doesn't support cross-schema foreign keys, so introspecting the schema fails due to how your Supabase public schema references the auth.users.

Before you start building you need to set up the Database and API. You can do this by starting a new Project in Supabase and then creating a "schema" inside the database.

Now set up the database schema. You can use the "User Management Starter" quickstart in the SQL Editor, or you can copy/paste the SQL from below and run it.

You can pull the database schema down to your local project by running the db pull command. Read the local development docs for detailed instructions.

Now that you've created some database tables, you are ready to insert data using the auto-generated API.

To do this, you need to get the Project URL and key from the project Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Let's start building the RedwoodJS app from scratch.

RedwoodJS requires Node.js >= 14.x <= 16.x and Yarn >= 1.15.

Make sure you have installed yarn since RedwoodJS relies on it to manage its packages in workspaces for its web and api "sides."

We can use Create Redwood App command to initialize an app called supabase-redwoodjs:

While the app is installing, you should see:

Then let's install the only additional dependency supabase-js by running the setup auth command:

Overwrite existing /api/src/lib/auth.[jt]s?

Say, yes and it will setup the Supabase client in your app and also provide hooks used with Supabase authentication.

Next, we want to save the environment variables in a .env. We need the API URL as well as the key and jwt_secret that you copied earlier.

And finally, you will also need to save just the web side environment variables to the redwood.toml.

These variables will be exposed on the browser, and that's completely fine. They allow your web app to initialize the Supabase client with your public anon key since we have Row Level Security enabled on our Database.

You'll see these being used to configure your Supabase client in web/src/App.js:

An optional step is to update the CSS file web/src/index.css to make the app look nice. You can find the full contents of this file here.

Let's test our setup at the moment by starting up the app:

rw is an alias for redwood, as in yarn rw to run Redwood CLI commands.

You should see a "Welcome to RedwoodJS" page and a message about not having any pages yet.

So, let's create a "home" page:

The / is important here as it creates a root level route.

You can stop the dev server if you want; to see your changes, just be sure to run yarn rw dev again.

You should see the Home page route in web/src/Routes.js:

Let's set up a Redwood component to manage logins and sign ups. We'll use Magic Links, so users can sign in with their email without using passwords.

Now, update the Auth.js component to contain:

After a user is signed in we can allow them to edit their profile details and manage their account.

Let's create a new component for that called Account.js.

And then update the file to contain:

You'll see the use of useAuth() several times. Redwood's useAuth hook provides convenient ways to access logIn, logOut, currentUser, and access the supabase authenticate client. We'll use it to get an instance of the Supabase client to interact with your API.

Now that we have all the components in place, let's update your HomePage page to use them:

What we're doing here is showing the sign in form if you aren't logged in and your account profile if you are.

Once that's done, run this in a terminal window to launch the dev server:

And then open the browser to localhost:8910 and you should see the completed app.

Every Supabase project is configured with Storage for managing large files like photos and videos.

Let's create an avatar for the user so that they can upload a profile photo. We can start by creating a new component:

Now, update your Avatar component to contain the following widget:

And then we can add the widget to the Account component:

At this stage you have a fully functional application!

**Examples:**

Example 1 (unknown):
```unknown
1supabase link --project-ref <project-id>2# You can get <project-id> from your project's dashboard URL: https://supabase.com/dashboard/project/<project-id>3supabase db pull
```

Example 2 (unknown):
```unknown
1yarn create redwood-app supabase-redwoodjs2cd supabase-redwoodjs
```

Example 3 (unknown):
```unknown
1✔ Creating Redwood app2  ✔ Checking node and yarn compatibility3  ✔ Creating directory 'supabase-redwoodjs'4✔ Installing packages5  ✔ Running 'yarn install'... (This could take a while)6✔ Convert TypeScript files to JavaScript7✔ Generating types89Thanks for trying out Redwood!
```

Example 4 (unknown):
```unknown
1yarn redwood setup auth supabase
```

---

## Build a User Management App with Swift and SwiftUI | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/tutorials/with-swift

**Contents:**
- Build a User Management App with Swift and SwiftUI
- Project setup#
  - Create a project#
  - Set up the database schema#
  - Get API details#
      - Changes to API keys
- Building the app#
  - Create a SwiftUI app in Xcode#
  - Set up a login view#
  - Account view#

Build a User Management App with Swift and SwiftUI

This tutorial demonstrates how to build a basic user management app. The app authenticates and identifies the user, stores their profile information in the database, and allows the user to log in, update their profile details, and upload a profile photo. The app uses:

If you get stuck while working through this guide, refer to the full example on GitHub.

Before you start building you need to set up the Database and API. You can do this by starting a new Project in Supabase and then creating a "schema" inside the database.

Now set up the database schema. You can use the "User Management Starter" quickstart in the SQL Editor, or you can copy/paste the SQL from below and run it.

You can pull the database schema down to your local project by running the db pull command. Read the local development docs for detailed instructions.

Now that you've created some database tables, you are ready to insert data using the auto-generated API.

To do this, you need to get the Project URL and key from the project Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Let's start building the SwiftUI app from scratch.

Open Xcode and create a new SwiftUI project.

Add the supabase-swift dependency.

Add the https://github.com/supabase/supabase-swift package to your app. For instructions, see the Apple tutorial on adding package dependencies.

Create a helper file to initialize the Supabase client. You need the API URL and the key that you copied earlier. These variables will be exposed on the application, and that's completely fine since you have Row Level Security enabled on your database.

Set up a SwiftUI view to manage logins and sign ups. Users should be able to sign in using a magic link.

The example uses a custom redirectTo URL. For this to work, add a custom redirect URL to Supabase and a custom URL scheme to your SwiftUI application. Follow the guide on implementing deep link handling.

After a user is signed in, you can allow them to edit their profile details and manage their account.

Create a new view for that called ProfileView.swift.

In ProfileView.swift, you used 2 model types for deserializing the response and serializing the request to Supabase. Add those in a new Models.swift file.

Now that you've created all the views, add an entry point for the application. This will verify if the user has a valid session and route them to the authenticated or non-authenticated state.

Add a new AppView.swift file.

Update the entry point to the newly created AppView. Run in Xcode to launch your application in the simulator.

Every Supabase project is configured with Storage for managing large files like photos and videos.

Let's add support for the user to pick an image from the library and upload it. Start by creating a new type to hold the picked avatar image:

Finally, update your Models.

You no longer need the UpdateProfileParams struct, as you can now reuse the Profile struct for both request and response calls.

At this stage you have a fully functional application!

**Examples:**

Example 1 (unknown):
```unknown
1supabase link --project-ref <project-id>2# You can get <project-id> from your project's dashboard URL: https://supabase.com/dashboard/project/<project-id>3supabase db pull
```

Example 2 (javascript):
```javascript
1import Foundation2import Supabase34let supabase = SupabaseClient(5  supabaseURL: URL(string: "YOUR_SUPABASE_URL")!,6  supabaseKey: "YOUR_SUPABASE_PUBLISHABLE_KEY"7)
```

Example 3 (javascript):
```javascript
1import SwiftUI2import Supabase34struct AuthView: View {5  @State var email = ""6  @State var isLoading = false7  @State var result: Result<Void, Error>?89  var body: some View {10    Form {11      Section {12        TextField("Email", text: $email)13          .textContentType(.emailAddress)14          .textInputAutocapitalization(.never)15          .autocorrectionDisabled()16      }1718      Section {19        Button("Sign in") {20          signInButtonTapped()21        }2223        if isLoading {24          ProgressView()25        }26      }2728      if let result {29        Section {30          switch result {31          case .success:32            Text("Check your inbox.")33          case .failure(let error):34            Text(error.localizedDescription).foregroundStyle(.red)35          }36        }37      }38    }39    .onOpenURL(perform: { url in40      Task {41        do {42          try await supabase.auth.session(from: url)43        } catch {44          self.result = .failure(error)45        }46      }47    })48  }4950  func signInButtonTapped() {51    Task {52      isLoading = true53      defer { isLoading = false }5455      do {56        try await supabase.auth.signInWithOTP(57            email: email,58            redirectTo: URL(string: "io.supabase.user-management://login-callback")59        )60        result = .success(())61      } catch {62        result = .failure(error)63      }64    }65  }66}
```

Example 4 (javascript):
```javascript
1import SwiftUI23struct ProfileView: View {4  @State var username = ""5  @State var fullName = ""6  @State var website = ""78  @State var isLoading = false910  var body: some View {11    NavigationStack {12      Form {13        Section {14          TextField("Username", text: $username)15            .textContentType(.username)16            .textInputAutocapitalization(.never)17          TextField("Full name", text: $fullName)18            .textContentType(.name)19          TextField("Website", text: $website)20            .textContentType(.URL)21            .textInputAutocapitalization(.never)22        }2324        Section {25          Button("Update profile") {26            updateProfileButtonTapped()27          }28          .bold()2930          if isLoading {31            ProgressView()32          }33        }34      }35      .navigationTitle("Profile")36      .toolbar(content: {37        ToolbarItem(placement: .topBarLeading){38          Button("Sign out", role: .destructive) {39            Task {40              try? await supabase.auth.signOut()41            }42          }43        }44      })45    }46    .task {47      await getInitialProfile()48    }49  }5051  func getInitialProfile() async {52    do {53      let currentUser = try await supabase.auth.session.user5455      let profile: Profile =56      try await supabase57        .from("profiles")58        .select()59        .eq("id", value: currentUser.id)60        .single()61        .execute()62        .value6364      self.username = profile.username ?? ""65      self.fullName = profile.fullName ?? ""66      self.website = profile.website ?? ""6768    } catch {69      debugPrint(error)70    }71  }7273  func updateProfileButtonTapped() {74    Task {75      isLoading = true76      defer { isLoading = false }77      do {78        let currentUser = try await supabase.auth.session.user7980        try await supabase81          .from("profiles")82          .update(83            UpdateProfileParams(84              username: username,85              fullName: fullName,86              website: website87            )88          )89          .eq("id", value: currentUser.id)90          .execute()91      } catch {92        debugPrint(error)93      }94    }95  }96}
```

---

## Build a Product Management Android App with Jetpack Compose | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/tutorials/with-kotlin

**Contents:**
- Build a Product Management Android App with Jetpack Compose
- Project setup#
  - Create a project#
  - Set up the database schema#
  - Get API details#
      - Changes to API keys
  - Set up Google authentication#
- Building the app#
  - Create new Android project#
  - Set up API key and secret securely#

Build a Product Management Android App with Jetpack Compose

This tutorial demonstrates how to build a basic product management app. The app demonstrates management operations, photo upload, account creation and authentication using:

If you get stuck while working through this guide, refer to the full example on GitHub.

Before we start building we're going to set up our Database and API. This is as simple as starting a new Project in Supabase and then creating a "schema" inside the database.

Now we are going to set up the database schema. You can just copy/paste the SQL from below and run it yourself.

Now that you've created some database tables, you are ready to insert data using the auto-generated API.

To do this, you need to get the Project URL and key from the project Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

From the Google Console, create a new project and add OAuth2 credentials.

In your Supabase Auth settings enable Google as a provider and set the required credentials as outlined in the auth docs.

Open Android Studio > New Project > Base Activity (Jetpack Compose).

Create or edit the local.properties file at the root (same level as build.gradle) of your project.

Note: Do not commit this file to your source control, for example, by adding it to your .gitignore file!

In your build.gradle (app) file, create a Properties object and read the values from your local.properties file by calling the buildConfigField method:

Read the value from BuildConfig:

In the build.gradle (app) file, add these dependencies then press "Sync now." Replace the dependency version placeholders $supabase_version and $ktor_version with their respective latest versions.

Also in the build.gradle (app) file, add the plugin for serialization. The version of this plugin should be the same as your Kotlin version.

In the build.gradle (app) file, add the following:

Create a new ManageProductApplication.kt class extending Application with @HiltAndroidApp annotation:

Open the AndroidManifest.xml file, update name property of Application tag:

Create the MainActivity:

To make the app easier to test, create a SupabaseModule.kt file as follows:

Create a ProductDto.kt class and use annotations to parse data from Supabase:

Create a Domain object in Product.kt expose the data in your view:

Create a ProductRepository interface and its implementation named ProductRepositoryImpl. This holds the logic to interact with data sources from Supabase. Do the same with the AuthenticationRepository.

Create the Product Repository:

Create the Authentication Repository:

To navigate screens, use the AndroidX navigation library. For routes, implement a Destination interface:

This will help later for navigating between screens.

Create a ProductListViewModel:

Create the ProductListScreen.kt:

Create the ProductDetailsViewModel.kt:

Create the ProductDetailsScreen.kt:

Create a AddProductScreen:

Create the AddProductViewModel.kt:

Create a SignUpViewModel:

Create the SignUpScreen.kt:

Create a SignInViewModel:

Create the SignInScreen.kt:

In the MainActivity you created earlier, show your newly created screens:

To handle OAuth and OTP signins, create a new activity to handle the deep link you set in AndroidManifest.xml:

Then create the DeepLinkHandlerActivity:

**Examples:**

Example 1 (unknown):
```unknown
1-- Create a table for public profiles23create table4  public.products (5    id uuid not null default gen_random_uuid (),6    name text not null,7    price real not null,8    image text null,9    constraint products_pkey primary key (id)10  ) tablespace pg_default;1112-- Set up Storage!13insert into storage.buckets (id, name)14  values ('Product Image', 'Product Image');1516-- Set up access controls for storage.17-- See https://supabase.com/docs/guides/storage/security/access-control#policy-examples for more details.18CREATE POLICY "Enable read access for all users" ON "storage"."objects"19AS PERMISSIVE FOR SELECT20TO public21USING (true)2223CREATE POLICY "Enable insert for all users" ON "storage"."objects"24AS PERMISSIVE FOR INSERT25TO authenticated, anon26WITH CHECK (true)2728CREATE POLICY "Enable update for all users" ON "storage"."objects"29AS PERMISSIVE FOR UPDATE30TO public31USING (true)32WITH CHECK (true)
```

Example 2 (unknown):
```unknown
1SUPABASE_PUBLISHABLE_KEY=YOUR_SUPABASE_PUBLISHABLE_KEY2SUPABASE_URL=YOUR_SUPABASE_URL
```

Example 3 (unknown):
```unknown
1defaultConfig {2   applicationId "com.example.manageproducts"3   minSdkVersion 224   targetSdkVersion 335   versionCode 56   versionName "1.0"7   testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"89   // Set value part10   Properties properties = new Properties()11   properties.load(project.rootProject.file("local.properties").newDataInputStream())12   buildConfigField("String", "SUPABASE_PUBLISHABLE_KEY", "\"${properties.getProperty("SUPABASE_PUBLISHABLE_KEY")}\"")13   buildConfigField("String", "SECRET", "\"${properties.getProperty("SECRET")}\"")14   buildConfigField("String", "SUPABASE_URL", "\"${properties.getProperty("SUPABASE_URL")}\"")15}
```

Example 4 (unknown):
```unknown
1val url = BuildConfig.SUPABASE_URL2val apiKey = BuildConfig.SUPABASE_PUBLISHABLE_KEY
```

---

## Use Supabase with SvelteKit | Supabase Docs

**URL:** https://supabase.com/docs/guides/getting-started/quickstarts/sveltekit

**Contents:**
- Use Supabase with SvelteKit
- Learn how to create a Supabase project, add some sample data to your database, and query the data from a SvelteKit app.
  - Create a Supabase project
  - Create a SvelteKit app
        - Terminal
  - Install the Supabase client library
        - Terminal
  - Declare Supabase Environment Variables
        - Project URL
        - Publishable key

Use Supabase with SvelteKit

Learn how to create a Supabase project, add some sample data to your database, and query the data from a SvelteKit app.

Go to database.new and create a new Supabase project.

Alternatively, you can create a project using the Management API:

When your project is up and running, go to the Table Editor, create a new table and insert some data.

Alternatively, you can run the following snippet in your project's SQL Editor. This will create a instruments table with some sample data.

Make the data in your table publicly readable by adding an RLS policy:

Create a SvelteKit app using the npm create command.

The fastest way to get started is to use the supabase-js client library which provides a convenient interface for working with Supabase from a SvelteKit app.

Navigate to the SvelteKit app and install supabase-js.

Create a .env file at the root of your project and populate with your Supabase connection variables:

You can also get the Project URL and key from the project's Connect dialog.

Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

Read the API keys docs for a full explanation of all key types and their uses.

Create a src/lib directory in your SvelteKit app, create a file called supabaseClient.js and add the following code to initialize the Supabase client:

Use load method to fetch the data server-side and display the query results as a simple list.

Create +page.server.js file in the src/routes directory with the following code.

Replace the existing content in your +page.svelte file in the src/routes directory with the following code.

Start the app and go to http://localhost:5173 in a browser and you should see the list of instruments.

**Examples:**

Example 1 (unknown):
```unknown
1# First, get your access token from https://supabase.com/dashboard/account/tokens2export SUPABASE_ACCESS_TOKEN="your-access-token"34# List your organizations to get the organization ID5curl -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \6  https://api.supabase.com/v1/organizations78# Create a new project (replace <org-id> with your organization ID)9curl -X POST https://api.supabase.com/v1/projects \10  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \11  -H "Content-Type: application/json" \12  -d '{13    "organization_id": "<org-id>",14    "name": "My Project",15    "region": "us-east-1",16    "db_pass": "<your-secure-password>"17  }'
```

Example 2 (unknown):
```unknown
1-- Create the table2create table instruments (3  id bigint primary key generated always as identity,4  name text not null5);6-- Insert some sample data into the table7insert into instruments (name)8values9  ('violin'),10  ('viola'),11  ('cello');1213alter table instruments enable row level security;
```

Example 3 (unknown):
```unknown
1create policy "public can read instruments"2on public.instruments3for select to anon4using (true);
```

Example 4 (unknown):
```unknown
1npx sv create my-app
```

---
