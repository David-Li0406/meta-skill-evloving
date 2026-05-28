---
name: mongodb
description: MongoDB database operations including connection, queries, indexes, aggregation, transactions, and bulk operations.
---

# MongoDB — Comprehensive Guide

**Connection**

```powershell
.\mongosh.exe "mongodb+srv://?/" --apiVersion 1 --username ?
docker run -ti --rm alpine/mongosh mongosh "mongodb://user:pass@host:27017/db"
docker run -e ME_CONFIG_MONGODB_SERVER=mongodb -e ME_CONFIG_MONGODB_ENABLE_ADMIN=false -e ME_CONFIG_MONGODB_AUTH_DATABASE=db -e ME_CONFIG_MONGODB_AUTH_USERNAME=user -e ME_CONFIG_MONGODB_AUTH_PASSWORD=pass  -p 8085:8081 mongo-express
```

**Basic Queries**

```javascript
db.inventory.insertMany([
  { item: "journal", qty: 25, size: { h: 14, w: 21, uom: "cm" }, status: "A" },
  ...
]);

db.inventory.find({ item: { $in: ["paper"] } }, { item: 1 });
```


**Indexes**
```javascript
db.collection.createIndex({ field: 1 });  // 1 for ascending, -1 for descending
db.collection.getIndexes();
```

**Aggregation**
```javascript
db.orders.aggregate([
  { $match: { status: "A" } },
  { $group: { _id: "$cust_id", total: { $sum: "$amount" } } }
]);
```

**Replica Set Status**
```bash
mongosh --eval "rs.status()"
```

## MongoDB — Expert Techniques

**Transactions**
```javascript
session = db.getMongo().startSession();
session.startTransaction();
try {
  db.orders.insertOne({ item: "book" }, { session });
  db.inventory.updateOne({ item: "book" }, { $inc: { qty: -1 } }, { session });
  session.commitTransaction();
} catch (e) {
  session.abortTransaction();
}
```

**Bulk Operations**
```javascript
const bulk = db.items.initializeUnorderedBulkOp();
bulk.insert({ item: "laptop" });
bulk.insert({ item: "monitor" });
bulk.execute();
```

**Text Search**
```javascript
db.articles.createIndex({ content: "text" });
db.articles.find({ $text: { $search: "database" } });
```