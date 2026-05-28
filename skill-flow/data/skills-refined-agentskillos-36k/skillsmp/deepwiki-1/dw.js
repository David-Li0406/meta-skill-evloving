#!/usr/bin/env node

const { EventSource } = require('eventsource');
const axios = require('axios');
const path = require('path');

const MCP_ENDPOINT = 'https://mcp.deepwiki.com/sse';

// Type definitions for view_share response

// Response type handlers
const RESPONSE_HANDLERS = {
  'module_call_id': (item) => {
    return `[Module Call ID: ${item.data?.module_call_id}]`;
  },
  'loading_indexes': (item) => {
    const data = item.data;
    const progress = data.type === 'all_indexes' ? 'Complete' : 'Loading';
    return `[${progress}: ${data.type}${data.durationSeconds ? ` (${data.durationSeconds.toFixed(2)}s)` : ''}]`;
  },
  'file_contents': (item) => {
    const [repo, filePath, content] = item.data || [];
    return {
      type: 'file',
      repo,
      filePath,
      content
    };
  },
  'file_path_range': (item) => {
    const { file_path, range_start, range_end } = item.data || {};
    return `[File Range: ${file_path} (${range_start}-${range_end})]`;
  },
  'stats': (item) => {
    const { key, value } = item.data || {};
    const duration = value ? ` ${value.toFixed(2)}ms` : '';
    return `[Stats: ${key}${duration}]`;
  },
  'text': (item) => {
    return {
      type: 'text',
      content: item.data
    };
  },
  'error': (item) => {
    return `[Error: ${JSON.stringify(item.data)}]`;
  },
  'unknown': (item) => {
    return `[Unknown type: ${item.type}]`;
  }
};

// Parse and format shared query response
function formatSharedQueryResponse(data, format = 'full') {
  if (format === 'json') {
    return [{ type: 'text', content: JSON.stringify(data, null, 2) }];
  }

  if (!data.queries || data.queries.length === 0) {
    return [{ type: 'text', content: JSON.stringify(data, null, 2) }];
  }

  const query = data.queries[0];
  const result = [];

  // Clean title by removing relevant_context tags if present
  const cleanTitle = (text) => {
    if (!text) return '';
    return text.replace(/<relevant_context>[\s\S]*?<\/relevant_context>/g, '').trim() || text;
  };

  // Display title and query information
  const displayTitle = cleanTitle(data.title) || cleanTitle(query.user_query) || 'DeepWiki Query Result';
  result.push({ type: 'header', content: displayTitle });

  if (format === 'full' && query.repos && query.repos.length > 0) {
    const repoList = query.repos.map(r => r.name).join(', ');
    result.push({ type: 'header', content: `📚 Repos: ${repoList}` });
  }

  if (format === 'full' && query.engine_id) {
    result.push({ type: 'info', content: `🔍 Engine: ${query.engine_id}` });
  }

  if (!query.response || query.response.length === 0) {
    if (query.error) {
      result.push({ type: 'error', content: JSON.stringify(query.error, null, 2) });
    } else {
      result.push({ type: 'info', content: 'No response data available' });
    }
    return result;
  }

  // Filter response types based on format
  const skipTypes = format === 'brief'
    ? ['loading_indexes', 'stats', 'module_call_id', 'file_path_range', 'unknown']
    : ['loading_indexes', 'stats', 'module_call_id', 'unknown'];

  query.response.forEach(item => {
    if (skipTypes.includes(item.type)) return;

    const handler = RESPONSE_HANDLERS[item.type];
    if (!handler) return;

    const formatted = handler(item);

    if (typeof formatted === 'string') {
      result.push({ type: 'info', content: formatted });
    } else if (formatted.type === 'file') {
      result.push({
        type: 'file',
        repo: formatted.repo,
        filePath: formatted.filePath,
        content: formatted.content
      });
    } else if (formatted.type === 'text') {
      result.push(formatted);
    }
  });

  if (query.error) {
    result.push({ type: 'error', content: `Error: ${JSON.stringify(query.error)}` });
  }

  return result;
}

