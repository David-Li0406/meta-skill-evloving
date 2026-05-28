import { Component, ErrorInfo, ReactNode } from 'react';
import { Button } from './ui/Button';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static override getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
      errorInfo: null,
    };
  }

  override componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    this.setState({
      error,
      errorInfo,
    });

    // TODO: Send error to error tracking service (e.g., Sentry)
  }

  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg shadow-lg p-8 max-w-2xl w-full">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
                <svg
                  className="w-6 h-6 text-red-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
              </div>
              <div>
                <h1 className="text-xl font-semibold text-gray-900">出错了</h1>
                <p className="text-sm text-gray-500">应用程序遇到了意外错误</p>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <h2 className="text-sm font-medium text-gray-900 mb-2">错误信息</h2>
                <div className="bg-gray-50 rounded-md p-4">
                  <p className="text-sm text-red-600 font-mono">{this.state.error?.message}</p>
                </div>
              </div>

              {this.state.errorInfo && (
                <div>
                  <h2 className="text-sm font-medium text-gray-900 mb-2">堆栈跟踪</h2>
                  <details className="bg-gray-50 rounded-md">
                    <summary className="px-4 py-3 text-sm text-gray-600 cursor-pointer hover:bg-gray-100 rounded-t-md">
                      查看详细信息
                    </summary>
                    <pre className="p-4 text-xs text-gray-600 overflow-auto max-h-64 font-mono">
                      {this.state.errorInfo.componentStack}
                    </pre>
                  </details>
                </div>
              )}

              <div className="flex gap-3 pt-4">
                <Button onClick={this.handleReset} variant="default">
                  重试
                </Button>
                <Button onClick={() => window.location.reload()} variant="outline">
                  刷新页面
                </Button>
              </div>

              <div className="pt-4 border-t border-gray-200">
                <p className="text-xs text-gray-500">
                  如果问题持续存在，请尝试：
                  <ul className="list-disc list-inside mt-2 space-y-1">
                    <li>清除浏览器缓存</li>
                    <li>重启应用程序</li>
                    <li>联系技术支持</li>
                  </ul>
                </p>
              </div>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
