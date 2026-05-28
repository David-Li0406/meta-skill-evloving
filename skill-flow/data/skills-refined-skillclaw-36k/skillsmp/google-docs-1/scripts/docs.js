const https = require('https');
const url = require('url');
const fs = require('fs');
const path = require('path');

// Mime Type mappings for Local files (Upload)
const LOCAL_MIME_MAP = {
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.png': 'image/png',
  '.gif': 'image/gif',
  '.bmp': 'image/bmp'
};

function makeRequest(method, requestUrl, headers, body = null) {
  return new Promise((resolve, reject) => {
    const parsedUrl = url.parse(requestUrl);
    const options = {
      hostname: parsedUrl.hostname,
      path: parsedUrl.path,
      method: method,
      headers: headers
    };

    const req = https.request(options, (res) => {
      let responseBody = '';

      res.on('data', (chunk) => {
        responseBody += chunk;
      });

      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            const json = JSON.parse(responseBody);
            resolve(json);
          } catch (e) {
            resolve(responseBody);
          }
        } else {
          reject(new Error(`Request failed with status code ${res.statusCode}: ${responseBody}`));
        }
      });
    });

    req.on('error', (e) => {
      reject(e);
    });

    if (body) {
      req.write(body);
    }
    req.end();
  });
}

function uploadFileRequest(method, requestUrl, headers, metadata, fileContentBuffer, mediaMimeType) {
  return new Promise((resolve, reject) => {
    const boundary = '-------314159265358979323846';
    const delimiter = Buffer.from("\r\n--" + boundary + "\r\n");
    const close_delim = Buffer.from("\r\n--" + boundary + "--");

    const part1 = Buffer.from(
      'Content-Type: application/json\r\n\r\n' +
      JSON.stringify(metadata)
    );

    const part2Header = Buffer.from('Content-Type: ' + mediaMimeType + '\r\n\r\n');

    const multipartRequestBody = Buffer.concat([
      delimiter,
      part1,
      delimiter,
      part2Header,
      fileContentBuffer,
      close_delim
    ]);

    const parsedUrl = url.parse(requestUrl);
    const options = {
      hostname: parsedUrl.hostname,
      path: parsedUrl.path,
      method: method,
      headers: Object.assign({}, headers, {
        'Content-Type': 'multipart/related; boundary="' + boundary + '"',
        'Content-Length': multipartRequestBody.length
      })
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            resolve(JSON.parse(body));
          } catch (e) {
            resolve(body);
          }
        } else {
          reject(new Error(`Upload failed (${res.statusCode}): ${body}`));
        }
      });
    });

    req.on('error', (e) => reject(e));
    req.write(multipartRequestBody);
    req.end();
  });
}

async function setFilePublic(fileId, headers) {
  const requestUrl = `https://www.googleapis.com/drive/v3/files/${fileId}/permissions`;
  const body = JSON.stringify({ role: 'reader', type: 'anyone' });
  await makeRequest('POST', requestUrl, headers, body);
}

async function deleteFile(fileId, headers) {
  const requestUrl = `https://www.googleapis.com/drive/v3/files/${fileId}`;
  await makeRequest('DELETE', requestUrl, headers);
  console.log(`Deleted temporary file ${fileId}`);
}

