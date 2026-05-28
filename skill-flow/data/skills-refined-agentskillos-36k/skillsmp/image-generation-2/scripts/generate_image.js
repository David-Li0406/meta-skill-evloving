#!/usr/bin/env node
/**
 * Alibaba Cloud DashScope Image Generation Tool - Fast Version
 * Uses non-streaming response for faster speed.
 * Usage: node generate_image.js "your prompt"
 */

const https = require("https");
const http = require("http");
const fs = require("fs");
const { URL } = require("url");

// Get API Key from environment variables
const API_KEY = process.env.DASHSCOPE_API_KEY;

if (!API_KEY) {
  console.error(
    "❌ Error: Please set the DASHSCOPE_API_KEY environment variable."
  );
  console.error(
    'Usage: DASHSCOPE_API_KEY=your_key node generate_image.js "prompt"'
  );
  process.exit(1);
}

// Get prompt from command line arguments
const prompt = process.argv[2];

if (!prompt) {
  console.error("❌ Error: Please provide a prompt.");
  console.error('Usage: node generate_image.js "your prompt"');
  process.exit(1);
}

console.log("🎨 Starting image generation...");
console.log(`📝 Prompt: ${prompt}`);
console.log("");

const startTime = Date.now();

// Request configuration - using non-streaming response
const requestData = JSON.stringify({
  model: "gemini-3-pro-image-preview",
  dashscope_extend_params: {
    using_native_protocol: true,
  },
  stream: false, // ⚡ Critical: Use non-streaming response
  contents: [
    {
      parts: [
        {
          text: prompt,
        },
      ],
      role: "user",
    },
  ],
  generationConfig: {
    responseModalities: ["text", "image"],
  },
});

const options = {
  hostname: "dashscope.aliyuncs.com",
  port: 443,
  path: "/compatible-mode/v1/chat/completions",
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${API_KEY}`,
    "Content-Length": Buffer.byteLength(requestData),
  },
};

// Send request
const req = https.request(options, (res) => {
  console.log(`📡 Response Status: ${res.statusCode}`);

  if (res.statusCode !== 200) {
    console.error(`❌ Request failed, status code: ${res.statusCode}`);
    res.on("data", (chunk) => {
      console.error(chunk.toString());
    });
    return;
  }

  let responseData = "";

  res.on("data", (chunk) => {
    responseData += chunk.toString();
    process.stdout.write(".");
  });

  res.on("end", () => {
    console.log("\n");
    const apiTime = ((Date.now() - startTime) / 1000).toFixed(2);
    console.log(`⏱️  API Response Time: ${apiTime}s`);

    try {
      const data = JSON.parse(responseData);

      // Extract image and text
      let imageUrl = null;
      let responseText = "";

      if (data.candidates && data.candidates[0]) {
        const parts = data.candidates[0].content?.parts || [];
        for (const part of parts) {
          if (part.text) {
            responseText += part.text;
          }
          if (part.inlineData) {
            imageUrl = part.inlineData.data;
            console.log("🖼️  Image data found!");
          }
        }
      }

      if (responseText) {
        console.log("💬 Generated Text:");
        console.log(responseText);
        console.log("");
      }

      if (imageUrl) {
        console.log("📥 Starting image download...");
        downloadImage(imageUrl, prompt, data, startTime);
      } else {
        console.log("⚠️  No image data found.");

        // Save response for debugging
        const debugFile = `debug_response_${Date.now()}.json`;
        fs.writeFileSync(debugFile, JSON.stringify(data, null, 2));
        console.log(`Debug info saved to: ${debugFile}`);
      }
    } catch (e) {
      console.error(`❌ Failed to parse response: ${e.message}`);
      const debugFile = `debug_response_${Date.now()}.txt`;
      fs.writeFileSync(debugFile, responseData);
      console.log(`Raw response saved to: ${debugFile}`);
    }
  });
});

req.on("error", (e) => {
  console.error(`❌ Request error: ${e.message}`);
});

req.write(requestData);
req.end();

/**
 * Downloads the image locally
 */
function downloadImage(url, promptText, fullResponse, startTime) {
  const downloadStartTime = Date.now();
  const urlObj = new URL(url);
  const protocol = urlObj.protocol === "https:" ? https : http;

  // Generate filename (using timestamp)
  const timestamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, -5);
  const filename = `image_${timestamp}.png`;
  const jsonFilename = `response_${timestamp}.json`;

  protocol
    .get(url, (response) => {
      if (response.statusCode === 200) {
        const fileStream = fs.createWriteStream(filename);

        let downloadedBytes = 0;
        response.on("data", (chunk) => {
          downloadedBytes += chunk.length;
          process.stdout.write(
            `\r📦 Downloaded: ${(downloadedBytes / 1024 / 1024).toFixed(2)} MB`
          );
        });

        response.pipe(fileStream);

        fileStream.on("finish", () => {
          fileStream.close();
          const downloadTime = (
            (Date.now() - downloadStartTime) /
            1000
          ).toFixed(2);
          const totalTime = ((Date.now() - startTime) / 1000).toFixed(2);

          console.log(`\n✅ Image saved: ${filename}`);
          console.log(
            `📊 File Size: ${(downloadedBytes / 1024 / 1024).toFixed(2)} MB`
          );
          console.log(`⏱️  Download Time: ${downloadTime}s`);
          console.log(`⏱️  Total Time: ${totalTime}s`);

          // Save complete JSON response
          if (fullResponse) {
            fs.writeFileSync(
              jsonFilename,
              JSON.stringify(fullResponse, null, 2)
            );
            console.log(`📄 Response data saved: ${jsonFilename}`);
          }

          // Save metadata
          const metadata = {
            prompt: promptText,
            imageUrl: url,
            filename: filename,
            timestamp: new Date().toISOString(),
            fileSize: downloadedBytes,
            timings: {
              apiResponse: `${((downloadStartTime - startTime) / 1000).toFixed(
                2
              )}s`,
              download: `${downloadTime}s`,
              total: `${totalTime}s`,
            },
          };
          fs.writeFileSync(
            `metadata_${timestamp}.json`,
            JSON.stringify(metadata, null, 2)
          );
          console.log(`📝 Metadata saved: metadata_${timestamp}.json`);
          console.log("\n🎉 Done!");
        });
      } else {
        console.error(
          `❌ Download failed, status code: ${response.statusCode}`
        );
      }
    })
    .on("error", (e) => {
      console.error(`❌ Download error: ${e.message}`);
    });
}