// Display formatted response
function displayFormattedResponse(formattedItems) {
  formattedItems.forEach(item => {
    switch (item.type) {
      case 'header':
        console.log(`\n${'█'.repeat(70)}`);
        console.log(`  ${item.content}`);
        console.log(`${'█'.repeat(70)}`);
        break;
      case 'file':
        if (item.filePath && item.content) {
          const repoPrefix = item.repo ? `${item.repo}/` : '';
          console.log(`\n${'─'.repeat(70)}`);
          console.log(`📄 ${repoPrefix}${item.filePath}`);
          console.log(`${'─'.repeat(70)}`);
          console.log(item.content);
        }
        break;
      case 'text':
        console.log(item.content);
        break;
      case 'info':
        console.log(item.content);
        break;
      case 'error':
        console.log(`\n❌ ${item.content}`);
        break;
    }
  });
}

// i18n messages
const MESSAGES = {
  en: {
    usage: 'Usage: deepwiki <command> [options]',
    description: 'A CLI tool for retrieving GitHub repository documentation and knowledge via DeepWiki',
    commands: {
      'read_wiki_structure': 'Get repository documentation structure',
      'rws': '[alias] Get repository documentation structure',
      'read_wiki_contents': 'Read specific documentation content',
      'rwc': '[alias] Read specific documentation content',
      'ask_question': 'Ask questions about the repository',
      'aq': '[alias] Ask questions about the repository',
      'view_share': 'View shared query result by UUID',
      'vs': '[alias] View shared query result by UUID'
    },
    options: {
      repoName: 'Repository name (e.g., "owner/repo")',
      topic: 'Documentation topic name',
      question: 'Your question about the repository',
      uuid: 'Share query UUID (e.g., "_5495e609-f29e-44a7-a7bf-91c3f8f76303")',
      format: 'Output format (brief|full|json, default: full)'
    },
    examples: {
      structure: '  deepwiki read_wiki_structure --repoName "openai/openai-node"',
      contents: '  deepwiki read_wiki_contents --repoName "openai/openai-node" --topic "Installation"',
      question: '  deepwiki ask_question --repoName "openai/openai-node" --question "How to authenticate?"',
      share: '  deepwiki view_share --uuid "_5495e609-f29e-44a7-a7bf-91c3f8f76303"',
      shareBrief: '  deepwiki view_share --uuid "..." --format brief',
      shareJson: '  deepwiki view_share --uuid "..." --format json'
    },
    errors: {
      noCommand: 'Error: No command provided',
      invalidCommand: 'Error: Invalid command',
      missingRepo: 'Error: --repoName is required',
      missingTopic: 'Error: --topic is required',
      missingQuestion: 'Error: --question is required',
      missingUuid: 'Error: --uuid is required',
      connectionFailed: 'Error: SSE connection failed',
      requestFailed: 'Error: Request failed',
      timeout: 'Error: Timeout - no response from server'
    },
    help: {
      title: 'Help',
      commandsSection: 'Commands:',
      optionsSection: 'Options:',
      examplesSection: 'Examples:',
      seeAlso: 'For more information, visit: https://github.com/Dwsy/deepwiki-skills'
    }
  },
  zh: {
    usage: '用法: deepwiki <命令> [选项]',
    description: '通过 DeepWiki MCP SSE 协议获取 GitHub 仓库文档和知识的 CLI 工具',
    commands: {
      'read_wiki_structure': '获取仓库文档结构',
      'rws': '[别名] 获取仓库文档结构',
      'read_wiki_contents': '查看具体文档内容',
      'rwc': '[别名] 查看具体文档内容',
      'ask_question': '针对仓库提问',
      'aq': '[别名] 针对仓库提问',
      'view_share': '查看分享的查询结果',
      'vs': '[别名] 查看分享的查询结果'
    },
    options: {
      repoName: '仓库名称 (例如: "owner/repo")',
      topic: '文档主题名称',
      question: '关于仓库的问题',
      uuid: '分享查询的 UUID (例如: "_5495e609-f29e-44a7-a7bf-91c3f8f76303")',
      format: '输出格式 (brief|full|json, 默认: full)'
    },
    examples: {
      structure: '  deepwiki read_wiki_structure --repoName "openai/openai-node"',
      contents: '  deepwiki read_wiki_contents --repoName "openai/openai-node" --topic "Installation"',
      question: '  deepwiki ask_question --repoName "openai/openai-node" --question "如何认证?"',
      share: '  deepwiki view_share --uuid "_5495e609-f29e-44a7-a7bf-91c3f8f76303"',
      shareBrief: '  deepwiki view_share --uuid "..." --format brief',
      shareJson: '  deepwiki view_share --uuid "..." --format json'
    },
    errors: {
      noCommand: '错误: 未提供命令',
      invalidCommand: '错误: 无效的命令',
      missingRepo: '错误: 需要 --repoName 参数',
      missingTopic: '错误: 需要 --topic 参数',
      missingQuestion: '错误: 需要 --question 参数',
      missingUuid: '错误: 需要 --uuid 参数',
      connectionFailed: '错误: SSE 连接失败',
      requestFailed: '错误: 请求失败',
      timeout: '错误: 超时 - 未收到服务器响应'
    },
    help: {
      title: '帮助',
      commandsSection: '命令:',
      optionsSection: '选项:',
      examplesSection: '示例:',
      seeAlso: '更多信息请访问: https://github.com/Dwsy/deepwiki-skills'
    }
  }
};

