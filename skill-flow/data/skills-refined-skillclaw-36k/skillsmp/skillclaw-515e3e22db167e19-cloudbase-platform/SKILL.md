---
name: cloudbase-platform
description: Use this skill for general CloudBase platform understanding, including storage, hosting, authentication, cloud functions, database permissions, and data models.
---

# When to use this skill

Use this skill for **CloudBase platform knowledge** when you need to:

- Understand CloudBase storage and hosting concepts
- Configure authentication for different platforms (Web vs Mini Program)
- Deploy and manage cloud functions
- Understand database permissions and access control
- Work with data models (MySQL and NoSQL)
- Access CloudBase console management pages

**This skill provides foundational knowledge** that applies to all CloudBase projects, regardless of whether they are Web, Mini Program, or backend services.

## How to use this skill (for a coding agent)

1. **Understand platform differences**
   - Web and Mini Program have completely different authentication approaches.
   - Must strictly distinguish between platforms; never mix authentication methods across platforms.

2. **Follow best practices**
   - Use SDK built-in authentication features for Web.
   - Understand the natural login-free feature for Mini Program.
   - Configure appropriate database permissions.
   - Use cloud functions for cross-collection operations.

3. **Use correct SDKs and APIs**
   - Different platforms require different SDKs for data models.
   - MySQL data models must use the models SDK, not the collection API.
   - Use the `envQuery` tool to get the environment ID.

## CloudBase Platform Knowledge

### Storage and Hosting

1. **Static Hosting vs Cloud Storage**:
   - CloudBase static hosting and cloud storage are two different buckets.
   - Publicly accessible files can be stored in static hosting, which provides a public web address.
   - Static hosting supports custom domain configuration (requires console operation).
   - Cloud storage is suitable for files with privacy requirements; temporary access addresses can be obtained via temporary file URLs.

2. **Static Hosting Domain**:
   - The CloudBase static hosting domain can be obtained via the `getWebsiteConfig` tool.
   - Combine with static hosting file paths to construct final access addresses.
   - **Important**: If the access address is a directory, it must end with `/`.

### Environment and Authentication

1. **SDK Initialization**:
   - CloudBase SDK initialization requires an environment ID.
   - The environment ID can be queried via the `envQuery` tool.