async function uploadLocalFile(filePath, headers) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`File not found: ${filePath}`);
  }

  const buffer = fs.readFileSync(filePath);
  const ext = path.extname(filePath).toLowerCase();
  const basename = path.basename(filePath);
  const mediaMimeType = LOCAL_MIME_MAP[ext] || 'application/octet-stream';

  console.log(`Uploading '${basename}' to Drive...`);
  const url = 'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name,webViewLink,webContentLink';
  const metadata = { name: basename };

  const result = await uploadFileRequest('POST', url, headers, metadata, buffer, mediaMimeType);
  console.log(`Uploaded. File ID: ${result.id}`);
  return result.id;
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  const token = process.env.GCLOUD_ACCESS_TOKEN;

  if (!token) {
    console.error("Error: GCLOUD_ACCESS_TOKEN environment variable is required.");
    process.exit(1);
  }

  const headers = {
    'Authorization': `Bearer ${token}`,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  };

  try {
    if (command === 'read') {
      const docId = args[1];
      if (!docId) {
        console.error("Usage: node docs.js read <docId> [--tabId=<tabId>]");
        process.exit(1);
      }

      let tabId = null;
      for (let i = 2; i < args.length; i++) {
        if (args[i].startsWith('--tabId=')) {
          tabId = args[i].split('=')[1];
        }
      }

      const requestUrl = tabId 
        ? `https://docs.googleapis.com/v1/documents/${docId}?includeTabsContent=true`
        : `https://docs.googleapis.com/v1/documents/${docId}`;
      
      const data = await makeRequest('GET', requestUrl, headers);

      if (tabId) {
        const findTab = (tabs, id) => {
          for (const tab of tabs) {
            if (tab.tabId === id) return tab;
            // The API returns tabProperties with tabId
            if (tab.tabProperties && tab.tabProperties.tabId === id) return tab;
            if (tab.childTabs) {
              const found = findTab(tab.childTabs, id);
              if (found) return found;
            }
          }
          return null;
        };

        const targetTab = findTab(data.tabs || [], tabId);
        if (targetTab) {
          console.log(JSON.stringify(targetTab, null, 2));
        } else {
          console.error(`Error: Tab with ID ${tabId} not found.`);
          process.exit(1);
        }
      } else {
        console.log(JSON.stringify(data, null, 2));
      }

    } else if (command === 'tabs') {
      const docId = args[1];
      if (!docId) {
        console.error("Usage: node docs.js tabs <docId>");
        process.exit(1);
      }
      const requestUrl = `https://docs.googleapis.com/v1/documents/${docId}?fields=tabs(tabProperties(tabId,title),childTabs)`;
      const data = await makeRequest('GET', requestUrl, headers);
      
      const listTabs = (tabs, level = 0) => {
        if (!tabs) return;
        tabs.forEach((tab, index) => {
          const indent = '  '.repeat(level);
          const props = tab.tabProperties || {};
          console.log(`${indent}${index}. ${props.title || 'Untitled'} (ID: ${props.tabId})`);
          if (tab.childTabs) {
            listTabs(tab.childTabs, level + 1);
          }
        });
      };
      
      if (data.tabs) {
        console.log(`Tabs in document ${docId}:`);
        listTabs(data.tabs);
      } else {
        console.log("No tabs found or document does not support tabs.");
      }

    } else if (command === 'create') {
      const title = args[1] || 'Untitled Document';
      const requestUrl = `https://docs.googleapis.com/v1/documents`;
      const body = JSON.stringify({ title: title });
      const data = await makeRequest('POST', requestUrl, headers, body);
      console.log(JSON.stringify(data, null, 2));

    } else if (command === 'edit') {
      const docId = args[1];
      let requestsJson = args[2];
      
      if (!docId || !requestsJson) {
        console.error("Usage: node docs.js edit <docId> <requests_json_string> [--file-<ID>=<PATH> ...]");
        process.exit(1);
      }

      const filesToUpload = {};
      // Parse file arguments
      for (let i = 3; i < args.length; i++) {
        const arg = args[i];
        const match = arg.match(/^--file-(.+)=(.+)$/);
        if (match) {
          const id = match[1];
          const path = match[2];
          filesToUpload[id] = path;
        }
      }

      const uploadedFiles = [];

      try {
        // Upload files and replace placeholders
        for (const [id, filePath] of Object.entries(filesToUpload)) {
          const fileId = await uploadLocalFile(filePath, headers);
          await setFilePublic(fileId, headers);
          uploadedFiles.push(fileId);
          
          const imageUrl = `https://drive.google.com/uc?export=view&id=${fileId}`;
          const placeholder = `FILE_${id}`;
          
          // Replace all occurrences of FILE_<ID> with the URL
          // Escape the placeholder for regex usage
          const escapedPlaceholder = placeholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
          requestsJson = requestsJson.replace(new RegExp(escapedPlaceholder, 'g'), imageUrl);
        }

        let requests;
        try {
          requests = JSON.parse(requestsJson);
          if (Array.isArray(requests)) {
              // It's just a list of requests
          } else if (requests.requests && Array.isArray(requests.requests)) {
              requests = requests.requests;
          } else {
              requests = [requests];
          }
        } catch (e) {
          console.error("Error parsing requests JSON:", e.message);
          throw e; // Re-throw to trigger cleanup
        }

        const requestUrl = `https://docs.googleapis.com/v1/documents/${docId}:batchUpdate`;
        const body = JSON.stringify({ requests: requests });
        const data = await makeRequest('POST', requestUrl, headers, body);
        console.log(JSON.stringify(data, null, 2));

      } catch (error) {
        console.error("Error during edit operation:", error.message);
        process.exitCode = 1;
      } finally {
        // Cleanup uploaded files
        if (uploadedFiles.length > 0) {
            console.log("Cleaning up temporary files...");
            for (const fileId of uploadedFiles) {
                try {
                    await deleteFile(fileId, headers);
                } catch (cleanupError) {
                    console.error(`Failed to delete temporary file ${fileId}:`, cleanupError.message);
                }
            }
        }
      }

    } else if (command === 'comments') {
      const docId = args[1];
      if (!docId) {
        console.error("Usage: node docs.js comments <docId>");
        process.exit(1);
      }
      // Comments are part of Drive API
      const requestUrl = `https://www.googleapis.com/drive/v3/files/${docId}/comments?fields=*`;
      const data = await makeRequest('GET', requestUrl, headers);
      console.log(JSON.stringify(data, null, 2));

    } else if (command === 'create_comment') {
      const docId = args[1];
      const content = args[2];
      const anchor = args[3];

      if (!docId || !content) {
        console.error("Usage: node docs.js create_comment <docId> <content> [anchor]");
        process.exit(1);
      }

      const requestUrl = `https://www.googleapis.com/drive/v3/files/${docId}/comments?fields=*`;
      const bodyObj = { content: content };
      if (anchor) {
        bodyObj.anchor = anchor;
      }
      const body = JSON.stringify(bodyObj);
      const data = await makeRequest('POST', requestUrl, headers, body);
      console.log(JSON.stringify(data, null, 2));

    } else if (command === 'reply_comment') {
      const docId = args[1];
      const commentId = args[2];
      const content = args[3];

      if (!docId || !commentId || !content) {
        console.error("Usage: node docs.js reply_comment <docId> <commentId> <content>");
        process.exit(1);
      }

      const requestUrl = `https://www.googleapis.com/drive/v3/files/${docId}/comments/${commentId}/replies?fields=*`;
      const body = JSON.stringify({ content: content });
      const data = await makeRequest('POST', requestUrl, headers, body);
      console.log(JSON.stringify(data, null, 2));

    } else if (command === 'resolve_comment') {
      const docId = args[1];
      const commentId = args[2];

      if (!docId || !commentId) {
        console.error("Usage: node docs.js resolve_comment <docId> <commentId>");
        process.exit(1);
      }

      const requestUrl = `https://www.googleapis.com/drive/v3/files/${docId}/comments/${commentId}/replies?fields=*`;
      const body = JSON.stringify({ action: 'resolve' });
      const data = await makeRequest('POST', requestUrl, headers, body);
      console.log(JSON.stringify(data, null, 2));

    } else if (command === 'insert_image') {
      let tabId = null;
      const positionalArgs = [];
      
      // Parse args starting from index 1 (skipping command name)
      for (let i = 1; i < args.length; i++) {
        if (args[i].startsWith('--tabId=')) {
          tabId = args[i].split('=')[1];
        } else {
          positionalArgs.push(args[i]);
        }
      }

      const docId = positionalArgs[0];
      const filePath = positionalArgs[1];
      const index = parseInt(positionalArgs[2], 10);
      const width = positionalArgs[3]; // Optional
      const height = positionalArgs[4]; // Optional

      if (!docId || !filePath || isNaN(index)) {
        console.error("Usage: node docs.js insert_image <docId> <filePath> <index> [width] [height] [--tabId=TAB_ID]");
        process.exit(1);
      }

      // 1. Upload the file to Drive
      const fileId = await uploadLocalFile(filePath, headers);

      // 2. Make it public so Docs API can read it
      await setFilePublic(fileId, headers);

      // 3. Construct the image URL
      const imageUrl = `https://drive.google.com/uc?export=view&id=${fileId}`;

      // 4. Create the batchUpdate request
      const request = {
        insertInlineImage: {
          uri: imageUrl,
          location: {
            index: index
          }
        }
      };
      
      if (tabId) {
        request.insertInlineImage.location.tabId = tabId;
      }

      if (width && height) {
        request.insertInlineImage.objectSize = {
          height: { magnitude: parseFloat(height), unit: 'PT' },
          width: { magnitude: parseFloat(width), unit: 'PT' }
        };
      }

      const requestUrl = `https://docs.googleapis.com/v1/documents/${docId}:batchUpdate`;
      const body = JSON.stringify({ requests: [request] });
      
      console.log("Inserting image into document...");
      const data = await makeRequest('POST', requestUrl, headers, body);
      console.log(JSON.stringify(data, null, 2));

    } else if (command === 'create_tab') {
      const docId = args[1];
      let tabTitle = null;
      let parentTabId = null;
      let tabIndex = null;
      let emoji = null;

      if (!docId) {
        console.error("Usage: node docs.js create_tab <docId> [title] [--parentTabId=ID] [--index=N] [--emoji=EMOJI]");
        process.exit(1);
      }

      for (let i = 2; i < args.length; i++) {
        const arg = args[i];
        if (arg.startsWith('--parentTabId=')) {
          parentTabId = arg.split('=')[1];
        } else if (arg.startsWith('--index=')) {
          tabIndex = parseInt(arg.split('=')[1], 10);
        } else if (arg.startsWith('--emoji=')) {
          emoji = arg.split('=')[1];
        } else if (!arg.startsWith('--') && !tabTitle) {
          tabTitle = arg;
        }
      }

      if (!tabTitle) {
        tabTitle = 'New Tab';
      }

      const requestObj = {
        addDocumentTab: {
          tabProperties: {
            title: tabTitle
          }
        }
      };

      if (parentTabId) {
        requestObj.addDocumentTab.tabProperties.parentTabId = parentTabId;
      }

      if (tabIndex !== null && !isNaN(tabIndex)) {
        requestObj.addDocumentTab.tabProperties.index = tabIndex;
      }

      if (emoji) {
        requestObj.addDocumentTab.tabProperties.iconEmoji = emoji;
      }

      const requestUrl = `https://docs.googleapis.com/v1/documents/${docId}:batchUpdate`;
      const body = JSON.stringify({
        requests: [requestObj]
      });
      const data = await makeRequest('POST', requestUrl, headers, body);
      console.log(JSON.stringify(data, null, 2));

    } else {
      console.error("Unknown command. Use 'read', 'tabs', 'create', 'create_tab', 'edit', 'comments', 'create_comment', 'reply_comment', 'resolve_comment', or 'insert_image'.");
      process.exit(1);
    }
  } catch (error) {
    console.error("Error:", error.message);
    process.exit(1);
  }
}

main();