// Detect language
function getLanguage() {
  const envLang = process.env.LANG || process.env.LC_ALL || process.env.LC_MESSAGES || '';
  if (envLang.startsWith('zh')) return 'zh';
  return 'en';
}

const LANG = getLanguage();
const t = MESSAGES[LANG];

// Print help
function printHelp() {
  console.log();
  console.log(t.usage);
  console.log();
  console.log(t.description);
  console.log();
  console.log(t.help.commandsSection);
  Object.entries(t.commands).forEach(([cmd, desc]) => {
    console.log(`  ${cmd.padEnd(25)} ${desc}`);
  });
  console.log();
  console.log(t.help.optionsSection);
  console.log(`  --repoName, -r, --repo  ${t.options.repoName}`);
  console.log(`  --topic, -t            ${t.options.topic}`);
  console.log(`  --question, -q         ${t.options.question}`);
  console.log(`  --uuid, -u             ${t.options.uuid}`);
  console.log(`  --format, -f           ${t.options.format}`);
  console.log(`  --lang, -l             Language (en|zh, default: auto)`);
  console.log(`  --help, -h             ${t.help.title}`);
  console.log();
  console.log('Aliases:');
  console.log('  dw                     Alias for deepwiki');
  console.log('  rws, str               read_wiki_structure');
  console.log('  rwc, cont              read_wiki_contents');
  console.log('  aq, ask                ask_question');
  console.log('  vs                     view_share');
  console.log();
  console.log(t.help.examplesSection);
  console.log(t.examples.structure);
  console.log(t.examples.contents);
  console.log(t.examples.question);
  console.log(t.examples.share);
  console.log(t.examples.shareBrief);
  console.log(t.examples.shareJson);
  console.log();
  console.log(t.help.seeAlso);
  console.log();
}

// Command aliases
const COMMAND_ALIASES = {
  'rws': 'read_wiki_structure',
  'rwc': 'read_wiki_contents',
  'aq': 'ask_question',
  'str': 'read_wiki_structure',
  'cont': 'read_wiki_contents',
  'ask': 'ask_question',
  'vs': 'view_share'
};

// Parameter aliases
const PARAM_ALIASES = {
  'r': 'repoName',
  'repo': 'repoName',
  't': 'topic',
  'q': 'question',
  'u': 'uuid',
  'l': 'lang',
  'f': 'format'
};

// Expand command alias
function expandCommand(cmd) {
  return COMMAND_ALIASES[cmd] || cmd;
}

// Expand parameter alias
function expandParam(param) {
  return PARAM_ALIASES[param] || param;
}

