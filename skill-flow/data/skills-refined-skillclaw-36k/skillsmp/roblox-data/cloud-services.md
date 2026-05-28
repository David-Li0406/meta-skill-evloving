# Cloud-services Reference

## Contents
- [Best practices for data stores](#best-practices-for-data-stores)
- [Data Stores Manager](#data-stores-manager)
- [Data store error codes and limits](#data-store-error-codes-and-limits)
- [Data stores](#data-stores)
- [Data store observability](#data-store-observability)
- [Implement player data and purchasing systems](#implement-player-data-and-purchasing-systems)
- [Data store versioning, listing, and caching](#data-store-versioning-listing-and-caching)
- [Best practices when designing MemoryStore data structures](#best-practices-when-designing-memorystore-data-structures)
- [Memory store hash map](#memory-store-hash-map)
- [Memory stores](#memory-stores)
- [Memory store observability](#memory-store-observability)
- [Partitions and data distribution](#partitions-and-data-distribution)
- [Memory store queue](#memory-store-queue)
- [Memory store sorted map](#memory-store-sorted-map)

---

## Best practices for data stores

Best practices are guidelines that help you manage your data more efficiently.

## General best practices

### Create fewer data stores

Data stores have similar behavior to tables in databases. When you minimize the number of data stores in an experience and put related data in the same data store, you're able to configure each data store individually and improve the service's efficiency to operate the data.

### Use a single object for related data

To use the maximum [4 MB object size limit](./error-codes-and-limits.md#throughput-limits) more efficiently, fetch all relevant data in one call. `Class.GlobalDataStore:SetAsync()|SetAsync()` updates all data so that all data for the same user is always in sync.

The versioning system versions individual objects instead of the entire data store. This means self-contained objects are consistent when you restore data stores to older versions.

### Use key prefixes to organize your data

Filter keys with a specific [prefix](./versioning-listing-and-caching.md#listing-and-prefixes) when calling `Class.DataStore:ListKeysAsync()|ListKeysAsync()`. For example, you can save keys with a prefix like `/User_1234/profiles/warrior` and `/User_1234/profiles/mage` in experiences that support users with multiple character profiles. You can then use a prefix search with `/User_1234/profiles` to get a list of all profiles belonging to that user.

## Optimization best practices

Data stores have storage limits that apply per experience. When your experience approaches or exceeds its quota, you should take action to reduce usage and avoid potential additional costs.

### Monitor storage usage

Use these tools for data store observability:

- **Data Stores Dashboard**, which provides you with a visual overview of your storage usage over time. Use this dashboard to monitor how your storage scales and to identify periods of unexpected growth in usage.
- **Data Stores Manager**, which gives you a direct view into your experience's stored data

[Content truncated - see full docs]

---

## Data Stores Manager

With the Data Stores Manager, you can browse and monitor your data stores, their key entries, and their storage usage directly on the Creator Hub.

## Access the Data Stores Manager

<Alert severity="info">
If you're the owner of an experience or the group owner of a group-owned experience, you already have full access to the Data Stores Manager by default.

To give members of your group access to the Data Stores Manager, you can [grant them one of the following permissions](../../projects/groups.md#roles-and-permissions):

- **View Data Stores** lets them view the Data Stores Manager page in the Creator Hub.
- **Edit Data Stores** lets them delete keys.
- **Delete Data Stores** lets them delete data stores.
- **Edit all group experiences** gives them full access to all of the functionality of the Data Stores Manager.
</Alert>

To access the Data Stores Manager:

1. Go to Creations and select an experience.
2. Go to **Configure** ⟩ **Data Stores Manager**.

<img src="./../../assets/data/data-store/Data-Stores-Manager-Page.png" alt="Overview of Data Stores Manager page displaying the Summary section, the Data Stores list, and the Keys list." />

<br/>
<br/>

The **Summary** section of the Data Stores Manager page includes the **Total Size** and the **Storage Limit** of your data stores. Total Size is calculated by adding the number of bytes consumed by all existing keys in your experience, and Storage Limit is calculated based on your experience's lifetime user count. For more information about storage limits, see [Limits](./error-codes-and-limits.md#limits).

If your Total Size exceeds your Storage Limit, your **Est. Monthly Costs** will populate in your Summary and show an estimation of the impact of the usage that has gone over your quota. For tips on how to reduce your storage consumption, see [Best practices](./best-practices.md).

## View data stores and keys

<Alert severity="warning">
  If your experience has more than 100 data stores, the data store size and

[Content truncated - see full docs]

---

## Data store error codes and limits

Requests you make to data stores can fail due to poor connectivity or other issues. To handle errors and return messages with an error code, wrap data store functions in `Global.LuaGlobals.pcall()`.

## Error code reference

<table>
<thead>
  <tr>
    <th>Error code</th>
    <th>Error name</th>
    <th>Error message</th>
    <th>Notes</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>`101`</td>
    <td>`KeyNameEmpty`</td>
    <td>Key name can't be empty.</td>
    <td>Check if the key input into the data store function is an empty string.</td>
  </tr>
  <tr>
    <td>`102`</td>
    <td>`KeyNameLimit`</td>
    <td>Key name exceeds the 50 character limit.</td>
    <td>Check if the key input into the data store function exceeds a length of 50.</td>
  </tr>
  <tr>
    <td>`103`</td>
    <td>`ValueNotAllowed`</td>
    <td>Can't allow <b>X</b> in `DataStore`.</td>
    <td>A bad update function returned a value of type <b>X</b>.</td>
  </tr>
  <tr>
    <td>`104`</td>
    <td>`CantStoreValue`</td>
    <td>Can't store <b>X</b> in `DataStore`.</td>
    <td>The update function returned a value of type <b>X</b> that didn't serialize.</td>
  </tr>
  <tr>
    <td>`105`</td>
    <td>`ValueTooLarge`</td>
    <td>Serialized value exceeds <b>X</b> limit.</td>
    <td>If you're setting a value with `Class.GlobalDataStore:SetAsync()|SetAsync()` or `Class.GlobalDataStore:UpdateAsync()|UpdateAsync()`, the serialized length of the value can't exceed the size <b>X</b>. To check the serialized length of the data, use `Class.HttpService:JSONEncode()|JSONEncode()`.</td>
  </tr>
  <tr>
    <td>`106`</td>
    <td>`MaxValueInvalid`</td>
    <td>`MaxValue` must be an integer.</td>
    <td>If you're passing a maximum value to `Class.OrderedDataStore:GetSortedAsync()|GetSortedAsync()` for an `Class.OrderedDataStore`, it must be an integer.</td>
  </tr>
  <tr>
    <td>`106`</td>
    <td>`MinValueInvalid`</td>
    <td>`MinValue` must be an integer.</td>
    <td>If you're passing a minimum value to `Class.Or

[Content truncated - see full docs]

---

## Data stores

The `Class.DataStoreService` lets you store data that needs to persist between sessions, like items in a player's inventory or skill points. Data stores are consistent per experience, so any place in an experience can access and change the same data, including places on different servers.

If you want to add granular permission control to your data stores and access them outside of Studio or Roblox servers, you can use [Open Cloud APIs for data stores](/cloud/reference/DataStore).

To view and monitor all the data stores in an experience through the Creator Hub, use the [Data Stores Manager](./data-stores-manager.md).

For temporary data that you need to update or access frequently, use [memory stores](./../memory-stores/index.md).

## Enable Studio access

By default, experiences tested in Studio can't access data stores, so you must first enable them. Accessing data stores in Studio can be dangerous for live experiences because Studio accesses the same data stores as the client application. To avoid overwriting production data, do not enable this setting for live experiences. Instead, enable it for a separate test version of the experience.

To enable Studio access in a [published](../../production/publishing/publish-experiences-and-places.md) experience:

1. Open Studio's **File**&nbsp;⟩ **Game Settings** window.
2. Navigate to **Security**.
3. Enable the **Enable Studio Access to API Services** toggle.
4. Click **Save**.

## Access data stores

To access a data store inside an experience:

1. Add `Class.DataStoreService` to a server-side `Class.Script|Script`.
2. Use the `Class.DataStoreService:GetDataStore()|GetDataStore()` function and specify the name of the data store you want to use. If the data store doesn't exist, Studio creates one when you save your experience data for the first time.

```lua
local DataStoreService = game:GetService("DataStoreService")

local experienceStore = DataStoreService:GetDataStore("PlayerExperience")
```

<Alert severity="warni

[Content truncated - see full docs]

---

## Data store observability

The data stores observability dashboard provides real-time charts on your request counts and on your usage against future data store limits, and allows you to filter the request data by standard or ordered data stores.

[Image: An image showing the request count by API dashboard in the Creator Hub.]

## Access the dashboard

The data stores dashboard is available for any experience that uses `Class.DataStoreService`, but you must either be the experience owner or have [analytics group permissions](../../production/analytics/analytics-dashboard.md#grant-group-permission) to access the dashboard.

1. Navigate to the [Creations](https://create.roblox.com/dashboard/creations) page on the **Creator Hub**.
2. Under the **Creator Hub** dropdown, select your account or the group owning the target experience.
3. Select the experience.
4. In the **Monitoring** dropdown, select **Data Stores**.

## Available charts

- **Storage Usage Bytes** on amount of data store storage and limit currently available for the selected universe.
- **Request Count by API** on API request count per minute by API method, such as `Class.DataStore:SetAsync()` or `Class.OrderedDataStore:GetSortedAsync()`.
- **Request Count by Status** on API request count by [response status](#response-status-codes).
- **Request by API x Status** on response statuses returned by all or a specific API method.
- **Read Request Type Quota Usage** on number of read API method calls against future read category limits.
- **Write Request Type Quota Usage** on number of write API method calls against future write category limits.
- **List Request Type Quota Usage** on number of list API method calls against future list category limits.
- **Remove Request Type Quota Usage** on number of remove API method calls against future remove category limits.

Use the selector at the top of the page to filter by standard or ordered data stores. The default view includes standard data store only.

Use the **Explore** button next to eac

[Content truncated - see full docs]

---

## Implement player data and purchasing systems

## Background

Roblox provides a set of APIs to interface with data stores via `Class.DataStoreService`. The most common use case for these APIs is for saving, loading, and replicating _player data_. That is, data associated with the player's progress, purchases, and other session characteristics that persists between individual play sessions.

Most experiences on Roblox use these APIs to implement some form of a player data system. These implementations differ in their approach, but generally seek to solve the same set of issues.

## Common problems

Below are some of the most common problems player data systems attempt to solve:

- **In Memory Access:** `Class.DataStoreService` requests make web requests that operate asynchronously and are subject to rate limits. This is appropriate for an initial load at the start of the session, but not for high frequency read and write operations during the normal course of gameplay. Most developers' player data systems store this data in-memory on the Roblox server, limiting `Class.DataStoreService` requests to the following scenarios:

  - Initial read at the start of a session
  - Final write at the end of the session
  - Periodic writes at an interval to mitigate the scenario where the final write fails
  - Writes to ensure data is saved while processing a purchase

- **Efficient Storage:** Storing all of a player's session data in a single table lets you update multiple values atomically and handle the same amount of data in fewer requests. It also removes the risk of inter-value desynchronization and makes rollbacks easier to reason around.

  Some developers also implement custom serialization to compress large data structures (typically to save in-game user-generated content).

- **Replication:** The client needs regular access to a player's data (for example, to update the UI). A generic approach to replicating player data to the client lets you transmit this information without having to create bespoke replication sys

[Content truncated - see full docs]

---

## Data store versioning, listing, and caching

Manage your data using versioning, listing, and caching.

## Versioning

Versioning happens when you [set](./index.md#create-data), [update](./index.md#update-data), and [increment](./index.md#increment-data) data. The functions `Class.GlobalDataStore:SetAsync()|SetAsync()`, `Class.GlobalDataStore:UpdateAsync()|UpdateAsync()`, and `Class.GlobalDataStore:IncrementAsync()|IncrementAsync()` create versioned backups of your data using the first write to each key in each UTC hour. Successive writes to a key in the same UTC hour permanently overwrite the previous data.

Versioned backups expire 30 days after a new write overwrites them. The latest version never expires.

The following functions perform versioning operations:

<table>
<thead>
  <tr>
    <th>Function</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>
      `Class.DataStore:ListVersionsAsync()|ListVersionsAsync()`
    </td>
    <td>
      Lists all versions for a key by returning a `Class.DataStoreVersionPages` instance that you can use to enumerate all version numbers. You can filter versions using a time range.
    </td>
  </tr>
  <tr>
    <td>
      `Class.DataStore:GetVersionAsync()|GetVersionAsync()`
    </td>
    <td>
      Retrieves a specific version of a key using the key's version number.
    </td>
  </tr>
  <tr>
    <td>
      `Class.DataStore:RemoveVersionAsync()|RemoveVersionAsync()`
    </td>
    <td>
      Deletes a specific version of a key.

      This function also creates a tombstone version while retaining the previous version. For example, if you call `RemoveAsync("User_1234")` and then try to call `GetAsync("User_1234")`, you get `nil` back. However, you can still use `Class.DataStore:ListVersionsAsync()|ListVersionsAsync()` and `Class.DataStore:GetVersionAsync()|GetVersionAsync()` to retrieve older versions of the data.
    </td>

  </tr>
</tbody>
</table>

You can use versioning to handle user requests. If a user reports that a problem occurred at 2020-10-09T01:42,

[Content truncated - see full docs]

---

## Best practices when designing MemoryStore data structures

Depending on the data structure type, MemoryStoreService enforces [limits](../../cloud-services/memory-stores/index.md#data-structure-size-limits) on the memory and number of items in a data structure. All data structures are also constrained by a global per-partition request limit.

Each Roblox experience has the [Memory Store Observability Dashboard](../../cloud-services/memory-stores/observability.md), which includes a set of charts that you can use to monitor memory store usage.

## Sorted maps and queues

Sorted maps and queues both have limits on the maximum number of items and maximum total memory. Additionally, the items in one of these data structures always reside on a single partition. Every request to one of those data structures is a request to the same partition.

When a sorted map or queues reaches its item or memory limit, the best course of action is to remove unnecessary items manually or by adding an expiration policy for items. Alternatively, if only the memory limit is causing throttling, you can try to reduce the size of your items by stripping unnecessary information out of your keys and values.

If you need all of your items or are experiencing throttling due to request throughput, the only solution is sharding.

### Sharding

Sharding is the process of storing a set of related data across multiple data structures. In other words, it means taking an existing, high-throughput data structure and replacing it with multiple, smaller ones that together contain the same set of data as the original.

The key challenge to sharding is finding a way to spread the data across multiple data structures in a way that maintains the same functionality as the original.

For hash maps, although the data structure is already partitioned, sharding is done by spreading the requests among several keys.

### Sharding a sorted map

To shard a sorted map, consider splitting your data into alphabetic subsections with character ranges. For example, assume that you only

[Content truncated - see full docs]

---

## Memory store hash map

**Hash maps**, similar to sorted maps, let you store in-memory data as key-value pairs. Unlike sorted maps, they maintain no ordering guarantees. This data structure is useful for cases that require simple data caching and rapid access, such as shared inventories, physical auction houses, and more. Hash maps automatically handle partitioning your data and are very useful if you have more than 1,000 keys. For smaller key spaces, we recommend [sorted maps](../../cloud-services/memory-stores/sorted-map.md).

## Limits

Hash maps have a key size limit of 128 characters and a value size limit of 32 KB.

Otherwise, hash maps use the same [API request](../../cloud-services/memory-stores/index.md#api-requests-limits) and [memory quota](../../cloud-services/memory-stores/index.md#memory-size-quota) limits as the other memory store data structures.

## Get a hash map

To get a hash map, call `Class.MemoryStoreService:GetHashMap()` with a name for the hash map. The name is global within the experience, so you can access the same hash map on any script using this name.

```lua title="Getting a Hash Map"
local MemoryStoreService = game:GetService("MemoryStoreService")

local hashMap = MemoryStoreService:GetHashMap("HashMap1")
```

After you get a hash map, call any of the following functions to read or write data in it:

<table>
<thead>
  <tr>
    <th>Function</th>
    <th>Action</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>`Class.MemoryStoreHashMap:SetAsync()`</td>
    <td>[Add](#add-or-overwrite-data) a new key or overwrite the value if the key already exists.</td>
  </tr>
  <tr>
    <td>`Class.MemoryStoreHashMap:GetAsync()`</td>
    <td>[Read](#get-data) a particular key.</td>
  </tr>
	<tr>
    <td>`Class.MemoryStoreHashMap:ListItemsAsync()`</td>
    <td>[List](#get-data) items in a hash map.</td>
  </tr>
  <tr>
    <td>`Class.MemoryStoreHashMap:UpdateAsync()`</td>
    <td>[Update](#update-data) the value of a key after retrieving it from a hash map.</td>
  </tr>
  <tr>
    <

[Content truncated - see full docs]

---

## Memory stores

`Class.MemoryStoreService` is a high throughput and low latency data service that provides fast in-memory data storage accessible from all servers in a live session. **Memory Stores** are suitable for frequent and ephemeral data that change rapidly and don't need to be durable, because they are faster to access and vanish when reaching the maximum lifetime. For data that needs to persist across sessions, use [data stores](../../cloud-services/data-stores/index.md).

## Data structures

Instead of directly accessing raw data, memory stores have three primitive data structures shared across servers for quick processing: [sorted map](../../cloud-services/memory-stores/sorted-map.md), [queue](../../cloud-services/memory-stores/queue.md), and [hash map](../../cloud-services/memory-stores/hash-map.md). Each data structure is a good fit for certain use cases:

- **Skill-based matchmaking** - Save user information, such as skill level, in a shared **queue** among servers, and use lobby servers to run matchmaking periodically.
- **Cross-server trading and auctioning** - Enable universal trading between different servers, where users can bid on items with real-time changing prices, with a **sorted map** of key-value pairs.
- **Global leaderboards** - Store and update user rankings on a shared leaderboard inside a **sorted map**.
- **Shared inventories** - Save inventory items and statistics in a shared **hash map**, where users can utilize inventory items concurrently with one another.
- **Cache for Persistent Data** - Sync and copy your persistent data in a data store to a memory store **hash map** that can act as a cache and improve your experience's performance.

```mermaid
graph TD
    A[Does your data need to be sorted in a specific order?]
    B[Use a sorted map.]
    C[Do you need the ability to scan all of your items at once?]
    D[Use a hash map.]
    E[Do you expect to have fewer than 1,000 keys?]

    A -- YES --> B
    A -- NO --> C

    C -- YES --> E
    C -- N

[Content truncated - see full docs]

---

## Memory store observability

The memory stores observability dashboard provides real-time charts on your memory usage and API requests. It also has a built-in alert system that notifies you by email when an issue arises to help you troubleshoot in sync. For further information about specific errors, you can view your [Error Report](../../production/analytics/error-report.md) to find the error logs.

## Access the dashboard

The memory stores observability dashboard is available for any experience using `Class.MemoryStoreService`, but you must either be the experience owner or have [analytics group permissions](../../production/analytics/analytics-dashboard.md#grant-group-permission) to access the dashboard.

To access the dashboard:

1. Navigate to the [Creations](https://create.roblox.com/dashboard/creations) page on the **Creator Dashboard**.
2. Expand the account switcher in the upper-left and select your account or the group owning the target experience.
3. Select the experience.
4. In the **Monitoring** dropdown, select **Memory Stores**.

## Available charts

The dashboard includes two categories of line graphs:

- **Quota Usage** charts for tracking your usage compared to the [dynamically allocated quotas](../../cloud-services/memory-stores/index.md#limits-and-quotas), which are calculated based on the number of users in your experience.
  - **Memory Usage** on your memory usage per minute in bytes compared to how much your allocated quota left.
  - **API Request Unit** on your total request units per minute compared to how much your allocated quota left. This chart can be broken down by each API method.
- **API Usage and Performance** charts for monitoring the API usage pattern and performance based on API method and response status.
  - **Request Count by API** on API request count per minute by API method, such as `Class.MemoryStoreQueue:ReadAsync()` or `Class.MemoryStoreSortedMap:UpdateAsync()`.
  - **Request Count by Status** on API request count by [response status](#response-statu

[Content truncated - see full docs]

---

## Partitions and data distribution

With the release of the `Class.MemoryStoreHashMap` data structure, Roblox removed all existing limits for individual data structures and replaced them with a single, global "per-partition" throttling limit. The exact limit fluctuates based on internal values and how the automatic partitioning process distributes your data, but generally allows for much higher usage before throttling, particularly for hash maps. This new limit enables flexible usage of memory stores across all data structures.

## Partitions

The MemoryStores API stores data on _partitions_, which are just subdivisions of storage. Whenever you write an item to a memory store, that item is stored on exactly one partition. Partitions are fully managed by the MemoryStores API; you do not need to manage them yourself.

## Partition assignment

Partition storage is different according to the data structure an item is being stored on. For sorted maps and queues, each data structure is assigned a single partition.

For example, consider a carnival game with a sorted map called `PlayerScores` and a queue called `PlayerLine` of players waiting to play the game:

<img src="../../assets/data/memory-store/Per-Partition-Limits-1.png" width="100%" />

Unlike sorted maps and queues, hash maps are allotted multiple partitions, and data is automatically distributed across these partitions. If you were to add a hash map called `Prizes`, the partitions might look like this:

<img src="../../assets/data/memory-store/Per-Partition-Limits-3.png" width="100%" />

Note how the hash map exists on all partitions, and each partition has some subset of items.

## Limits

Having a per-partition limit allows for higher throughput to all data structures. It also favors hash maps, because they're distributed across all partitions.

For example, consider an example per-partition limit of 50,000 requests per minute (RPM):

- In the very best case, a sorted map and a queue are limited to 50,000 RPM, because each one resides on a singl

[Content truncated - see full docs]

---

## Memory store queue

A **queue** is a linear data structure with a collection of items that either follows the first-in-first-out (FIFO) principle or prioritizes elements based on predefined criteria. [Memory stores](../../cloud-services/memory-stores/index.md) support two types of queue, the FIFO [regular queues](../../luau/queues.md#regular-queues) and [priority queues](../../luau/queues.md#priority-queues). Both types share the same set of functions for initializing an empty queue, adding data to the queue, reading data from the queue, and removing data from the queue.

Memory store queues are useful for order-based processing and storing user information, such as skill levels, to facilitate matchmaking based on your desired criteria. For example, you can add a lobby place as the start place of your experience, use memory store queues as a centralized user information storage system accessible by multiple servers, manage the placement order of users using the queues, and teleport user who have completed the matchmaking to the main place of your experience.

## Get a queue

To get a queue, call `Class.MemoryStoreService:GetQueue()` with a **name**, which is global within the experience for any script to access, and an optional **invisibility timeout** in seconds, which prevents duplicated processing of the same queue item. Invisibility timeout is 30 seconds by default if you leave it empty like the following code sample.

```lua title="Getting an Empty Queue"
local MemoryStoreService = game:GetService("MemoryStoreService")

local queue = MemoryStoreService:GetQueue("Queue1")
```

When a queue is processing an item in it, the invisibility timeout applies to the item, turning it invisible from being processed by other servers, as multiple servers can update the queue concurrently. Though it's expected to complete both read and removal operations for an item during the invisibility timeout duration, if an error occurs that causes the item to remain in the queue after the timeout elapses,

[Content truncated - see full docs]

---

## Memory store sorted map

The **sorted map** data structure of [memory stores](../../cloud-services/memory-stores/index.md) allows you to store frequent in-memory data as key-value pairs with an optional sort key and maintain a specific order based on the sort keys and keys. Unlike queues, the order of keys entering a map doesn't determine the order of processing, making sorted maps useful for sorting based data organization for implementing in-experience entities for engagement such as leaderboards and cross-server auctioning.

## Limits

In addition to the [data structure size limits](../../cloud-services/memory-stores/index.md#data-structure-size-limits), sorted maps have a key size limit of 128 characters, a value size limit of 32 KB, and a sort key size limit of 128 characters.

If you need to store data that surpasses this limit for your experience, you can adopt the sharding technique to split and distribute them through **key prefix** into multiple data structures. Sharding memory stores can also help improve the scalability of your system.

## Get a sorted map

To get a sorted map, call `Class.MemoryStoreService:GetSortedMap()` with a **name** you want to define for the map. The name is global within the experience, so you can access the same sorted map on any script using the name.

```lua title="Getting a Sorted Map"
local MemoryStoreService = game:GetService("MemoryStoreService")

local sortedMap = MemoryStoreService:GetSortedMap("SortedMap1")
```

After you get a sorted map, call any of the following functions:

<table>
<thead>
  <tr>
    <th>Function</th>
    <th>Action</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>`Class.MemoryStoreSortedMap:SetAsync()`</td>
    <td>[Add](#add-or-overwrite-data) a new key or overwrite the value and/or sort key if the key already exists.</td>
  </tr>
  <tr>
    <td>`Class.MemoryStoreSortedMap:GetAsync()`</td>
    <td>[Read](#get-data) a particular key.</td>
  </tr>
  <tr>
    <td>`Class.MemoryStoreSortedMap:GetRangeAsync()`</td>
    <td>[Read](#

[Content truncated - see full docs]

---

