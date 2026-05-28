#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import axios from 'axios';
import FormData from 'form-data';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load environment variables from central secrets location
dotenv.config({ path: path.join(__dirname, '../../secrets/wistia/.env') });

/**
 * Parse command line arguments
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const params = {
    file: null,
    project: '8b0i9mexdc', // Default project: Customer Interviews
    name: null,
    description: null
  };

  args.forEach(arg => {
    const [key, value] = arg.split('=');
    const cleanKey = key.replace('--', '');

    if (cleanKey === 'file') {
      params.file = value?.replace(/^["']|["']$/g, ''); // Remove quotes
    } else if (cleanKey === 'project') {
      params.project = value?.replace(/^["']|["']$/g, '');
    } else if (cleanKey === 'name') {
      params.name = value?.replace(/^["']|["']$/g, '');
    } else if (cleanKey === 'description') {
      params.description = value?.replace(/^["']|["']$/g, '');
    }
  });

  return params;
}

/**
 * Validate setup and parameters
 */
function validate(params) {
  const errors = [];

  // Check API token
  if (!process.env.WISTIA_API_TOKEN) {
    errors.push('WISTIA_API_TOKEN not found in .env file');
  }

  // Check file parameter
  if (!params.file) {
    errors.push('--file parameter is required');
  } else if (!fs.existsSync(params.file)) {
    errors.push(`File not found: ${params.file}`);
  } else {
    const ext = path.extname(params.file).toLowerCase();
    const supportedFormats = ['.mp4', '.mov', '.avi', '.wmv', '.flv', '.mkv', '.webm', '.ogv', '.mpg', '.mpeg'];
    if (!supportedFormats.includes(ext)) {
      errors.push(`Unsupported video format: ${ext}. Supported formats: ${supportedFormats.join(', ')}`);
    }
  }

  return errors;
}

/**
 * Upload video to Wistia
 */
async function uploadToWistia(params) {
  const apiToken = process.env.WISTIA_API_TOKEN;
  const filePath = params.file;
  const fileName = params.name || path.basename(filePath);

  // Create form data
  const form = new FormData();
  form.append('file', fs.createReadStream(filePath));

  if (params.project) {
    form.append('project_id', params.project);
  }

  if (params.name) {
    form.append('name', params.name);
  }

  if (params.description) {
    form.append('description', params.description);
  }

  try {
    // Upload to Wistia
    const response = await axios.post('https://upload.wistia.com/', form, {
      headers: {
        ...form.getHeaders(),
        'Authorization': `Bearer ${apiToken}`
      },
      maxContentLength: Infinity,
      maxBodyLength: Infinity
    });

    // Parse response
    const video = response.data;
    const wistiaAccount = process.env.WISTIA_ACCOUNT || 'yourname';
    const accountUrl = `${wistiaAccount}.wistia.com`;

    return {
      success: true,
      video_id: video.hashed_id,
      name: video.name,
      url: `https://${accountUrl}/medias/${video.hashed_id}`,
      embed_url: `https://fast.wistia.net/embed/iframe/${video.hashed_id}`,
      thumbnail_url: video.thumbnail?.url,
      duration: video.duration,
      transcript_url: `https://${accountUrl}/medias/${video.hashed_id}/captions`,
      created: video.created,
      project_id: video.project?.id
    };

  } catch (error) {
    // Handle errors
    let errorMessage = 'Upload failed';
    let errorCode = error.response?.status;

    if (errorCode === 401) {
      errorMessage = 'Authentication failed. Check your WISTIA_API_TOKEN in .env file';
    } else if (errorCode === 404) {
      errorMessage = 'Project not found. Check the project ID';
    } else if (errorCode === 413) {
      errorMessage = 'File is too large. Check your Wistia account limits';
    } else if (error.code === 'ENOENT') {
      errorMessage = `File not found: ${filePath}`;
    } else if (error.response?.data) {
      errorMessage = error.response.data.error || error.message;
    } else {
      errorMessage = error.message;
    }

    return {
      success: false,
      error: errorMessage,
      error_code: errorCode
    };
  }
}

/**
 * Main execution
 */
async function main() {
  const params = parseArgs();

  // Validate
  const errors = validate(params);
  if (errors.length > 0) {
    console.error(JSON.stringify({
      success: false,
      errors: errors
    }, null, 2));
    process.exit(1);
  }

  // Show upload start
  const fileSize = fs.statSync(params.file).size;
  const fileSizeMB = (fileSize / (1024 * 1024)).toFixed(2);

  console.error(`Uploading ${path.basename(params.file)} (${fileSizeMB} MB) to Wistia...`);

  // Upload
  const result = await uploadToWistia(params);

  // Output result as JSON
  console.log(JSON.stringify(result, null, 2));

  // Exit with appropriate code
  process.exit(result.success ? 0 : 1);
}

main();
