# MongoDB

**Category**: databases
**Description**: MongoDB NoSQL database drivers and ODMs
**Homepage**: https://www.mongodb.com

## Package Detection

### NPM
*Node.js MongoDB clients and ODMs*

- `mongodb`
- `mongoose`
- `mongoist`
- `monk`

### PYPI
*Python MongoDB drivers and ODMs*

- `pymongo`
- `motor`
- `mongoengine`
- `odmantic`

### RUBYGEMS
*Ruby MongoDB drivers and ODMs*

- `mongo`
- `mongoid`

### MAVEN
*Java MongoDB drivers*

- `org.mongodb:mongodb-driver-sync`
- `org.mongodb:mongo-java-driver`

### GO
*Go MongoDB driver*

- `go.mongodb.org/mongo-driver`

### Related Packages
- `mongodb-memory-server`
- `@typegoose/typegoose`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]mongodb['"]`
- Type: esm_import

**Pattern**: `require\(['"]mongodb['"]\)`
- Type: commonjs_require

**Pattern**: `from\s+['"]mongoose['"]`
- Type: esm_import

**Pattern**: `require\(['"]mongoose['"]\)`
- Type: commonjs_require

### Python

**Pattern**: `import\s+pymongo`
- Type: python_import

**Pattern**: `from\s+pymongo`
- Type: python_import

**Pattern**: `import\s+motor`
- Type: python_import

**Pattern**: `from\s+mongoengine`
- Type: python_import

### Go

**Pattern**: `"go\.mongodb\.org/mongo-driver`
- Type: go_import

## Environment Variables

*MongoDB connection URI*

*MongoDB connection URL*

*MongoDB connection URL (alternative)*

*MongoDB host*

*MongoDB port*

*MongoDB database name*

*MongoDB username*

*MongoDB password*


## Detection Notes

- Check for MONGODB_URI or MONGO_URL in environment
- Look for mongodb:// or mongodb+srv:// connection strings
- Common with Mongoose ODM in Node.js

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