// Parse arguments
function parseArgs(args) {
  const result = {
    command: null,
    params: {},
    options: {}
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg === '--help' || arg === '-h') {
      result.options.help = true;
      return result;
    }

    if (arg.startsWith('--') || arg.startsWith('-')) {
      const key = expandParam(arg.replace(/^-+/, ''));
      const value = args[i + 1];

      if (key === 'lang') {
        result.options.lang = value;
        i++;
      } else if (value && !value.startsWith('-')) {
        result.params[key] = value;
        i++;
      } else {
        result.params[key] = true;
      }
    } else if (!result.command) {
      result.command = expandCommand(arg);
    }
  }

  return result;
}

// Validate command
function validateCommand(parsed) {
  if (parsed.options.help) {
    return null;
  }

  if (!parsed.command) {
    console.error(t.errors.noCommand);
    console.error();
    printHelp();
    process.exit(1);
  }

  const validCommands = Object.keys(t.commands);
  if (!validCommands.includes(parsed.command)) {
    console.error(`${t.errors.invalidCommand}: ${parsed.command}`);
    console.error();
    printHelp();
    process.exit(1);
  }

  // Validate required parameters
  if (parsed.command !== 'view_share' && !parsed.params.repoName) {
    console.error(t.errors.missingRepo);
    process.exit(1);
  }

  if (parsed.command === 'read_wiki_contents' && !parsed.params.topic) {
    console.error(t.errors.missingTopic);
    process.exit(1);
  }

  if (parsed.command === 'ask_question' && !parsed.params.question) {
    console.error(t.errors.missingQuestion);
    process.exit(1);
  }

  if (parsed.command === 'view_share' && !parsed.params.uuid) {
    console.error(t.errors.missingUuid);
    process.exit(1);
  }

  return parsed;
}

// Main function
async function run() {
  const args = process.argv.slice(2);
  const parsed = parseArgs(args);

  if (parsed.options.help || !parsed.command) {
    printHelp();
    process.exit(0);
  }

  const validated = validateCommand(parsed);
  if (!validated) return;

  const { command, params } = validated;

  // Handle view_share command directly via API
  if (command === 'view_share') {
    try {
      const url = `https://api.devin.ai/ada/query/${params.uuid}`;
      const format = params.format || 'full';

      const response = await axios.get(url, {
        headers: {
          'Accept': 'application/json'
        },
        timeout: 30000
      });

      const formatted = formatSharedQueryResponse(response.data, format);
      displayFormattedResponse(formatted);

      process.exit(0);
    } catch (err) {
      console.error(t.errors.requestFailed, err.response?.data || err.message);
      process.exit(1);
    }
  }

  const es = new EventSource(MCP_ENDPOINT);
  let postUrl = '';

  es.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);

      if (data.id === 2) {
        if (data.result && data.result.content) {
          console.log(data.result.content.map(c => c.text).join('\n'));
        } else if (data.error) {
          console.error(`${t.errors.requestFailed}:`, JSON.stringify(data.error, null, 2));
        } else {
          console.log(JSON.stringify(data, null, 2));
        }
        es.close();
        process.exit(0);
      }
    } catch (e) {
      // Ignore non-JSON messages
    }
  };

  es.addEventListener('endpoint', async (event) => {
    postUrl = new URL(event.data, MCP_ENDPOINT).href;

    try {
      // Initialize
      await axios.post(postUrl, {
        jsonrpc: '2.0',
        id: 1,
        method: 'initialize',
        params: {
          protocolVersion: '2024-11-05',
          capabilities: {},
          clientInfo: { name: 'pi-bridge', version: '1.0.0' }
        }
      });

      // Call tool
      await axios.post(postUrl, {
        jsonrpc: '2.0',
        id: 2,
        method: 'tools/call',
        params: {
          name: command,
          arguments: params
        }
      });
    } catch (err) {
      console.error(t.errors.requestFailed, err.response?.data || err.message);
      es.close();
      process.exit(1);
    }
  });

  es.onerror = (err) => {
    console.error(t.errors.connectionFailed, err);
    es.close();
    process.exit(1);
  };

  // Timeout protection
  setTimeout(() => {
    console.error(t.errors.timeout);
    es.close();
    process.exit(1);
  }, 30000);
}

run();