import React, { useEffect, useRef, useState } from 'react';
import Monaco, { OnMount } from '@monaco-editor/react';
import loader from '@monaco-editor/loader';
import * as monaco from 'monaco-editor';
import { Icon } from '@components/icons';

// 配置 Worker
loader.config({ paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.43.0/min/vs' } });

interface CodeBrowserProps {
  selectedNodeId?: string;
  fileContent?: string;
  filePath?: string;
  language?: string;
  readOnly?: boolean;
}

const CodeBrowser: React.FC<CodeBrowserProps> = ({
  selectedNodeId,
  fileContent = '',
  filePath = '',
  language = 'typescript',
  readOnly = true,
}) => {
  const [isReady, setIsReady] = useState(false);
  const editorRef = useRef<monaco.editor.IStandaloneCodeEditor | null>(null);

  const handleEditorMount: OnMount = (editor) => {
    editorRef.current = editor;
    setIsReady(true);
  };

  useEffect(() => {
    if (!isReady) return;
    if (!editorRef.current) return;
  }, [isReady, fileContent]);

  if (!fileContent || !filePath) {
    return (
      <div className="h-full flex items-center justify-center bg-muted/30">
        <div className="text-center">
          <Icon.FileCode size={48} className="mx-auto mb-4 text-muted-foreground/50" />
          <p className="text-sm text-muted-foreground">
            {selectedNodeId ? 'Select a node to view code' : 'No code selected'}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between px-4 py-2 border-b border-border bg-background/95">
        <span className="text-sm font-medium truncate text-foreground">{filePath}</span>
        <div className="flex items-center gap-2">
          <span className="text-xs text-muted-foreground capitalize">{language}</span>
        </div>
      </div>

      <div className="flex-1 overflow-hidden">
        <Monaco
          height="100%"
          defaultLanguage={language}
          value={fileContent}
          theme="vs-dark"
          options={{
            readOnly: readOnly,
            minimap: { enabled: false },
            fontSize: 13,
            fontFamily: "'JetBrains Mono', monospace",
            lineNumbers: 'on',
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 2,
            wordWrap: 'on',
          }}
          onMount={handleEditorMount}
          loading={
            <div className="flex items-center justify-center h-full">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          }
        />
      </div>
    </div>
  );
};

export default CodeBrowser;
