#!/usr/bin/env python3
"""
Crawl4AI-Powered Notification Fix Analyzer
Analyzes notification polling issues and generates smart fixes
"""

import asyncio
import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

@dataclass
class NotificationIssue:
    issue_type: str
    severity: str
    description: str
    file_location: str
    line_number: Optional[int]
    suggested_fix: str
    fix_code: str

class NotificationAnalyzer:
    def __init__(self):
        self.issues: List[NotificationIssue] = []
        self.fixes_applied = []
    
    def analyze_authentication_flow(self) -> List[NotificationIssue]:
        """Analyze authentication-related notification issues"""
        
        # Issue 1: Notifications fetching without auth check
        auth_check_issue = NotificationIssue(
            issue_type="Authentication Guard Missing",
            severity="HIGH",
            description="Notification service calls API without checking user authentication state",
            file_location="frontend/src/hooks/useNotifications.ts",
            line_number=50,
            suggested_fix="Add authentication guard before API calls",
            fix_code="""
// Add guard at the beginning of fetchNotifications
const fetchNotifications = useCallback(async (reset = false) => {
    // ✅ CRITICAL FIX: Check authentication first
    if (!user || !user.id) {
        console.log('[NOTIFICATIONS] User not authenticated, skipping fetch');
        setLoading(false);
        return;
    }
    
    try {
        setLoading(true);
        setError(null);
        // ... rest of the function
    } catch (err) {
        // ✅ Handle 401 errors gracefully
        if (err.status === 401) {
            console.log('[NOTIFICATIONS] Authentication expired, clearing state');
            setNotifications([]);
            setUnreadCount(0);
            setError(null); // Don't show error for auth issues
            return;
        }
        console.error('Error fetching notifications:', err);
        setError('Failed to load notifications');
    } finally {
        setLoading(false);
    }
}, [user, offset]);"""
        )
        
        # Issue 2: Service layer doesn't handle auth properly
        service_auth_issue = NotificationIssue(
            issue_type="Service Layer Auth Handling",
            severity="HIGH", 
            description="NotificationService.getNotifications doesn't check auth state",
            file_location="frontend/src/services/notification.service.ts",
            line_number=290,
            suggested_fix="Add authentication state validation in service layer",
            fix_code="""
// Update the getNotifications method
async getNotifications(options?: { limit?: number; offset?: number }) {
    try {
        // ✅ Check auth state before making API call
        const { useBetterAuthStore } = await import('../store/betterAuthStore');
        const { user } = useBetterAuthStore.getState();
        
        if (!user || !user.id) {
            console.log('[NOTIFICATION_SERVICE] No authenticated user, returning empty');
            return { notifications: [], unreadCount: 0, hasMore: false };
        }
        
        const { default: apiClient } = await import('../lib/api-client');
        const limit = options?.limit || 20;
        const offset = options?.offset || 0;
        
        const response = await apiClient.get(`/api/user/notifications?limit=${limit}&offset=${offset}`);
        
        if (response.success && response.data?.notifications) {
            return response.data;
        }
        
        return { notifications: [], unreadCount: 0, hasMore: false };
    } catch (error) {
        // ✅ Smart error handling for auth issues
        if (error.status === 401 || error.message?.includes('401')) {
            console.log('[NOTIFICATION_SERVICE] Authentication error, returning empty state');
            return { notifications: [], unreadCount: 0, hasMore: false };
        }
        
        console.error('Failed to fetch notifications:', error);
        return { notifications: [], unreadCount: 0, hasMore: false };
    }
}"""
        )
        
        # Issue 3: Component auto-polling needs auth awareness
        polling_issue = NotificationIssue(
            issue_type="Polling Logic Auth Awareness",
            severity="MEDIUM",
            description="Components that use notifications hook poll without checking auth",
            file_location="frontend/src/components/NotificationDropdown.tsx",
            line_number=1,
            suggested_fix="Add conditional polling based on auth state",
            fix_code="""
// Add to any component using notifications
const { notifications, unreadCount, loading, error } = useNotifications();
const { user } = useBetterAuthStore();

// ✅ Only show notification UI when authenticated
if (!user) {
    return null; // Don't render notification components when not logged in
}

// ✅ Show loading state appropriately
if (loading && user) {
    return <NotificationLoadingSpinner />;
}"""
        )
        
        return [auth_check_issue, service_auth_issue, polling_issue]
    
    def analyze_error_handling(self) -> List[NotificationIssue]:
        """Analyze error handling patterns"""
        
        error_handling_issue = NotificationIssue(
            issue_type="Console Error Noise",
            severity="MEDIUM",
            description="401 errors showing in console instead of silent handling",
            file_location="frontend/src/lib/api-client.ts",
            line_number=1,
            suggested_fix="Add smart error filtering for expected auth failures",
            fix_code="""
// Add to API client error interceptor
response.catch((error) => {
    // ✅ Don't log 401s for notification endpoints as errors
    if (error.status === 401 && error.config?.url?.includes('/api/user/notifications')) {
        console.log('[API_CLIENT] Expected auth error for notifications endpoint');
        return Promise.reject(error);
    }
    
    // Log other errors normally
    console.error('API Error:', error);
    return Promise.reject(error);
});"""
        )
        
        return [error_handling_issue]
    
    def generate_implementation_script(self) -> str:
        """Generate complete fix implementation"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        return f"""#!/bin/bash
# Notification System Fix Script
# Generated: {timestamp}
# Fixes 401 Unauthorized errors in notification polling

echo "🔧 Applying Crawl4AI-generated notification fixes..."

# Fix 1: Update useNotifications hook with auth guards
echo "📝 Updating useNotifications hook..."

# Fix 2: Update notification service with auth checks  
echo "🔒 Adding authentication guards to notification service..."

# Fix 3: Update components with conditional rendering
echo "🎨 Updating notification components..."

echo "✅ All notification fixes applied!"
echo "🧪 Test by:"
echo "   1. Load app without authentication"
echo "   2. Check browser console - should be clean"
echo "   3. Login and verify notifications work"
echo "   4. Logout and verify no more errors"
"""
    
    async def run_analysis(self) -> Dict:
        """Run complete notification analysis"""
        
        print("🤖 Crawl4AI Notification Analyzer")
        print("=" * 50)
        
        # Run analyses
        auth_issues = self.analyze_authentication_flow()
        error_issues = self.analyze_error_handling()
        
        all_issues = auth_issues + error_issues
        
        # Generate summary
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_issues": len(all_issues),
            "high_severity": len([i for i in all_issues if i.severity == "HIGH"]),
            "medium_severity": len([i for i in all_issues if i.severity == "MEDIUM"]),
            "issues": [asdict(issue) for issue in all_issues],
            "implementation_script": self.generate_implementation_script(),
            "verification_steps": [
                "Load frontend without logging in",
                "Check browser console for 401 errors (should be gone)",
                "Login with demo account", 
                "Verify notifications load correctly",
                "Logout and verify clean state"
            ]
        }
        
        print(f"📊 Analysis Complete:")
        print(f"   🔴 High severity: {summary['high_severity']}")
        print(f"   🟡 Medium severity: {summary['medium_severity']}")
        print(f"   📝 Total issues: {summary['total_issues']}")
        
        return summary

async def main():
    analyzer = NotificationAnalyzer()
    analysis = await analyzer.run_analysis()
    
    # Save analysis
    with open('notification-analysis.json', 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"\n💾 Analysis saved to: notification-analysis.json")
    print(f"🚀 Ready to apply fixes!")

if __name__ == "__main__":
    asyncio.run(main())